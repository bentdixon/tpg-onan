#!/bin/bash
# Train the forward and backward models side by side with identical settings.
# Run from the nanochat directory with its venv active.
# Usage: bash scripts/run_pair.sh <tag_prefix> <extra base_train args...>
#   e.g. bash scripts/run_pair.sh d20 --depth=20 --fp8 --target-param-data-ratio=8
# Forward uses GPUs 0,1 and backward GPUs 2,3 (2-way DDP each). Both runs must use the same
# number of GPUs: DDP shards the data by rank, so a different world size changes data order.
set -e
export OMP_NUM_THREADS=1
mkdir -p logs
P=$1; shift
# Per-run compile caches on local disk. A shared cache races when several processes compile
# the same kernels at once (FileNotFoundError in Triton).
CACHE=${CACHE:-/tmp/nanochat_compile_cache}
mkdir -p $CACHE/${P}_fwd $CACHE/${P}_bwd
TRITON_CACHE_DIR=$CACHE/${P}_fwd/triton TORCHINDUCTOR_CACHE_DIR=$CACHE/${P}_fwd/inductor CUDA_VISIBLE_DEVICES=0,1 NANOCHAT_DIRECTION=forward  torchrun --nproc_per_node=2 --master_port=29511 -m scripts.base_train -- --model-tag=${P}_fwd --core-metric-every=-1 --sample-every=-1 "$@" > logs/${P}_fwd.log 2>&1 &
TRITON_CACHE_DIR=$CACHE/${P}_bwd/triton TORCHINDUCTOR_CACHE_DIR=$CACHE/${P}_bwd/inductor CUDA_VISIBLE_DEVICES=2,3 NANOCHAT_DIRECTION=backward torchrun --nproc_per_node=2 --master_port=29512 -m scripts.base_train -- --model-tag=${P}_bwd --core-metric-every=-1 --sample-every=-1 "$@" > logs/${P}_bwd.log 2>&1 &
wait
echo PAIR_DONE
