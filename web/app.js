// Flip the Script demo site. Talks to scripts/demo_server.py.
// The API defaults to the same origin; override with ?api=http://localhost:8765
// All model output is inserted with textContent, never as HTML.

const API = new URLSearchParams(location.search).get("api") || "";
// demos.json sits next to this script, so pages in subfolders (alt/) can share it.
const SCRIPT_DIR = new URL(".", document.currentScript.src);
const $ = (id) => document.getElementById(id);

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k === "text") node.textContent = v;
    else node.setAttribute(k, v);
  }
  for (const c of children) node.append(c);
  return node;
}

// ---------------------------------------------------------------------------
// One quiet line for server state and errors.

function notify(text = "", isError = false) {
  $("notice").textContent = text;
  $("notice").classList.toggle("error", isError);
}

let serverUp = null;

async function checkHealth() {
  try {
    const r = await fetch(`${API}/health`, { cache: "no-store" });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const h = await r.json();
    $("d-fwd").textContent = `${h.models.forward.tag}, step ${h.models.forward.step}`;
    $("d-bwd").textContent = `${h.models.backward.tag}, step ${h.models.backward.step}`;
    $("d-device").textContent = h.device;
    if (serverUp === false) notify();
    serverUp = true;
    setTimeout(checkHealth, 30000);
  } catch (e) {
    serverUp = false;
    notify("Server unreachable. Is scripts/demo_server.py running?", true);
    setTimeout(checkHealth, 4000);
  }
}

function explain(e) {
  if (e instanceof TypeError) { checkHealth(); return "Lost the server. Check the SSH tunnel."; }
  return e.message;
}

async function failure(resp) {
  let detail = "";
  try {
    const body = await resp.json();
    detail = Array.isArray(body.detail) ? body.detail.map((d) => d.msg).join("; ") : String(body.detail || "");
  } catch (e) { /* not JSON */ }
  return new Error(resp.status === 422
    ? `Invalid settings${detail ? `: ${detail}` : ""}. Adjust them in Options.`
    : `Server error ${resp.status}${detail ? `: ${detail}` : ""}.`);
}

// ---------------------------------------------------------------------------
// Tabs. The URL hash remembers the view.

const tabs = [...document.querySelectorAll('[role="tab"]')];
const viewName = (tab) => tab.id.slice(4);

function selectTab(tab, focus = true) {
  for (const t of tabs) {
    const selected = t === tab;
    t.setAttribute("aria-selected", String(selected));
    t.tabIndex = selected ? 0 : -1;
    $(t.getAttribute("aria-controls")).hidden = !selected;
  }
  history.replaceState(null, "", `#${viewName(tab)}`);
  if (focus) tab.focus();
}
tabs.forEach((tab, i) => {
  tab.addEventListener("click", () => selectTab(tab));
  tab.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") selectTab(tabs[(i + 1) % tabs.length]);
    if (e.key === "ArrowLeft") selectTab(tabs[(i - 1 + tabs.length) % tabs.length]);
  });
});
const tabFromHash = () => tabs.find((t) => `#${viewName(t)}` === location.hash) || tabs[0];
selectTab(tabFromHash(), false);
window.addEventListener("hashchange", () => selectTab(tabFromHash(), false));
const activeView = () => viewName(tabs.find((t) => t.getAttribute("aria-selected") === "true"));

// ---------------------------------------------------------------------------
// Generation. The server runs one request at a time, so the page keeps at most
// one generation in flight; starting another stops the current one.

const SETTINGS = [
  // [input id, output id, request field, default, parse, format]
  ["set-temp", "out-temp", "temperature", 0.8, parseFloat, (v) => v.toFixed(2)],
  ["set-topk", "out-topk", "top_k", 50, (v) => parseInt(v, 10), (v) => (v === 0 ? "off" : String(v))],
  ["set-rep", "out-rep", "repetition_penalty", 1.0, parseFloat, (v) => (v === 1 ? "off" : v.toFixed(2))],
  ["set-max", "out-max", "max_tokens", 128, (v) => parseInt(v, 10), String],
  ["set-seed", "out-seed", "seed", 42, (v) => parseInt(v, 10), String],
  ["set-speed", "out-speed", "speed", 1.0, parseFloat, (v) => (v >= 2 ? "instant" : `${v.toFixed(1)}x`)],
];
const CLIENT_ONLY = new Set(["speed"]); // settings used by the page, not sent to the server
const STORE_KEY = "flip-options";

function settings({ request = false } = {}) {
  const out = {};
  for (const [id, , field, fallback, parse] of SETTINGS) {
    if (request && CLIENT_ONLY.has(field)) continue;
    const v = parse($(id).value);
    out[field] = Number.isFinite(v) ? v : fallback;
  }
  return out;
}

function showSettings() {
  for (const [id, outId, , , parse, format] of SETTINGS) $(outId).textContent = format(parse($(id).value));
}

function saveSettings() {
  try { localStorage.setItem(STORE_KEY, JSON.stringify(settings())); } catch (e) { /* storage unavailable */ }
}

function loadSettings() {
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(STORE_KEY)) || {}; } catch (e) { /* storage unavailable */ }
  for (const [id, , field] of SETTINGS) if (Number.isFinite(saved[field])) $(id).value = saved[field];
  showSettings();
}

for (const [id] of SETTINGS) $(id).addEventListener("input", () => { showSettings(); saveSettings(); });
$("options-reset").addEventListener("click", () => {
  for (const [id, , , fallback] of SETTINGS) $(id).value = fallback;
  showSettings();
  saveSettings();
});
loadSettings();

// ---------------------------------------------------------------------------
// Options drawer: the handle toggles it; Esc or a click outside closes it.

const drawer = $("options");
const handle = $("options-handle");
const drawerOpen = () => handle.getAttribute("aria-expanded") === "true";

function setDrawer(open) {
  handle.setAttribute("aria-expanded", String(open));
  drawer.classList.toggle("open", open);
  drawer.inert = !open;
  if (open) drawer.querySelector("input").focus();
}
handle.addEventListener("click", () => setDrawer(!drawerOpen()));
document.addEventListener("pointerdown", (e) => {
  if (drawerOpen() && !drawer.contains(e.target) && !handle.contains(e.target)) setDrawer(false);
});

let current = null; // { controller, done }

function stopCurrent() { if (current) current.controller.abort(); }

async function exclusive(task) {
  if (current) { current.controller.abort(); await current.done.catch(() => {}); }
  const controller = new AbortController();
  const done = task(controller.signal);
  current = { controller, done };
  try { return await done; } finally { if (current && current.done === done) current = null; }
}

// Stream one generation. onText receives the generated text so far, in reading order.
async function streamGenerate(direction, text, onText, signal) {
  const resp = await fetch(`${API}/generate/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ direction, text, ...settings({ request: true }) }),
    signal,
  });
  if (!resp.ok) throw await failure(resp);
  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop();
    for (const raw of events) {
      if (raw.startsWith("data: ")) onText(JSON.parse(raw.slice(6)).generated);
    }
  }
}

// Streamed text arrives in bursts of tokens. A Reveal buffers it and shows it a few
// characters per frame at a steady pace that speeds up when the buffer grows, so the
// text flows instead of jumping. Backward text grows at its start, forward at its end.

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const BASE_RATE = 90;   // characters per second when the buffer is short (speed 1)
const CATCH_UP = 0.35;  // seconds to drain whatever is buffered (speed 1)

// Text speed setting: 0.1 is very slow, 1 is the default, 2 shows text as soon as it arrives.
// Below 1 text reveals at a fixed, slower rate; above 1 the reveal rate grows without bound.
function revealSpeed() {
  const s = settings().speed;
  return s >= 2 ? Infinity : s;
}

class Reveal {
  constructor(slot, backward, anchor) {
    this.slot = slot;
    this.backward = backward;
    this.anchor = anchor; // element that must not move while backward text grows above it
    this.target = "";
    this.shown = "";
    this.count = 0;       // characters of target revealed (fractional)
    this.frame = null;
    this.idle = null;
    this.caret = el("span", { class: "caret", "aria-hidden": "true" });
    this.pin = anchor ? anchor.getBoundingClientRect().top : null;
    keepInPlace(anchor, () => { slot.textContent = ""; slot.append(this.caret); }, this.pin);
    slot.setAttribute("aria-busy", "true");
  }

  set(text) {
    this.target = text.trim();
    if (reducedMotion.matches || revealSpeed() === Infinity) { this.count = this.target.length; this.render(); return; }
    if (this.frame === null) { this.last = performance.now(); this.frame = requestAnimationFrame((t) => this.tick(t)); }
  }

  tick(now) {
    const dt = Math.min(1 / 30, (now - this.last) / 1000);
    this.last = now;
    const backlog = this.target.length - this.count;
    const s = revealSpeed();
    const rate = s === Infinity ? Infinity : s < 1 ? BASE_RATE * s : Math.max(BASE_RATE, backlog / CATCH_UP) / (2 - s);
    this.count = Math.min(this.target.length, this.count + rate * dt);
    this.render();
    if (this.count < this.target.length) {
      this.frame = requestAnimationFrame((t) => this.tick(t));
    } else {
      this.frame = null;
      if (this.idle) this.idle();
    }
  }

  // Show the first (forward) or last (backward) count characters of the target.
  render() {
    const n = Math.floor(this.count);
    const want = this.backward ? this.target.slice(this.target.length - n) : this.target.slice(0, n);
    if (want === this.shown) return;
    follow(this.slot, this.backward, () => keepInPlace(this.anchor, () => this.draw(want), this.pin));
  }

  draw(want) {
    const extends_ = this.backward ? want.endsWith(this.shown) : want.startsWith(this.shown);
    if (!extends_ || reducedMotion.matches) {
      // The decoded text changed under us (or motion is off): redraw without fading.
      this.slot.textContent = "";
      this.slot.append(...(this.backward ? [this.caret, want] : [want, this.caret]));
    } else {
      const added = this.backward ? want.slice(0, want.length - this.shown.length) : want.slice(this.shown.length);
      const chunk = el("span", { class: "fresh", text: added });
      chunk.addEventListener("animationend", () => { chunk.replaceWith(chunk.textContent); this.slot.normalize(); }, { once: true });
      if (this.backward) this.caret.after(chunk); else this.caret.before(chunk);
    }
    this.shown = want;
  }

  // Resolve once everything buffered has been shown.
  drain() {
    if (this.frame === null) return Promise.resolve();
    return new Promise((resolve) => { this.idle = resolve; });
  }

  finish() {
    if (this.frame !== null) cancelAnimationFrame(this.frame);
    this.frame = null;
    this.count = this.target.length;
    this.render();
    follow(this.slot, this.backward, () => keepInPlace(this.anchor, () => { this.slot.textContent = this.target; }, this.pin)); // drops the caret and any spans still fading
    this.slot.removeAttribute("aria-busy");
  }
}

// Generated text lives in a fixed-height scroll region. Run a DOM change in a slot and keep
// the region showing the text next to the prompt (the bottom for backward, the top for
// forward), unless the reader has scrolled away from that edge.
function follow(slot, backward, mutate) {
  const region = slot.parentElement;
  if (!region.classList.contains("scroll")) { mutate(); return; }
  const fromBottom = region.scrollHeight - region.scrollTop - region.clientHeight;
  const atEdge = backward ? fromBottom < 8 : region.scrollTop < 8;
  mutate();
  if (backward) region.scrollTop = atEdge ? region.scrollHeight : region.scrollHeight - region.clientHeight - fromBottom;
  markClipped(region);
}

// Mark which edges of a scroll region have hidden text beyond them (styled as a fade).
function markClipped(region) {
  region.classList.toggle("more-up", region.scrollTop > 1);
  region.classList.toggle("more-down", region.scrollHeight - region.scrollTop - region.clientHeight > 1);
}
document.addEventListener("scroll", (e) => {
  if (e.target.classList?.contains("scroll")) markClipped(e.target);
}, true);

// When a region is resized (window resize or zoom), keep backward text pinned to the prompt
// unless the reader has scrolled away from it.
const regionSizes = new ResizeObserver((entries) => {
  for (const { target: region } of entries) {
    const fromBottom = Number(region.dataset.fromBottom || 0);
    region.scrollTop = region.scrollHeight - region.clientHeight - fromBottom;
    markClipped(region);
  }
});
for (const region of document.querySelectorAll(".scroll-up")) watchRegion(region);

function watchRegion(region) {
  region.addEventListener("scroll", () => {
    const fromBottom = region.scrollHeight - region.scrollTop - region.clientHeight;
    region.dataset.fromBottom = fromBottom < 8 ? 0 : Math.round(fromBottom);
  });
  regionSizes.observe(region);
}

// Run a DOM change without moving anchor on screen: when text grows above it, the page
// scrolls by the same amount, lengthening the page first if it is too short to scroll.
// A pin (a fixed screen position) stops sub-pixel rounding from accumulating.
function keepInPlace(anchor, mutate, pin = null) {
  if (!anchor) { mutate(); return; }
  const before = pin ?? anchor.getBoundingClientRect().top;
  mutate();
  const delta = anchor.getBoundingClientRect().top - before;
  if (Math.abs(delta) < 0.5) return;
  const need = window.scrollY + delta + window.innerHeight;
  if (delta > 0 && document.documentElement.scrollHeight < need) document.body.style.minHeight = `${Math.ceil(need)}px`;
  window.scrollBy(0, delta);
}

// Clear old output before a new run; the page keeps the given box where it is.
function clearSlots(slots) {
  document.body.style.minHeight = "";
  keepInPlace(slots.box, () => { slots.bwd.textContent = ""; slots.fwd.textContent = ""; });
  for (const slot of [slots.bwd, slots.fwd]) {
    const region = slot.parentElement;
    if (region.classList.contains("scroll")) { region.scrollTop = slot === slots.bwd ? region.scrollHeight : 0; markClipped(region); }
  }
}

// Fill the slots around a box. Backward text sits above the box, forward below it.
async function runBox(slots, directions, text, signal) {
  for (const direction of directions) {
    const backward = direction === "backward";
    const reveal = new Reveal(backward ? slots.bwd : slots.fwd, backward, null);
    try {
      await streamGenerate(direction, text, (t) => reveal.set(t), signal);
      await reveal.drain();
    } finally {
      reveal.finish();
    }
  }
}

// Run a task, reporting stops and failures on the notice line.
async function guarded(task) {
  notify();
  try {
    await exclusive(task);
  } catch (e) {
    if (e.name !== "AbortError") notify(explain(e), true);
  }
}

// ---------------------------------------------------------------------------
// Write view

const writeText = $("write-text");
const writeSlots = { bwd: $("write-bwd"), fwd: $("write-fwd"), box: $("write-box") };

function fitText() {
  writeText.style.height = "auto";
  writeText.style.height = `${writeText.scrollHeight}px`;
}
writeText.addEventListener("input", () => {
  // Edited text makes old output stale.
  if (!current) clearSlots(writeSlots);
  fitText();
});
window.addEventListener("resize", fitText);
document.fonts?.ready.then(fitText);
fitText();

function setRunning(button, on) {
  button.textContent = on ? "Stop" : "Run";
}

let writeRunning = false;

async function runWrite() {
  if (writeRunning) return;
  const text = writeText.value.trim();
  const directions = [];
  if ($("write-bwd-on").checked) directions.push("backward");
  if ($("write-fwd-on").checked) directions.push("forward");
  if (!text) { notify("Type something first."); writeText.focus(); return; }
  if (!directions.length) { notify("Select Forward or Backward."); return; }
  clearSlots(writeSlots);
  writeRunning = true;
  writeText.readOnly = true;
  setRunning($("write-go"), true);
  try {
    await guarded((signal) => runBox(writeSlots, directions, text, signal));
  } finally {
    writeRunning = false;
    writeText.readOnly = false;
    setRunning($("write-go"), false);
  }
}

$("write-go").addEventListener("click", () => {
  if (writeRunning) stopCurrent(); else runWrite();
});

// ---------------------------------------------------------------------------
// Demos view

let curatedSets = [];
let currentDemo = null;

function demoBox(given) {
  const bwd = el("p", { class: "gen gen-bwd", "aria-live": "polite" });
  const fwd = el("p", { class: "gen gen-fwd", "aria-live": "polite" });
  const box = el("div", { class: "box" }, el("p", { class: "given", text: given }));
  const above = el("div", { class: "scroll scroll-up" }, bwd);
  watchRegion(above);
  const below = el("div", { class: "scroll" }, fwd);
  return { node: el("div", { class: "run-block" }, above, box, below), slots: { bwd, fwd, box } };
}

function runDemo(demo) {
  currentDemo = demo;
  $("demo-list").querySelectorAll("button").forEach((b) => b.setAttribute("aria-current", String(b.dataset.id === demo.id)));
  const runs = demo.runs || [{ directions: ["backward", "forward"], text: demo.text }];
  const container = $("demo-runs");
  document.body.style.minHeight = "";
  container.textContent = "";
  const boxes = runs.map((run) => {
    const b = demoBox(run.text);
    container.append(b.node);
    return { run, slots: b.slots };
  });

  return guarded(async (signal) => {
    for (const { run, slots } of boxes) await runBox(slots, run.directions || [run.direction], run.text, signal);
  });
}

function renderDemoList() {
  const list = $("demo-list");
  list.textContent = "";
  for (const set of curatedSets) {
    const ul = el("ul", { "aria-label": set.title });
    for (const demo of set.demos) {
      const b = el("button", { type: "button", text: demo.title, "aria-current": String(currentDemo?.id === demo.id) });
      b.dataset.id = demo.id;
      b.addEventListener("click", () => runDemo(demo));
      ul.append(el("li", {}, b));
    }
    list.append(el("section", { class: "demo-set" }, el("h3", { class: "demo-set-title", text: set.title }), ul));
  }
}

async function loadCurated() {
  try {
    const r = await fetch(new URL("demos.json", SCRIPT_DIR), { cache: "no-store" });
    if (r.ok) curatedSets = (await r.json()).sets;
  } catch (e) { /* curated demos are optional */ }
  renderDemoList();
}

// ---------------------------------------------------------------------------
// Keyboard: Enter in the text box runs (Shift+Enter inserts a newline), Cmd/Ctrl+Enter runs
// from anywhere, Esc stops.

writeText.addEventListener("keydown", (e) => {
  if (e.key !== "Enter" || e.shiftKey || e.metaKey || e.ctrlKey || e.isComposing) return;
  e.preventDefault();
  runWrite();
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
    e.preventDefault();
    if (activeView() === "write") runWrite();
    else if (activeView() === "demos" && currentDemo) runDemo(currentDemo);
  } else if (e.key === "Escape" && drawerOpen()) {
    setDrawer(false);
    handle.focus();
  } else if (e.key === "Escape" && current) {
    stopCurrent();
  }
});

loadCurated();
checkHealth();
