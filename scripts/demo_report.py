"""
Run the forward and backward models on the demo passages and write a Markdown
report with clearly labelled tables:

  - Next-token predictions (forward model): for every token of the passage,
    the model sees the tokens to its LEFT and predicts it.
  - Previous-token predictions (backward model): for every token of the passage,
    the model sees the tokens to its RIGHT and predicts it.
  - Generations: forward continues the first sentence; backward writes what
    came before the last sentence.

    python -m scripts.demo_report --fwd-tag d16_fwd --bwd-tag d16_bwd \
        --passages demo/passages.json --out-dir results
"""

import argparse
import json
import math
import os

import torch

from nanochat.common import compute_init, autodetect_device_type
from nanochat.engine import Engine
from nanochat.checkpoint_manager import load_model

parser = argparse.ArgumentParser(description="Forward vs backward demo report")
parser.add_argument("--fwd-tag", type=str, default="d16_fwd")
parser.add_argument("--bwd-tag", type=str, default="d16_bwd")
parser.add_argument("--passages", type=str, default="demo/passages.json")
parser.add_argument("--out-dir", type=str, default="results")
parser.add_argument("--num-samples", type=int, default=3, help="sampled generations per passage (plus one greedy)")
parser.add_argument("--max-tokens", type=int, default=96)
parser.add_argument("--temperature", type=float, default=0.8)
parser.add_argument("--top-k", type=int, default=50)
parser.add_argument("--top-n", type=int, default=5, help="top predictions shown per token")
parser.add_argument("--context-tokens", type=int, default=4, help="adjacent context tokens shown per row")
parser.add_argument("--seed", type=int, default=42)
parser.add_argument("--device-type", type=str, default="", help="cuda|cpu|mps (empty = autodetect)")
args = parser.parse_args()

device_type = autodetect_device_type() if args.device_type == "" else args.device_type
_, _, _, _, device = compute_init(device_type)

fwd_model, tokenizer, fwd_meta = load_model("base", device, phase="eval", model_tag=args.fwd_tag)
bwd_model, _, bwd_meta = load_model("base", device, phase="eval", model_tag=args.bwd_tag)
assert fwd_meta.get("direction", "forward") == "forward", f"{args.fwd_tag} is not a forward model"
assert bwd_meta.get("direction") == "backward", f"{args.bwd_tag} is not a backward model"
fwd_engine, bwd_engine = Engine(fwd_model, tokenizer), Engine(bwd_model, tokenizer)
bos = tokenizer.get_bos_token_id()

# -----------------------------------------------------------------------------
# Model calls

@torch.no_grad()
def token_predictions(model, seq):
    """Teacher-forced predictions. seq = target tokens in the model's own order.
    Returns, for each target, (p_true, rank, [(token_id, prob) * top_n])."""
    idx = torch.tensor([[bos] + seq[:-1]], dtype=torch.long, device=device)
    logits = model(idx)[0].float()
    probs = torch.softmax(logits, dim=-1)
    targets = torch.tensor(seq, device=device)
    p_true = probs.gather(1, targets[:, None])[:, 0]
    ranks = (probs > p_true[:, None]).sum(dim=1) + 1
    top_p, top_i = probs.topk(args.top_n, dim=-1)
    return [
        (p_true[t].item(), ranks[t].item(), list(zip(top_i[t].tolist(), top_p[t].tolist())))
        for t in range(len(seq))
    ]


def generate(engine, prompt_ids, backward):
    """One greedy plus num_samples sampled generations, returned in reading order."""
    prompt = [bos] + (prompt_ids[::-1] if backward else prompt_ids)
    runs = [("greedy", 1, 0.0)] + [("sample", args.num_samples, args.temperature)]
    outputs = []
    for kind, n, temp in runs:
        results, _ = engine.generate_batch(prompt, num_samples=n, max_tokens=args.max_tokens,
                                           temperature=temp, top_k=args.top_k, seed=args.seed)
        for seq in results:
            gen = seq[len(prompt):] # results include the prompt
            outputs.append((kind, tokenizer.decode(gen[::-1] if backward else gen)))
    return outputs

# -----------------------------------------------------------------------------
# Markdown helpers

def cell(text):
    """Make arbitrary text safe for a Markdown table cell."""
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " \u21b5 ").strip() or "\u2205"


def tok(token_id):
    """Show a single token with visible whitespace."""
    s = tokenizer.decode([token_id]).replace("`", "'").replace("|", "\\|")
    s = s.replace("\n", "\\n").replace(" ", "\u2423")
    return f"`{s}`" if s else "`\u2205`"


def ctx(ids):
    return cell(tokenizer.decode(ids))


def prediction_table(rows, title, context_header):
    lines = [
        f"**{title}**", "",
        f"| Step | {context_header} | True token | p(true) | Rank | Top-{args.top_n} predictions |",
        "|---:|---|---|---:|---:|---|",
    ]
    for r in rows:
        top = ", ".join(f"{tok(i)} {p:.2f}" for i, p in r["top"])
        lines.append(f"| {r['step']} | {r['context']} | {tok(r['token'])} | {r['p']:.3f} | {r['rank']} | {top} |")
    return lines

# -----------------------------------------------------------------------------
# Run

with open(args.passages, encoding="utf-8") as f:
    passages = json.load(f)

records = []
for item in passages:
    text = " ".join([item["beginning"], item["middle"], item["ending"]])
    ids = tokenizer.encode(text)
    n, n_bytes = len(ids), len(text.encode("utf-8"))
    K = args.context_tokens

    # Next-token: forward model predicts ids[t] from ids[:t], in reading order.
    fwd_preds = token_predictions(fwd_model, ids)
    fwd_rows = [{
        "step": t + 1, "token": ids[t], "p": p, "rank": rank, "top": top,
        "context": ("\u2026" if t > K else "") + (ctx(ids[max(0, t - K):t]) if t > 0 else "[start of text]") + " \u2192 ?",
    } for t, (p, rank, top) in enumerate(fwd_preds)]

    # Previous-token: backward model predicts ids[t] from ids[t+1:], from the end to the start.
    bwd_preds = token_predictions(bwd_model, ids[::-1])
    bwd_rows = []
    for j, (p, rank, top) in enumerate(bwd_preds):
        t = n - 1 - j # position of the target in reading order
        right = ids[t + 1:t + 1 + K]
        bwd_rows.append({
            "step": j + 1, "token": ids[t], "p": p, "rank": rank, "top": top,
            "context": "? \u2190 " + (ctx(right) if right else "[end of text]") + ("\u2026" if t + 1 + K < n else ""),
        })

    fwd_bits = -sum(math.log2(max(r["p"], 1e-30)) for r in fwd_rows)
    bwd_bits = -sum(math.log2(max(r["p"], 1e-30)) for r in bwd_rows)

    fwd_gen = generate(fwd_engine, tokenizer.encode(item["beginning"]), backward=False)
    bwd_gen = generate(bwd_engine, tokenizer.encode(item["ending"]), backward=True)

    records.append({
        **item, "text": text, "num_tokens": n, "num_bytes": n_bytes,
        "fwd_bpb": fwd_bits / n_bytes, "bwd_bpb": bwd_bits / n_bytes,
        "fwd_top1": sum(r["rank"] == 1 for r in fwd_rows) / n,
        "bwd_top1": sum(r["rank"] == 1 for r in bwd_rows) / n,
        "next_token_predictions": fwd_rows, "prev_token_predictions": bwd_rows,
        "forward_generations": [{"kind": k, "text": g} for k, g in fwd_gen],
        "backward_generations": [{"kind": k, "text": g} for k, g in bwd_gen],
    })
    print(f"{item['id']:18s} fwd bpb {fwd_bits / n_bytes:.3f}  bwd bpb {bwd_bits / n_bytes:.3f}")

# -----------------------------------------------------------------------------
# Report

md = [
    "# Forward vs Backward: Demo Report", "",
    f"- Forward model: `{args.fwd_tag}` (step {fwd_meta['step']}), next-token prediction: sees tokens to the **left**.",
    f"- Backward model: `{args.bwd_tag}` (step {bwd_meta['step']}), previous-token prediction: sees tokens to the **right**.",
    f"- Generation: 1 greedy + {args.num_samples} samples (temperature {args.temperature}, top-k {args.top_k}, max {args.max_tokens} tokens, seed {args.seed}).",
    "- Token tables are teacher-forced on the true passage. `\u2423` marks a space; Rank 1 means the model's top guess was correct.", "",
    "## Summary", "",
    "| # | Passage | Category | Tokens | Next-token bpb (fwd) | Prev-token bpb (bwd) | Next-token top-1 acc | Prev-token top-1 acc |",
    "|---:|---|---|---:|---:|---:|---:|---:|",
]
for i, r in enumerate(records, 1):
    md.append(f"| {i} | [{r['id']}](#{i}-{r['id'].replace('_', '-')}) | {r['category']} | {r['num_tokens']} | "
              f"{r['fwd_bpb']:.3f} | {r['bwd_bpb']:.3f} | {r['fwd_top1']:.0%} | {r['bwd_top1']:.0%} |")
tot_bytes = sum(r["num_bytes"] for r in records)
mean_fwd = sum(r["fwd_bpb"] * r["num_bytes"] for r in records) / tot_bytes
mean_bwd = sum(r["bwd_bpb"] * r["num_bytes"] for r in records) / tot_bytes
md += ["", f"Byte-weighted mean bpb on demo passages: forward **{mean_fwd:.3f}**, backward **{mean_bwd:.3f}** "
           f"({100 * (mean_bwd - mean_fwd) / mean_fwd:+.1f}%). Small sample; use `compare_bpb.sh` for the real comparison.", ""]

for i, r in enumerate(records, 1):
    md += [
        "---", "", f"## {i}. {r['id']}", "",
        f"*Category: {r['category']}*", "",
        f"> **Beginning:** {r['beginning']}  ",
        f"> **Middle:** {r['middle']}  ",
        f"> **Ending:** {r['ending']}", "",
        "### Generations", "",
        "**Backward model: given the ending, generate what came before**", "",
        "| Run | Generated (preceding text) | Given ending |",
        "|---|---|---|",
    ]
    md += [f"| {g['kind']} | {cell(g['text'])} | {cell(r['ending'])} |" for g in r["backward_generations"]]
    md += [
        "", "**Forward model: given the beginning, generate what comes after**", "",
        "| Run | Given beginning | Generated (continuation) |",
        "|---|---|---|",
    ]
    md += [f"| {g['kind']} | {cell(r['beginning'])} | {cell(g['text'])} |" for g in r["forward_generations"]]
    md += ["", "### Token predictions on the true passage", "",
           f"| Model | Direction | bpb | Top-1 accuracy |", "|---|---|---:|---:|",
           f"| Forward | next-token (left context) | {r['fwd_bpb']:.3f} | {r['fwd_top1']:.0%} |",
           f"| Backward | previous-token (right context) | {r['bwd_bpb']:.3f} | {r['bwd_top1']:.0%} |", ""]
    md += prediction_table(r["next_token_predictions"],
                           "Next-token predictions (forward model, read left to right)", "Left context \u2192 ?")
    md += [""]
    md += prediction_table(r["prev_token_predictions"],
                           "Previous-token predictions (backward model, read right to left)", "? \u2190 Right context")
    md += [""]

os.makedirs(args.out_dir, exist_ok=True)
md_path = os.path.join(args.out_dir, "demo_report.md")
json_path = os.path.join(args.out_dir, "demo_results.json")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))
with open(json_path, "w", encoding="utf-8") as f:
    json.dump({"settings": vars(args), "fwd_step": fwd_meta["step"], "bwd_step": bwd_meta["step"],
               "results": records}, f, indent=2, ensure_ascii=False)
print(f"Wrote {md_path} and {json_path}")
