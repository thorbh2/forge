import { makeReader, write, connectWallet, activeAccount, short, fmtErr }
  from "../shared/genlayer-lite.js";

const CONTRACT = "0xa36eb7430894C299393647Fe21Ed30D7C3dBB75c";
const { read } = makeReader(CONTRACT);
const COLS = [
  { key: "pitched", status: 0, title: "Pitched", cls: "col-pitched" },
  { key: "greenlit", status: 1, title: "Greenlit", cls: "col-greenlit" },
  { key: "shelved", status: 2, title: "Shelved", cls: "col-shelved" },
];
const $ = (id) => document.getElementById(id);
const esc = (s) => (s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const hostOf = (u) => { try { return new URL(u).hostname.replace(/^www\./, ""); } catch (_) { return u; } };

let account = null, ideas = [], stats = null;

function toast(msg, kind = "", title = "forge") {
  const el = document.createElement("div"); el.className = "toast " + kind;
  el.innerHTML = `<span class="tt">${title}</span>`; el.appendChild(document.createTextNode(msg));
  $("log").appendChild(el); setTimeout(() => el.remove(), kind === "err" ? 15000 : 5000);
}

async function load() {
  stats = await read("get_stats");
  const n = Number(await read("get_idea_count"));
  const out = [];
  for (let i = 0; i < n; i++) out.push({ id: i, ...(await read("get_idea", [i])) });
  ideas = out;
}

function renderStats() {
  if (!stats) return;
  $("boardStats").innerHTML = `
    <span class="bs d-amber"><b>${stats.pitched}</b> pitched</span>
    <span class="bs d-green"><b>${stats.greenlit}</b> greenlit</span>
    <span class="bs d-slate"><b>${stats.shelved}</b> shelved</span>`;
}

function scoreClass(s) { return s >= 70 ? "hi" : s >= 40 ? "mid" : "lo"; }

function card(it) {
  const reviewed = it.status !== 0;
  const scoreBadge = reviewed ? `<div class="score ${scoreClass(it.score)}">${it.score}<small>/100</small></div>` : "";
  const reason = reviewed && it.rationale ? `<div class="card-reason">${esc(it.rationale)}</div>` : "";
  const action = it.status === 0
    ? `<button class="btn line sm" data-review="${it.id}"><i class="ph-bold ph-scan"></i> Run AI review</button>`
    : `<a href="${esc(it.spec_url)}" target="_blank" rel="noopener">${esc(hostOf(it.spec_url))} ↗</a>`;
  return `<div class="card ${it.status === 2 ? "shelved" : ""}">
    <div class="card-top"><h3>${esc(it.title)}</h3>${scoreBadge}</div>
    <div class="card-pitch">${esc(it.pitch)}</div>
    ${reason}
    <div class="card-foot"><span>${short(it.author)}</span>${action}</div>
  </div>`;
}

function render() {
  renderStats();
  $("board").innerHTML = COLS.map((c) => {
    const items = ideas.filter((i) => i.status === c.status);
    const body = items.length
      ? items.slice().reverse().map(card).join("")
      : `<div class="col-empty">Nothing here yet.</div>`;
    return `<section class="column ${c.cls}">
      <div class="col-head"><span class="col-dot"></span><span class="col-title">${c.title}</span><span class="col-count">${items.length}</span></div>
      <div class="col-body">${body}</div>
    </section>`;
  }).join("");
  $("board").querySelectorAll("[data-review]").forEach((b) => b.onclick = () => doReview(Number(b.dataset.review)));
}

/* drawer */
function openDrawer() { $("scrim").hidden = false; $("drawer").setAttribute("aria-hidden", "false"); }
function closeDrawer() { $("scrim").hidden = true; $("drawer").setAttribute("aria-hidden", "true"); }
$("pitchBtn").onclick = openDrawer;
$("drawerX").onclick = closeDrawer;
$("scrim").onclick = closeDrawer;

/* actions */
async function doReview(id) {
  if (!confirm("Run the AI review? Validators read the spec and score it, then move the card. Calls a real LLM consensus.")) return;
  const btn = document.querySelector(`[data-review="${id}"]`); if (btn) { btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> reviewing'; }
  try { await ensureWallet(); toast("Validators reading the spec…", "", "review"); await write(CONTRACT, "review", [id]); toast("Reviewed - card moved.", "ok"); await load(); render(); }
  catch (e) { toast(fmtErr(e), "err"); if (btn) { btn.disabled = false; btn.innerHTML = "Run AI review"; } }
}
async function doPitch() {
  const title = $("pTitle").value.trim(), pitch = $("pPitch").value.trim(), url = $("pUrl").value.trim();
  if (!title) return toast("Give it a title.", "err");
  if (!pitch) return toast("Write the pitch.", "err");
  if (!url) return toast("Add a spec URL.", "err");
  const btn = $("pitchSubmit"); btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> forging';
  try {
    await ensureWallet();
    await write(CONTRACT, "pitch", [title, pitch, url]);
    toast("Added to the forge.", "ok");
    $("pTitle").value = $("pPitch").value = $("pUrl").value = "";
    closeDrawer(); await load(); render();
  } catch (e) { toast(fmtErr(e), "err"); btn.disabled = false; btn.innerHTML = "Add to the forge"; }
}
$("pitchSubmit").onclick = doPitch;

/* wallet */
async function refreshWallet() {
  account = await activeAccount();
  const slot = $("walletslot");
  if (account) slot.innerHTML = `<span class="btn ghost" style="cursor:default"><i class="ph-fill ph-circle" style="color:var(--green);font-size:8px"></i> ${short(account)}</span>`;
  else { slot.innerHTML = `<button class="btn ghost" id="connectBtn"><i class="ph-bold ph-wallet"></i> Connect</button>`; $("connectBtn").onclick = doConnect; }
}
async function doConnect() { try { account = await connectWallet(); toast("Connected on studionet.", "ok"); await refreshWallet(); } catch (e) { toast(fmtErr(e), "err"); } }
async function ensureWallet() { if (!account) account = await connectWallet(); await refreshWallet(); }

const _cb = $("connectBtn"); if (_cb) _cb.onclick = doConnect;
if (window.ethereum) window.ethereum.on?.("accountsChanged", refreshWallet);

(async () => {
  await refreshWallet();
  try { await load(); render(); } catch (e) { $("board").innerHTML = `<div class="board-loading">Could not reach the chain. ${fmtErr(e)}</div>`; }
})();
