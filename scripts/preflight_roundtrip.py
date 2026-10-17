"""
Pre-flight checks for the direction flag (CPU only, no GPU needed).

1. Round-trip: for both directions, every row starts with BOS, and every
   BOS-delimited segment decodes (after un-reversing, for backward) to a real
   document. Full segments must equal a document; the final segment in a row
   may be cropped, so it must be a prefix (forward) or suffix (backward).
2. Forward identity: with direction=forward, batches are identical to the
   unmodified loader at HEAD (loaded from git).

    python -m scripts.preflight_roundtrip
"""

import importlib
import os
import subprocess
import sys
import types

import torch

B, T, NUM_BATCHES = 8, 2048, 3


def load_loader(direction):
    os.environ["NANOCHAT_DIRECTION"] = direction
    import nanochat.dataloader as dl
    return importlib.reload(dl)


def load_reference_loader():
    src = subprocess.check_output(["git", "show", "HEAD:nanochat/dataloader.py"], text=True)
    mod = types.ModuleType("reference_dataloader")
    exec(compile(src, "reference_dataloader.py", "exec"), mod.__dict__)
    return mod


def source_docs(dl, n_batches=40):
    docs = []
    it = dl._document_batches("train", None, 128)
    for _ in range(n_batches):
        docs.extend(next(it)[0])
    return docs


def batches(dl, tokenizer):
    loader = dl.tokenizing_distributed_data_loader_bos_bestfit(tokenizer, B, T, "train", device="cpu")
    for _ in range(NUM_BATCHES):
        x, y = next(loader)
        yield torch.cat([x, y[:, -1:]], dim=1).clone() # full row of T+1 tokens


def check_roundtrip(direction, tokenizer):
    dl = load_loader(direction)
    docs = source_docs(dl)
    doc_set = set(docs)
    bos = tokenizer.get_bos_token_id()
    n_full = n_crop = 0
    for rows in batches(dl, tokenizer):
        for row in rows.tolist():
            assert row[0] == bos, f"[{direction}] row does not start with BOS"
            starts = [i for i, t in enumerate(row) if t == bos] + [len(row)]
            for k in range(len(starts) - 1):
                seg = row[starts[k] + 1:starts[k + 1]]
                if direction == "backward":
                    seg = seg[::-1]
                text = tokenizer.decode(seg)
                last = k == len(starts) - 2
                if text in doc_set:
                    n_full += 1
                elif last and any((d.endswith(text) if direction == "backward" else d.startswith(text)) for d in docs):
                    n_crop += 1
                else:
                    raise AssertionError(f"[{direction}] segment {k} does not match any source document:\n{text[:300]!r}")
    print(f"[{direction}] round-trip OK: {n_full} full documents, {n_crop} cropped tails")
    return dl


def main():
    from nanochat.tokenizer import get_tokenizer
    tokenizer = get_tokenizer()

    # Show one backward example for the log
    dl = load_loader("backward")
    rows = next(batches(dl, tokenizer))
    row = rows[0].tolist()
    bos = tokenizer.get_bos_token_id()
    end = row.index(bos, 1) if bos in row[1:] else len(row)
    print("Backward row 0, first segment as stored (reversed):", repr(tokenizer.decode(row[1:end])[:200]))
    print("Backward row 0, first segment un-reversed:          ", repr(tokenizer.decode(row[1:end][::-1])[:200]))

    check_roundtrip("backward", tokenizer)
    fwd = check_roundtrip("forward", tokenizer)

    ref = load_reference_loader()
    for a, b in zip(batches(fwd, tokenizer), batches(ref, tokenizer)):
        assert torch.equal(a, b), "forward batches differ from the unmodified loader"
    print("Forward identity OK: batches match unmodified loader")
    print("ALL PREFLIGHT CHECKS PASSED")


if __name__ == "__main__":
    sys.exit(main())
