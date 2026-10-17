"""
Live inference server for the forward and backward base models.

Binds to 127.0.0.1 by default, so it is reachable only through an SSH tunnel
(see SERVER.md at the repository root).

    CUDA_VISIBLE_DEVICES=2 python -m scripts.demo_server --fwd-tag d16_fwd --bwd-tag d16_bwd --port 8765

Endpoints
    GET  /                 demo website (--web-dir), or the minimal test page if it is missing
    GET  /test             minimal test page
    GET  /health           model tags, steps, directions, device
    GET  /passages         demo passages (demo/passages.json)
    POST /generate         full generation, JSON response
    POST /generate/stream  token-by-token generation, Server-Sent Events
    POST /predict          teacher-forced per-token predictions (top-k) on a text

Request body for /generate and /generate/stream:
    {"direction": "forward" | "backward", "text": "...", "max_tokens": 128,
     "temperature": 0.8, "top_k": 50, "seed": 42, "repetition_penalty": 1.0, "num_samples": 1}
For "backward", text is the ending and the model writes what came before it.
"""

import argparse
import json
import os
import threading
import time
from typing import Literal

import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from nanochat.common import compute_init, autodetect_device_type
from nanochat.engine import Engine
from nanochat.checkpoint_manager import load_model

parser = argparse.ArgumentParser(description="Forward/backward live inference server")
parser.add_argument("--fwd-tag", type=str, default="d16_fwd")
parser.add_argument("--bwd-tag", type=str, default="d16_bwd")
parser.add_argument("--host", type=str, default="127.0.0.1", help="bind address (keep 127.0.0.1 and use an SSH tunnel)")
parser.add_argument("--port", type=int, default=8765)
parser.add_argument("--passages", type=str, default="demo/passages.json")
parser.add_argument("--web-dir", type=str, default="../web", help="static demo website served at / (skipped if missing)")
parser.add_argument("--max-tokens-limit", type=int, default=512, help="upper bound on max_tokens per request")
parser.add_argument("--device-type", type=str, default="", help="cuda|cpu|mps (empty = autodetect)")
args = parser.parse_args()

# -----------------------------------------------------------------------------
# Models

device_type = autodetect_device_type() if args.device_type == "" else args.device_type
_, _, _, _, device = compute_init(device_type)

MODELS = {}
for direction, tag in (("forward", args.fwd_tag), ("backward", args.bwd_tag)):
    model, tokenizer, meta = load_model("base", device, phase="eval", model_tag=tag)
    actual = meta.get("direction", "forward")
    assert actual == direction, f"{tag} was trained as {actual}, expected {direction}"
    MODELS[direction] = {"tag": tag, "step": meta["step"], "model": model, "engine": Engine(model, tokenizer)}
BOS = tokenizer.get_bos_token_id()

# Tokens that are only a separator line ("______", "=====", "....."), ignoring whitespace.
# Web text uses them as dividers, and the backward model sometimes emits them; blocking them
# keeps demo output readable. Short runs that occur in real text ("...", "--", "__") are kept.
SEPARATOR_MIN_RUN = {"_": 3, "=": 3, "*": 3, "~": 3, "#": 3, "-": 4, ".": 4}

def is_separator(s):
    s = s.strip()
    return len(s) >= SEPARATOR_MIN_RUN.get(s[:1], 10**9) and len(set(s)) == 1

SEPARATOR_TOKENS = [i for i in range(tokenizer.get_vocab_size()) if i != BOS and is_separator(tokenizer.decode([i]))]
print(f"Blocking {len(SEPARATOR_TOKENS)} separator tokens when block_separators is on")
GPU_LOCK = threading.Lock() # one request on the GPU at a time

# -----------------------------------------------------------------------------
# Core logic

class GenerateRequest(BaseModel):
    direction: Literal["forward", "backward"]
    text: str = Field(min_length=1)
    max_tokens: int = Field(default=128, ge=1)
    temperature: float = Field(default=0.8, ge=0.0, le=2.0)
    top_k: int = Field(default=50, ge=0)
    seed: int = 42
    repetition_penalty: float = Field(default=1.0, ge=1.0, le=2.0) # 1.0 = off
    num_samples: int = Field(default=1, ge=1, le=8)
    block_separators: bool = True # never sample separator-line tokens such as "______"


class PredictRequest(BaseModel):
    direction: Literal["forward", "backward"]
    text: str = Field(min_length=1)
    top_n: int = Field(default=5, ge=1, le=20)


def build_prompt(direction, text):
    ids = tokenizer.encode(text)
    return [BOS] + (ids[::-1] if direction == "backward" else ids)


def to_reading_order(direction, generated):
    """Decode generated tokens in normal reading order."""
    return tokenizer.decode(generated[::-1] if direction == "backward" else generated)


def gen_kwargs(req):
    return dict(max_tokens=min(req.max_tokens, args.max_tokens_limit), temperature=req.temperature,
                top_k=req.top_k or None, seed=req.seed, repetition_penalty=req.repetition_penalty,
                banned_tokens=SEPARATOR_TOKENS if req.block_separators else None)


def stream_events(req):
    """Yield SSE events. Each token event carries the full generated text so far, in reading order."""
    direction, entry = req.direction, MODELS[req.direction]
    prompt = build_prompt(direction, req.text)
    generated = []
    t0 = time.time()
    finished = "length"
    with GPU_LOCK:
        for token_column, _ in entry["engine"].generate(prompt, num_samples=1, **gen_kwargs(req)):
            token = token_column[0]
            if token == BOS:
                finished = "bos" # backward: reached the start of a document; forward: start of a new one
                break
            generated.append(token)
            event = {"type": "token", "token": tokenizer.decode([token]),
                     "generated": to_reading_order(direction, generated)}
            yield f"data: {json.dumps(event)}\n\n"
    dt = time.time() - t0
    done = {"type": "done", "direction": direction, "given": req.text,
            "generated": to_reading_order(direction, generated), "num_tokens": len(generated),
            "finish_reason": finished, "tokens_per_sec": len(generated) / dt if dt > 0 else 0.0}
    yield f"data: {json.dumps(done)}\n\n"


@torch.no_grad()
def predict(req):
    """Teacher-forced predictions for every token of the text, in the model's own order."""
    direction, entry = req.direction, MODELS[req.direction]
    ids = tokenizer.encode(req.text)
    seq = ids[::-1] if direction == "backward" else ids
    with GPU_LOCK:
        logits = entry["model"](torch.tensor([[BOS] + seq[:-1]], dtype=torch.long, device=device))[0].float()
    probs = torch.softmax(logits, dim=-1)
    targets = torch.tensor(seq, device=device)
    p_true = probs.gather(1, targets[:, None])[:, 0]
    ranks = (probs > p_true[:, None]).sum(dim=1) + 1
    top_p, top_i = probs.topk(req.top_n, dim=-1)
    rows = []
    for j in range(len(seq)):
        position = len(ids) - 1 - j if direction == "backward" else j # index in reading order
        rows.append({
            "step": j + 1, "position": position, "token": tokenizer.decode([seq[j]]),
            "p_true": p_true[j].item(), "rank": ranks[j].item(),
            "top": [{"token": tokenizer.decode([i]), "p": p} for i, p in zip(top_i[j].tolist(), top_p[j].tolist())],
        })
    bits = -torch.log2(p_true.clamp_min(1e-30)).sum().item()
    return {"direction": direction, "num_tokens": len(ids), "bpb": bits / len(req.text.encode("utf-8")),
            "top1_accuracy": (ranks == 1).float().mean().item(), "predictions": rows}

# -----------------------------------------------------------------------------
# HTTP

app = FastAPI(title="Forward vs Backward nanochat")
# Allow the website to be opened from another local origin (e.g. a file served on the laptop).
app.add_middleware(CORSMiddleware, allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
                   allow_methods=["GET", "POST"], allow_headers=["Content-Type"])


@app.get("/health")
def health():
    return {"status": "ok", "device": str(device),
            "models": {d: {"tag": m["tag"], "step": m["step"]} for d, m in MODELS.items()}}


@app.get("/passages")
def passages():
    if not os.path.exists(args.passages):
        raise HTTPException(404, f"{args.passages} not found")
    with open(args.passages, encoding="utf-8") as f:
        return json.load(f)


@app.post("/generate")
def generate(req: GenerateRequest):
    entry = MODELS[req.direction]
    prompt = build_prompt(req.direction, req.text)
    with GPU_LOCK:
        results, _ = entry["engine"].generate_batch(prompt, num_samples=req.num_samples, **gen_kwargs(req))
    samples = [to_reading_order(req.direction, seq[len(prompt):]) for seq in results]
    return {"direction": req.direction, "model_tag": entry["tag"], "given": req.text, "samples": samples}


@app.post("/generate/stream")
def generate_stream(req: GenerateRequest):
    return StreamingResponse(stream_events(req), media_type="text/event-stream")


@app.post("/predict")
def predict_endpoint(req: PredictRequest):
    return predict(req)


TEST_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Forward vs Backward</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 16px; line-height: 1.5; }
  textarea { width: 100%; height: 4rem; font: inherit; }
  .row { display: flex; gap: 1rem; align-items: center; flex-wrap: wrap; margin: .5rem 0; }
  .out { white-space: pre-wrap; border: 1px solid #ccc; border-radius: 6px; padding: .75rem; min-height: 4rem; }
  .gen { background: #fff3c4; } .given { font-weight: 600; }
  .meta { color: #666; font-size: .9em; }
</style></head><body>
<h1>Forward vs Backward</h1>
<p class="meta" id="health">Loading...</p>
<div class="row">
  <label><input type="radio" name="dir" value="backward" checked> Backward: given the ending, write what came before</label>
  <label><input type="radio" name="dir" value="forward"> Forward: given the beginning, continue</label>
</div>
<textarea id="text">So the match was cancelled and rescheduled for the following week.</textarea>
<div class="row">
  <label>Temperature <input id="temp" type="number" step="0.1" min="0" max="2" value="0.8"></label>
  <label>Top-k <input id="topk" type="number" min="0" value="50"></label>
  <label>Max tokens <input id="max" type="number" min="1" value="128"></label>
  <button id="go">Generate</button>
</div>
<div class="out" id="out"></div>
<p class="meta" id="stats"></p>
<script>
const $ = (id) => document.getElementById(id);
fetch("/health").then(r => r.json()).then(h => {
  $("health").textContent = Object.entries(h.models).map(([d, m]) => `${d}: ${m.tag} (step ${m.step})`).join(" | ") + ` | ${h.device}`;
});
function render(dir, given, gen) {
  const out = $("out"); out.textContent = "";
  const g = document.createElement("span"); g.className = "gen"; g.textContent = gen;
  const p = document.createElement("span"); p.className = "given"; p.textContent = given;
  if (dir === "backward") { out.append(g, p); } else { out.append(p, g); }
}
$("go").onclick = async () => {
  const dir = document.querySelector("input[name=dir]:checked").value;
  const text = $("text").value.trim();
  if (!text) return;
  // Backward: generated text precedes the ending; forward: it follows the beginning.
  const given = dir === "backward" ? " " + text : text;
  $("go").disabled = true; $("stats").textContent = ""; render(dir, given, "");
  const resp = await fetch("/generate/stream", {
    method: "POST", headers: {"Content-Type": "application/json"},
    body: JSON.stringify({direction: dir, text: text, temperature: +$("temp").value, top_k: +$("topk").value, max_tokens: +$("max").value}),
  });
  const reader = resp.body.getReader(); const dec = new TextDecoder(); let buf = "";
  while (true) {
    const {value, done} = await reader.read(); if (done) break;
    buf += dec.decode(value, {stream: true});
    const parts = buf.split("\\n\\n"); buf = parts.pop();
    for (const part of parts) {
      if (!part.startsWith("data: ")) continue;
      const ev = JSON.parse(part.slice(6));
      render(dir, given, ev.generated);
      if (ev.type === "done") $("stats").textContent = `${ev.num_tokens} tokens, ${ev.tokens_per_sec.toFixed(0)} tok/s, stopped: ${ev.finish_reason}`;
    }
  }
  $("go").disabled = false;
};
</script></body></html>"""


@app.get("/test", response_class=HTMLResponse)
def test_page():
    return TEST_PAGE


# Mount the website last so the API routes above take precedence.
if os.path.isdir(args.web_dir):
    app.mount("/", StaticFiles(directory=args.web_dir, html=True), name="web")
else:
    app.add_api_route("/", test_page, response_class=HTMLResponse)


if __name__ == "__main__":
    print(f"Serving on http://{args.host}:{args.port} (forward={args.fwd_tag}, backward={args.bwd_tag}, device={device})")
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
