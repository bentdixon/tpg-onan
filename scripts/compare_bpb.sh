#!/bin/bash
# Evaluate val bits-per-byte for the forward and backward models in parallel and print the gap.
# Run from the nanochat directory with its venv active.
# Usage: FWD_TAG=d20_fwd BWD_TAG=d20_bwd OUT_DIR=results/d20 bash scripts/compare_bpb.sh
set -e
FWD_TAG=${FWD_TAG:-d16_fwd}
BWD_TAG=${BWD_TAG:-d16_bwd}
FWD_GPU=${FWD_GPU:-0}
BWD_GPU=${BWD_GPU:-1}
OUT_DIR=${OUT_DIR:-results}
mkdir -p "$OUT_DIR"
CUDA_VISIBLE_DEVICES=$FWD_GPU NANOCHAT_DIRECTION=forward  python -m scripts.base_eval --model-tag "$FWD_TAG" --eval bpb 2>&1 | tee "$OUT_DIR/bpb_fwd.log" &
CUDA_VISIBLE_DEVICES=$BWD_GPU NANOCHAT_DIRECTION=backward python -m scripts.base_eval --model-tag "$BWD_TAG" --eval bpb 2>&1 | tee "$OUT_DIR/bpb_bwd.log" &
wait
OUT_DIR="$OUT_DIR" python - <<'PY'
import os, re
d = os.environ["OUT_DIR"]
def val(path):
    return float(re.findall(r"val bpb: ([0-9.]+)", open(path).read())[-1])
f, b = val(f"{d}/bpb_fwd.log"), val(f"{d}/bpb_bwd.log")
print(f"val bpb  forward: {f:.6f}  backward: {b:.6f}  delta: {100 * (b - f) / f:+.3f}%")
PY
