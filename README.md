<p align="center"><img src="assets/title.png" alt="gpt-nano | tpg-onan" width="720"></p>

**tpg-onan** is a language model that reads backwards. I pretrained two identical [nanochat](https://github.com/karpathy/nanochat) base models from scratch on the same data: a normal forward model that predicts the **next** token, and a backward model that predicts the **previous** token. With both enabled at the same time, the user can generate text bi-directionally.

## How it works

A language model factorises a document left to right, but the chain rule works just as well right to left:

```
p(x_1 ... x_T) = ∏ p(x_t | x_<t) = ∏ p(x_t | x_>t)
```

The backward model learns the right-hand factorisation. We implement it by reversing every training document **at the token level** after tokenisation, keeping the BOS token first, and training with nanochat's ordinary next-token loss. On reversed text, "next token" is exactly the previous token of the original, so the model sees `x_T ... x_t` and predicts `x_(t-1)`. This is equivalent to flipping the attention mask and target.

## Results

Validation bits per byte (lower is better). 

| Model | Params | Training tokens | Forward bpb | Backward bpb | Backward gap |
|---|---:|---:|---:|---:|---:|
| d16 | 537M | 1.88B | 0.8013 | 0.8208 | +2.44% |
| d20 | 897M | 3.48B | **0.7566** | **0.7778** | +2.81% |

- Predicting the past is consistently, but only slightly, harder than predicting the future: about 2.5 to 3% more bits per byte.
- On individual passages the backward model sometimes wins, for example on logical arguments whose conclusion makes the premises easy to reconstruct (see `results/*/demo_report.md`).

Both pairs were trained at a 8:1 token-to-parameter ratio with FP8, each model on 2 H200 GPUs, side by side (d16: 50 minutes, d20: 2.5 hours).

## Demo

`web/` is a small site served by `scripts/demo_server.py`. Type a sentence and the backward model writes what came **before** it (violet) while the forward model writes what comes **after** it (grey). The Demos tab has curated prompts in five sections: Shakespeare, Reasonably reasonable, Working backwards, Math and Simple causal reasoning.

Given *"Therefore, Socrates is mortal."*, the backward d20 model wrote:

> All men are mortal. Therefore Socrates is mortal. ...

## Repository layout

| Path | What |
|---|---|
| `nanochat.patch` | All changes to nanochat's own files: the direction switch and token reversal in `nanochat/dataloader.py`, the direction recorded in checkpoint metadata (`scripts/base_train.py`), and demo-only sampling options in `nanochat/engine.py` (repetition penalty, blocked tokens) |
| `scripts/run_pair.sh` | Trains the forward and backward models side by side with identical settings |
| `scripts/compare_bpb.sh` | Evaluates val bpb for both models and prints the gap |
| `scripts/preflight_roundtrip.py` | CPU checks: every row starts with BOS, reversed documents round-trip to the originals, forward batches are unchanged from upstream |
| `scripts/sample_backward.py` | Command-line sampling (`--ending` for the backward model, `--beginning` for the forward model) |
| `scripts/demo_report.py` | Per-passage report: generations plus teacher-forced next-token and previous-token prediction tables |
| `scripts/demo_server.py` | FastAPI inference server for the website (streaming generation, per-token predictions) |
| `demo/passages.json` | The 14 passages used by `demo_report.py` |
| `web/` | The demo website |
| `results/` | `compare_bpb.log` and `demo_report.md` for d16 and d20 |

## Reproduce

```bash
git clone https://github.com/bentdixon/tpg-onan && cd tpg-onan
git clone https://github.com/karpathy/nanochat && cd nanochat
git checkout 92d63d4
git apply ../nanochat.patch
cp ../scripts/* scripts/ && mkdir -p demo && cp ../demo/passages.json demo/

# Set up nanochat as usual (uv venv, uv sync --extra gpu), download data, train the tokenizer:
python -m nanochat.dataset -n 120
python -m scripts.tok_train

python -m scripts.preflight_roundtrip                      # sanity checks, CPU only
bash scripts/run_pair.sh d20 --depth=20 --fp8 --target-param-data-ratio=8   # needs 4 GPUs
FWD_TAG=d20_fwd BWD_TAG=d20_bwd OUT_DIR=results/d20 bash scripts/compare_bpb.sh

# Demo site on http://localhost:8765
python -m scripts.demo_server --fwd-tag d20_fwd --bwd-tag d20_bwd
```

To sample the backward model by hand, reverse the prompt tokens on the way in and the generated tokens on the way out (`scripts/sample_backward.py` does this):

```bash
python -m scripts.sample_backward --model-tag d20_bwd --ending "Therefore, Socrates is mortal."
```

## Notes

- nanochat's CORE benchmark and in-training samples are turned off for both runs. They use left-to-right prompts that do not make sense for the backward model.
- Only base models were trained. nanochat's chat fine-tuning and RL stages were not run.
- Built on [karpathy/nanochat](https://github.com/karpathy/nanochat) at commit `92d63d4`.
