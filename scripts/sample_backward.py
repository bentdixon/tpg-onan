"""
Sample from a forward or backward base model.

Backward model: given an ending, generate the text that precedes it.
    python -m scripts.sample_backward --model-tag d16_bwd --ending "TEXT"

Forward model: given a beginning, generate the continuation.
    python -m scripts.sample_backward --model-tag d16_fwd --beginning "TEXT"

Batch mode over a JSON list of {"id", "beginning", "ending"} items (each model
uses the field matching its direction), writing all samples to a JSON file:
    python -m scripts.sample_backward --model-tag d16_bwd --prompts-file demo.json --out results/samples_bwd.json
"""

import argparse
import json
import os

from nanochat.common import compute_init, autodetect_device_type
from nanochat.engine import Engine
from nanochat.checkpoint_manager import load_model

parser = argparse.ArgumentParser(description="Sample from a forward or backward base model")
parser.add_argument("--model-tag", type=str, required=True, help="checkpoint directory name, e.g. d16_bwd")
parser.add_argument("--step", type=int, default=None, help="checkpoint step (default = last)")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--ending", type=str, help="ending text (backward model)")
group.add_argument("--beginning", type=str, help="beginning text (forward model)")
group.add_argument("--prompts-file", type=str, help="JSON list of {id, beginning, ending}")
parser.add_argument("--out", type=str, default=None, help="write samples as JSON to this path")
parser.add_argument("--num-samples", type=int, default=3)
parser.add_argument("--max-tokens", type=int, default=256)
parser.add_argument("--temperature", type=float, default=0.8)
parser.add_argument("--top-k", type=int, default=50)
parser.add_argument("--seed", type=int, default=42)
parser.add_argument("--device-type", type=str, default="", help="cuda|cpu|mps (empty = autodetect)")
args = parser.parse_args()

device_type = autodetect_device_type() if args.device_type == "" else args.device_type
_, _, _, _, device = compute_init(device_type)
model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=args.model_tag, step=args.step)
direction = meta.get("direction", "forward")
backward = direction == "backward"
engine = Engine(model, tokenizer)
bos = tokenizer.get_bos_token_id()

if args.ending is not None:
    assert backward, f"--ending requires a backward model, but {args.model_tag} is {direction}"
if args.beginning is not None:
    assert not backward, f"--beginning requires a forward model, but {args.model_tag} is {direction}"


def sample(text):
    """Return a list of (generated, given) text pairs for one prompt."""
    ids = tokenizer.encode(text)
    prompt = [bos] + (ids[::-1] if backward else ids)
    results, _ = engine.generate_batch(
        prompt, num_samples=args.num_samples, max_tokens=args.max_tokens,
        temperature=args.temperature, top_k=args.top_k, seed=args.seed,
    )
    outputs = []
    for seq in results:
        generated = seq[len(prompt):] # results include the prompt; terminal BOS is excluded
        if backward:
            generated = generated[::-1] # back to reading order
        outputs.append(tokenizer.decode(generated))
    return outputs


def show(given, outputs):
    for i, gen in enumerate(outputs):
        print(f"--- sample {i + 1} ({direction}) ---")
        if backward:
            print(f"[GENERATED] {gen}\n[ENDING] {given}")
        else:
            print(f"[BEGINNING] {given}\n[GENERATED] {gen}")
    print()


records = []
if args.prompts_file:
    with open(args.prompts_file, encoding="utf-8") as f:
        items = json.load(f)
    for item in items:
        given = item["ending"] if backward else item["beginning"]
        print(f"=== {item['id']} ===")
        outputs = sample(given)
        show(given, outputs)
        records.append({"id": item["id"], "direction": direction, "given": given, "samples": outputs})
else:
    given = args.ending if backward else args.beginning
    outputs = sample(given)
    show(given, outputs)
    records.append({"id": "cli", "direction": direction, "given": given, "samples": outputs})

if args.out:
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"model_tag": args.model_tag, "step": meta["step"], "settings": vars(args), "results": records}, f, indent=2, ensure_ascii=False)
    print(f"Wrote {args.out}")
