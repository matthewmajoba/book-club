// Book Club front end (built from Game Club's).
// Safety rule for this file: user-written text is only ever inserted with textContent
// (through h()), never as HTML, so nobody can inject scripts into the page.
import { createClient } from "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/+esm";
import { SUPABASE_URL, SUPABASE_ANON_KEY } from "./config.js";
import { initPep } from "./pep.js";

const sb = createClient(SUPABASE_URL, SUPABASE_ANON_KEY, { auth: { persistSession: false } });
const FN_URL = `${SUPABASE_URL}/functions/v1/books`;
const MAX_LEN = 500, WARN_AT = 450;

// ---------- constants ----------
// font -> size multiplier so every name looks about the same size
const FONTS = {
  "Lobster": 1, "Special Elite": 0.86, "IM Fell English SC": 0.95, "UnifrakturMaguntia": 1.05, "Henny Penny": 0.92,
  "Fredericka the Great": 0.98, "Homemade Apple": 0.8, "Amatic SC": 1.3, "Mountains of Christmas": 1.08, "Creepster": 1.05,
};
const PALETTE = [
  ["Cranberry", "#ff6b6b"], ["Pumpkin", "#ff9f43"], ["Butterscotch", "#ffd166"], ["Pear", "#c5e063"],
  ["Sage", "#7bd88f"], ["Sea Glass", "#4fd1c5"], ["Rainy Sky", "#6ec6ff"], ["Cornflower", "#8fa8ff"],
  ["Lavender", "#b99cff"], ["Orchid", "#e58cff"], ["Rose", "#ff8fb8"], ["Peach", "#ffb38a"],
  ["Parchment", "#f4e1b0"], ["Cocoa", "#d9b38c"],
];
const TIERS = [
  { k: "DUSTY", a: "🕸️", b: "💤" },
  { k: "SKIMMING", a: "😐", b: "📄" },
  { k: "INTRIGUED", a: "🤔", b: "👀" },
  { k: "PAGE TURNER", a: "😍", b: "📖" },
  { k: "CAN'T PUT IT DOWN", a: "🤩", b: "📚" },
];
const TILTS = ["-2deg", "1.5deg", "-1deg", "2deg", "-1.5deg", "1deg"];

// ---------- state ----------
const store = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { v == null ? localStorage.removeItem(k) : localStorage.setItem(k, v); } catch { /* private mode */ } },
};
const S = {
  token: store.get("bc_token"), me: null, members: [], round: null, books: [], votes: [], read: [],
  messages: [], facts: [], chatOn: store.get("bc_chat_on") !== "0", here: new Set(), hereReady: false,
  unread: 0, tab: "shelf", openBookId: null, logOpen: false,
};

// ---------- tiny DOM helper (text is always text) ----------
function h(tag, attrs, ...kids) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k === "class") e.className = v;
    else if (k === "vars") for (const [n, val] of Object.entries(v)) e.style.setProperty(n, val);
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else if (k in e && typeof v !== "string") e[k] = v;
    else e.setAttribute(k, v === true ? "" : v);
  }
  for (const c of kids.flat(Infinity)) if (c != null && c !== false) e.append(c instanceof Node ? c : String(c));
  return e;
}
const $ = (id) => document.getElementById(id);
const member = (id) => S.members.find((m) => m.id === id);
const fmtTime = (t) => new Date(t).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
const fmtDay = (t) => new Date(t).toLocaleDateString([], { month: "short", day: "numeric" });

// If a name we don't know shows up (member list still loading or out of date),
// reload the member list instead of ever showing a placeholder name.
let membersReloading = null;
function reloadMembersSoon() {
  if (!membersReloading) membersReloading = loadMembers().then(renderAll).finally(() => { membersReloading = null; });
}
function nameEl(m, cls = "nm") {
  if (!m) { reloadMembersSoon(); return h("span", { class: cls }, "…"); }
  return h("span", { class: cls, vars: { "--mc": m.color || "#fff", "--mf": m.font ? `'${m.font}'` : "var(--ui)", "--fs": String(FONTS[m.font] || 0.85) } }, m.name);
}
const flip = (t) => h("span", { class: "flip" }, h("b", null, t.a), h("b", null, t.b));

function toast(msg, bad = false) {
  const t = h("div", { class: "toast" + (bad ? " bad" : ""), role: "status" }, msg);
  document.body.append(t);
  setTimeout(() => t.remove(), bad ? 4200 : 2600);
}
const errMsg = (e) => (e && (e.message || e.error)) || "Something went wrong.";

// char counter that only shows up near the limit
function withCounter(textarea) {
  const cnt = h("span", { class: "cnt", hidden: true });
  const upd = () => {
    const n = textarea.value.length;
    cnt.hidden = n < WARN_AT;
    cnt.textContent = `${MAX_LEN - n} left`;
  };
  textarea.maxLength = MAX_LEN;
  textarea.addEventListener("input", upd);
  return h("div", { class: "field" }, textarea, cnt);
}

// ---------- sounds (synthesized, no files) ----------
let ac = null;
function audio() {
  try {
    if (!ac) ac = new (window.AudioContext || window.webkitAudioContext)();
    if (ac.state === "suspended") ac.resume();
  } catch { ac = null; }
  return ac;
}
document.addEventListener("pointerdown", audio, { once: true });
function noise(a, t, dur, freq, gain) {
  const buf = a.createBuffer(1, Math.floor(a.sampleRate * dur), a.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length);
  const src = a.createBufferSource(); src.buffer = buf;
  const f = a.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = freq;
  const g = a.createGain(); g.gain.value = gain;
  src.connect(f).connect(g).connect(a.destination); src.start(t);
}
// someone walks in: a little shop bell over the door
function doorOpen() {
  const a = ac; if (!a || a.state !== "running") return;
  const t = a.currentTime;
  [[2093, 0], [2637, 0.07], [2093, 0.16], [2637, 0.23]].forEach(([fr, dt]) => {
    const o = a.createOscillator(); o.type = "sine"; o.frequency.value = fr;
    const o2 = a.createOscillator(); o2.type = "sine"; o2.frequency.value = fr * 2.76;
    const g = a.createGain(); g.gain.setValueAtTime(0, t + dt); g.gain.linearRampToValueAtTime(0.09, t + dt + 0.005); g.gain.exponentialRampToValueAtTime(0.001, t + dt + 0.9);
    const g2 = a.createGain(); g2.gain.value = 0.25;
    o.connect(g); o2.connect(g2).connect(g); g.connect(a.destination);
    o.start(t + dt); o2.start(t + dt); o.stop(t + dt + 1); o2.stop(t + dt + 1);
  });
}
// someone leaves: the door thumps shut
function doorClose() {
  const a = ac; if (!a || a.state !== "running") return;
  const t = a.currentTime;
  const o = a.createOscillator(); o.type = "sine";
  o.frequency.setValueAtTime(140, t); o.frequency.exponentialRampToValueAtTime(45, t + 0.25);
  const g = a.createGain(); g.gain.setValueAtTime(0.5, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.35);
  o.connect(g).connect(a.destination); o.start(t); o.stop(t + 0.4);
  noise(a, t, 0.12, 900, 0.35);
}
function blip(freq, at) {
  const a = audio(); if (!a) return;
  const t = a.currentTime + at;
  const o = a.createOscillator(); o.type = "triangle"; o.frequency.setValueAtTime(freq, t);
  const g = a.createGain(); g.gain.setValueAtTime(0.12, t); g.gain.exponentialRampToValueAtTime(0.001, t + 0.35);
  o.connect(g).connect(a.destination); o.start(t); o.stop(t + 0.36);
}

// ---------- data ----------
async function rpc(fn, args) {
  const { data, error } = await sb.rpc(fn, args);
  if (error) throw error;
  return data;
}
async function callFn(body) {
  const r = await fetch(FN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json", apikey: SUPABASE_ANON_KEY, Authorization: `Bearer ${SUPABASE_ANON_KEY}` },
    body: JSON.stringify(body),
  });
  const d = await r.json().catch(() => ({ error: "The server didn't answer properly." }));
  if (!r.ok || d.error) throw new Error(d.error || "Something went wrong.");
  return d;
}

async function loadMembers() {
  const { data } = await sb.from("members").select("*").order("name");
  S.members = data || [];
  if (S.me) S.me = member(S.me.id) || S.me;
}
async function loadShelf() {
  const { data: r } = await sb.from("rounds").select("*").eq("status", "open").maybeSingle();
  S.round = r;
  const [b, v, read] = await Promise.all([
    r ? sb.from("books").select("*").eq("round_id", r.id).order("created_at") : { data: [] },
    r ? sb.from("votes").select("*").eq("round_id", r.id) : { data: [] },
    sb.from("books").select("*").eq("status", "won").order("ended_at", { ascending: false }),
  ]);
  S.books = b.data || []; S.votes = v.data || []; S.read = read.data || [];
}
async function loadMessages() {
  const { data } = await sb.from("messages").select("*").order("created_at", { ascending: false }).limit(120);
  S.messages = (data || []).reverse();
}
async function loadFacts() {
  const { data } = await sb.from("facts").select("body");
  S.facts = (data || []).map((f) => f.body);
}
async function checkSession() {
  if (!S.token) return;
  try {
    const m = await rpc("me", { p_token: S.token });
    if (m) S.me = m; else { S.token = null; store.set("bc_token", null); }
  } catch { /* offline: keep token, try later */ }
}

// ---------- bookmark math ----------
function marks() {
  const per = new Map();
  for (const v of S.votes) per.set(v.book_id, (per.get(v.book_id) || 0) + v.points);
  const total = S.books.filter((b) => b.status === "active").reduce((a, b) => a + (per.get(b.id) || 0), 0);
  return { per, total };
}
function tierOf(n, total) {
  if (!n) return 0;
  const p = n / total;
  return p < 0.1 ? 1 : p < 0.2 ? 2 : p < 0.3 ? 3 : 4;
}
const myVotes = () => (S.me ? S.votes.filter((v) => v.member_id === S.me.id) : []);
const myUsed = () => myVotes().reduce((a, v) => a + v.points, 0);
const livePick = (memberId) => S.books.find((b) => b.member_id === memberId && (b.status === "active" || b.status === "pending"));
const maxPages = () => Number(S.round?.max_pages || 150);

// ---------- render: header ----------
function renderNav() {
  const nav = $("nav");
  const items = [
    h("button", { type: "button", class: "btn blue", onclick: openLog }, "📜 Log"),
    h("button", { type: "button", class: "btn", onclick: openRead }, "📚 Books We've Read"),
    h("button", { type: "button", class: "btn pink", onclick: openLoveNotes }, "🔮 Crystal Ball of Encouragement and Love"),
    h("button", { type: "button", class: "btn", onclick: openRules }, "Rules"),
  ];
  if (S.me?.is_admin) items.push(h("button", { type: "button", class: "btn pink", onclick: openAdmin }, "⚙ Admin"));
  items.push(S.me
    ? h("button", { type: "button", class: "btn", onclick: signOut }, "Sign out (", S.me.name, ")")
    : h("button", { type: "button", class: "btn on", onclick: openLogin }, "Sign in"));
  nav.replaceChildren(...items);
  $("round-badge").textContent = `Under ${maxPages()} pages`;
}

function renderTicker() {
  const el = $("facts");
  // shuffle so every visit starts on different facts; 30 at a time keeps the loop a sane length
  const pool = S.facts.slice();
  for (let i = pool.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; }
  const list = pool.length ? pool.slice(0, 30) : ["Welcome to Book Club!"];
  el.replaceChildren(...list.flatMap((f, i) => (i ? [h("em", null, "❦"), f] : [f])));
  requestAnimationFrame(() => { el.style.animationDuration = Math.max(60, el.scrollWidth / 38) + "s"; });
  // every time the ticker finishes a pass, deal a fresh random batch
  if (!el.dataset.reshuffles) { el.dataset.reshuffles = "1"; el.addEventListener("animationiteration", renderTicker); }
}

// ---------- render: shelf ----------
function renderBudget() {
  const b = $("budget");
  if (!S.me) {
    b.replaceChildren(h("span", null, "You get 3 🔖 bookmarks to vote with once you sign in."),
      h("button", { type: "button", class: "btn", onclick: openLogin }, "Sign in"));
    return;
  }
  const used = myUsed(), left = Math.max(0, 3 - used);
  b.replaceChildren(
    h("span", null, "Your bookmarks: ", h("span", { class: "tok" }, "🔖".repeat(left), h("s", null, "🔖".repeat(3 - left))), " ", h("b", null, `${left} left`)));
}

// a cloth-bound "cover" for books without a picture
const plainCover = (b) => h("div", { class: "marker" }, h("b", null, b.title), b.author ? h("small", null, b.author) : null);
function coverImg(b) {
  const img = h("img", { src: b.cover_url, alt: `Cover of ${b.title}`, loading: "lazy" });
  img.addEventListener("error", () => img.replaceWith(plainCover(b)));
  return img;
}
function caseEl(b, { sticker = true, tier = 0, mine = 0 } = {}) {
  const c = h("div", { class: "case" }, b.cover_url ? coverImg(b) : plainCover(b));
  if (b.status === "pending") c.append(h("span", { class: "waiting" }, "Page check"));
  else if (sticker) c.append(h("span", { class: `sticker t${tier}`, title: TIERS[tier].k }, flip(TIERS[tier])));
  if (mine) c.append(h("span", { class: "mine" + (mine === 1 ? " one" : "") }, mine === 2 ? "your big vote ×2" : "your 🔖"));
  return c;
}

function renderShelf() {
  renderBudget();
  const { per, total } = marks();
  const live = S.books.filter((b) => b.status === "active" || b.status === "pending");
  const mine = new Map(myVotes().map((v) => [v.book_id, v.points]));
  const cells = live.map((b, i) => {
    const m = member(b.member_id), n = per.get(b.id) || 0, ti = tierOf(n, total);
    const pct = total ? Math.round((n / total) * 100) : 0;
    return h("button", { type: "button", class: "cell", vars: { "--mc": m?.color || "#ccc" }, onclick: () => openBook(b.id), "aria-label": `${b.title}, picked by ${m?.name}` },
      caseEl(b, { tier: ti, mine: mine.get(b.id) || 0 }),
      h("div", { class: "edge" }),
      h("div", { class: "talker", vars: { "--r": TILTS[i % TILTS.length] } },
        h("div", { class: "hd" }, "★ CLUB PICK ★"),
        h("span", { class: "who" }, m?.name || "?"),
        h("span", { class: "say" }, b.title),
        h("div", { class: "bc" }, h("span", null, b.pages ? `${b.pages} PGS` : "? PGS"), h("span", null, b.status === "pending" ? "WAITING" : `🔖${n} · ${pct}%`))));
  });
  const open = S.members.filter((m) => !livePick(m.id));
  open.sort((a, b) => (S.me && a.id === S.me.id ? -1 : S.me && b.id === S.me.id ? 1 : 0));
  for (const m of open) {
    const isMe = S.me && m.id === S.me.id;
    cells.push(h(isMe ? "button" : "div", { type: isMe ? "button" : null, class: "cell" + (isMe ? " you" : " open-slot"), onclick: isMe ? openAdd : null },
      h("div", { class: "case blank" }, isMe ? `+ ${m.name}, shelve yours!` : `${m.name}'s spot`),
      h("div", { class: "edge" })));
  }
  $("shelf").replaceChildren(...cells);

  // book drop: only this shelf's early returns (it empties when a winner is crowned),
  // newest first, capped so it never takes over the page; the rest live in the Log
  const DROP_MAX = 6;
  const out = S.books.filter((b) => b.status === "withdrawn").reverse();
  const extra = out.length - DROP_MAX;
  $("bin").replaceChildren(h("span", { class: "lbl" }, "BOOK DROP"),
    ...(out.length ? out.slice(0, DROP_MAX).map((b, i) => h("div", { class: "scrap", vars: { "--r": i % 2 ? "4deg" : "-5deg" } }, `${member(b.member_id)?.name}: ${b.title}`))
      : [h("span", { class: "none" }, "nobody has returned theirs early... yet 👀")]),
    ...(extra > 0 ? [h("button", { type: "button", class: "more", onclick: openLog }, `+${extra} more in the Log`)] : []));
}

// ---------- render: chat ----------
function renderChatMenu() {
  const menu = $("chat-menu");
  if (!S.me) { menu.replaceChildren(h("span", null, "Just looking 👀")); return; }
  menu.replaceChildren(
    h("span", null, "You: ", h("b", null, S.me.name)),
    h("button", { type: "button", class: "lnk", onclick: toggleChatOn, vars: { "margin-left": "auto" } }, S.chatOn ? "🚪 Sign Off" : "🚪 Sign On"));
}
function renderHere() {
  const ids = [...S.here];
  $("here").replaceChildren(h("span", { class: "lbl" }, `here now (${ids.length}/${S.members.length || 10}):`),
    ...(ids.length ? ids.map((id) => nameEl(member(id))) : [h("span", { class: "lbl" }, "nobody... 🦗")]));
}
function msgEl(m) {
  const ts = h("span", { class: "ts" }, `(${fmtTime(m.created_at)})`);
  if (m.kind !== "chat") return h("p", { class: "sys" }, ts, m.body);
  const who = member(m.member_id);
  if (!who) { reloadMembersSoon(); return null; } // show it once we know who wrote it
  return h("p", null, ts, nameEl(who), h("span", { class: "msg" }, ": ", m.body));
}
function renderChat() {
  const log = $("chatlog");
  const nearBottom = log.scrollHeight - log.scrollTop - log.clientHeight < 80;
  log.replaceChildren(...S.messages.map(msgEl).filter(Boolean));
  if (nearBottom || !log.dataset.ready) { log.scrollTop = log.scrollHeight; log.dataset.ready = "1"; }
}
function renderSend() {
  const box = $("chat-send");
  if (!S.me) {
    box.replaceChildren(h("div", { class: "chat-note" }, "Members only in here. ", h("button", { type: "button", class: "btn", onclick: openLogin }, "Sign in to chat")));
    return;
  }
  if (!S.chatOn) {
    box.replaceChildren(h("div", { class: "chat-note" }, "You're signed off. ", h("button", { type: "button", class: "btn", onclick: toggleChatOn }, "🚪 Sign on")));
    return;
  }
  const ta = h("textarea", { id: "chat-input", rows: 2, placeholder: "type a message..." });
  const send = async () => {
    const body = ta.value.trim();
    if (!body) return;
    ta.disabled = true;
    try { await rpc("send_message", { p_token: S.token, p_body: body }); ta.value = ""; ta.dispatchEvent(new Event("input")); }
    catch (e) { toast(errMsg(e), true); }
    ta.disabled = false; ta.focus();
  };
  ta.addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } });
  box.replaceChildren(h("div", { class: "send" }, withCounter(ta), h("button", { type: "button", class: "go", onclick: send }, "Send")));
}

function renderAll() {
  renderNav(); renderShelf(); renderChatMenu(); renderHere(); renderChat(); renderSend();
  if (S.openBookId) refreshBookDialog();
}

// ---------- dialogs ----------
function dialog(title, { wide = false } = {}) {
  closeDialog();
  const body = h("div", { class: "body" });
  const win = h("div", { class: "win dlg" + (wide ? " wide" : ""), role: "dialog", "aria-modal": "true", "aria-label": title },
    h("div", { class: "tbar" }, h("span", { class: "ico" }, "❦"), h("span", { class: "t" }, title),
      h("button", { type: "button", class: "wb x", "aria-label": "Close", onclick: closeDialog }, "x")),
    body);
  const ov = h("div", { class: "overlay", onclick: (e) => { if (e.target === ov) closeDialog(); } }, win);
  $("layer").replaceChildren(ov);
  return body;
}
function closeDialog() {
  $("layer").replaceChildren();
  S.openBookId = null; S.logOpen = false;
}
document.addEventListener("keydown", (e) => { if (e.key === "Escape" && $("layer").firstChild) closeDialog(); });

// sign in: pick name -> "tell me something only I would know" -> code
function openLogin() {
  const body = dialog("Sign in to Book Club");
  body.append(h("h3", null, "Who are you?"),
    h("div", { class: "who-grid" }, S.members.slice().sort((a, b) => a.name.localeCompare(b.name)).map((m) =>
      h("button", { type: "button", class: "pick", onclick: () => askSecret(m) }, nameEl(m)))));
}
function askSecret(m) {
  const body = dialog(`Prove it, ${m.name}`);
  const inp = h("input", { type: "text", id: "secret", autocomplete: "off", autocapitalize: "off", spellcheck: false, placeholder: "type it here...", maxLength: 60 });
  const err = h("div", { class: "err", role: "alert" });
  const go = async () => {
    err.textContent = "";
    try {
      const r = await rpc("login", { p_name: m.name, p_code: inp.value });
      if (!r.ok) { err.textContent = r.error; inp.select(); return; }
      S.token = r.token; store.set("bc_token", r.token); S.me = r.member;
      await loadMembers();
      closeDialog(); audio();
      if (!S.me.setup_done) openSetup(); else toast(`Welcome back, ${S.me.name}!`);
      afterAuthChange();
    } catch (e) { err.textContent = errMsg(e); }
  };
  inp.addEventListener("keydown", (e) => { if (e.key === "Enter") go(); });
  body.append(
    h("p", { class: "q" }, "If you're really ", nameEl(m), ", tell me something only I would know..."),
    inp, err,
    h("div", { class: "row" }, h("button", { type: "button", class: "btn big", onclick: go }, "It's really me"),
      h("button", { type: "button", class: "btn", onclick: openLogin }, "That's not me")),
    h("small", null, "(Hint: it's your two secret words. Same ones as Game Club.)"));
  setTimeout(() => inp.focus(), 30);
}

// first sign-in: color + font
function openSetup() {
  const body = dialog("Make it yours", { wide: true });
  let color = S.me.color, font = S.me.font || "Lobster";
  const preview = h("div", { class: "preview" });
  const err = h("div", { class: "err", role: "alert" });
  const sw = h("div", { class: "sw" }), fonts = h("div", { class: "fonts" });
  const draw = () => {
    const taken = new Map(S.members.filter((m) => m.color && m.id !== S.me.id).map((m) => [m.color, m.name]));
    sw.replaceChildren(...PALETTE.map(([n, c]) => h("button", {
      type: "button", class: c === color ? "sel" : "", disabled: taken.has(c), vars: { "--c": c },
      onclick: () => { color = c; draw(); }, title: taken.has(c) ? `${taken.get(c)}'s color` : n,
    }, h("i"), taken.has(c) ? `${taken.get(c)}'s` : n)));
    fonts.replaceChildren(...Object.keys(FONTS).map((f) => h("button", { type: "button", class: f === font ? "sel" : "", onclick: () => { font = f; draw(); } },
      nameEl({ name: S.me.name, color: color || "#ff8fb8", font: f }), h("small", null, f))));
    preview.replaceChildren(nameEl({ name: S.me.name, color: color || "#fff", font }), h("span", null, "has curled up with a book. ☕️"));
  };
  draw();
  const save = async () => {
    err.textContent = "";
    if (!color) { err.textContent = "Pick a color first."; return; }
    try {
      S.me = await rpc("setup_profile", { p_token: S.token, p_color: color, p_font: font });
      await loadMembers(); closeDialog(); renderAll(); toast("Lookin' cozy! ☕️");
    } catch (e) { err.textContent = errMsg(e); await loadMembers(); draw(); }
  };
  body.append(h("h3", null, "Pick your color (first come, first served)"), sw,
    h("h3", null, "Pick your font"), fonts,
    h("h3", null, "Lookin' good?"), preview, err,
    h("div", { class: "row" }, h("button", { type: "button", class: "btn big", onclick: save }, "Enter Book Club")));
}

// add a book: search Open Library -> check pages -> put it on the shelf
function openAdd() {
  if (!S.me) return openLogin();
  if (livePick(S.me.id)) return toast("You already have a book on the shelf. Return it first (late fee!).", true);
  const body = dialog("Put a book on the shelf", { wide: true });
  const q = h("input", { type: "search", placeholder: "search books, novellas, short stories... (e.g. The Little Prince)", autocomplete: "off", maxLength: 80 });
  const results = h("div", { class: "results" });
  const detail = h("div");
  let timer = null, picked = null, seq = 0;
  const thumb = (r) => r.thumb ? h("img", { src: r.thumb, alt: "", loading: "lazy", onerror: (e) => e.target.replaceWith(h("span", { class: "nothumb" }, "📕")) }) : h("span", { class: "nothumb" }, "📕");
  const search = async () => {
    const term = q.value.trim(), my = ++seq;
    if (term.length < 2) { results.replaceChildren(); return; }
    results.replaceChildren(h("span", null, "searching the stacks..."));
    try {
      const d = await callFn({ action: "search", q: term });
      if (my !== seq) return;
      results.replaceChildren(...(d.results.length ? d.results.map((r) => h("button", { type: "button", onclick: (e) => choose(r, e.currentTarget) },
        thumb(r), h("span", null, h("b", null, r.title), h("small", null, [r.author, r.year, r.pages ? `${r.pages} pages` : null].filter(Boolean).join(" · ")))))
        : [h("span", null, "Couldn't find that one. Short stories often hide inside collections, so try the can't-find-it option below.")]));
    } catch (e) { results.replaceChildren(h("span", { class: "err" }, errMsg(e))); }
  };
  const choose = async (r, btn) => {
    picked = r;
    results.querySelectorAll("button").forEach((b) => b.classList.toggle("sel", b === btn));
    detail.replaceChildren(h("span", null, "Counting the pages..."));
    try {
      const d = await callFn({ action: "info", key: r.key });
      if (picked !== r) return;
      const v = d.verdict;
      const add = h("button", { type: "button", class: "btn big", disabled: !v.ok }, v.kind === "nodata" ? "Send it for a page check" : "Put it on the shelf!");
      add.addEventListener("click", async () => {
        add.disabled = true;
        try {
          const res = await callFn({ action: "add", token: S.token, key: r.key });
          closeDialog(); await refreshShelf();
          if (res.book?.status === "active") celebrate(); else toast("Sent! It goes on the shelf once the pages get counted.");
        } catch (e) { toast(errMsg(e), true); add.disabled = false; }
      });
      const fake = { title: r.title, author: r.author };
      detail.replaceChildren(h("div", { class: "book-top" },
        h("div", { class: "case" }, r.cover ? h("img", { src: r.cover, alt: `Cover of ${r.title}`, onerror: (e) => e.target.replaceWith(plainCover(fake)) }) : plainCover(fake)),
        h("div", { class: "facts" }, h("h3", null, r.title), r.author ? h("div", null, "by ", r.author) : null, h("div", { class: "verdict " + v.kind }, v.msg), add)));
    } catch (e) { detail.replaceChildren(h("span", { class: "err" }, errMsg(e))); }
  };
  q.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(search, 350); });

  const manual = h("input", { type: "text", placeholder: "book title", maxLength: 200 });
  const manualBy = h("input", { type: "text", placeholder: "author (optional)", maxLength: 200 });
  const manualBtn = h("button", { type: "button", class: "btn" }, "Send it for a check");
  manualBtn.addEventListener("click", async () => {
    if (!manual.value.trim()) return toast("Type the book's title first.", true);
    manualBtn.disabled = true;
    try { await callFn({ action: "add_manual", token: S.token, title: manual.value, author: manualBy.value }); closeDialog(); await refreshShelf(); toast("Sent! It goes on the shelf once the pages get counted."); }
    catch (e) { toast(errMsg(e), true); manualBtn.disabled = false; }
  });
  body.append(h("h3", null, `Rule: a book, novella or short story under ${maxPages()} pages`), q, results, detail,
    h("details", null, h("summary", null, "Can't find it?"),
      h("div", { class: "manual" }, manual, manualBy, manualBtn),
      h("small", null, "The pages get counted by hand before it goes on the shelf.")));
  setTimeout(() => q.focus(), 30);
}

// one book: details, voting, notes, return early, admin tools
function openBook(id) {
  dialog("Book", { wide: true });
  S.openBookId = id; // set after dialog(), which clears it
  refreshBookDialog();
}
async function refreshBookDialog() {
  const b = S.books.find((x) => x.id === S.openBookId) || S.read.find((x) => x.id === S.openBookId);
  const win = $("layer").querySelector(".dlg");
  if (!b || !win) return;
  const id = b.id;
  win.querySelector(".tbar .t").textContent = b.title;
  const body = win.querySelector(".body");
  const draftEl = body.querySelector("#note-input");
  const draft = draftEl ? draftEl.value : "";
  const { per, total } = marks();
  const n = per.get(b.id) || 0, ti = tierOf(n, total), pct = total ? Math.round((n / total) * 100) : 0;
  const picker = member(b.member_id);
  const mineNow = myVotes().find((v) => v.book_id === b.id)?.points || 0;
  const usedElsewhere = myUsed() - mineNow;

  const top = h("div", { class: "book-top" }, caseEl(b, { sticker: b.status === "active", tier: ti }),
    h("div", { class: "facts" },
      b.author ? h("div", null, h("b", null, "By: "), b.author) : null,
      h("div", null, "Picked by ", nameEl(picker)),
      h("div", null, h("b", null, "Length: "), b.pages ? `about ${b.pages} pages${b.pages_source === "admin" ? " (counted by hand)" : ""}` : "unknown (needs a page check)"),
      b.status === "active" ? h("div", null, h("b", null, "Bookmarks: "), `${n} 🔖 · ${pct}% of all the bookmarks · `, h("span", { class: `t${ti}` }, flip(TIERS[ti])), " ", TIERS[ti].k) : null,
      b.status === "won" ? h("div", { class: "ok" }, "📚 WE READ THIS ONE") : null,
      b.ol_key ? h("a", { href: `https://openlibrary.org${b.ol_key}`, target: "_blank", rel: "noopener" }, "See it on Open Library ↗") : null));

  const parts = [top];
  const voters = S.votes.filter((v) => v.book_id === b.id);
  if (voters.length) parts.push(h("div", { class: "voters" }, h("b", null, "Who's into it:"), voters.map((v) => h("span", null, nameEl(member(v.member_id)), " ", "🔖".repeat(v.points)))));

  if (S.me && b.status === "active") {
    // tap to put a bookmark in, tap the lit one again to take it back out
    const opts = [[1, "🔖"], [2, "🔖🔖 big vote"]];
    parts.push(h("div", null, h("h3", null, `Your vote (${3 - myUsed()} 🔖 left)`),
      h("div", { class: "votebar" }, opts.map(([p, label]) => h("button", {
        type: "button", class: "btn" + (mineNow === p ? " on" : ""), "aria-pressed": String(mineNow === p),
        disabled: mineNow !== p && usedElsewhere + p > 3,
        onclick: async () => {
          try { await rpc("set_vote", { p_token: S.token, p_book_id: id, p_points: mineNow === p ? 0 : p }); await refreshShelf(); }
          catch (e) { toast(errMsg(e), true); }
        },
      }, label)))));
  } else if (!S.me && b.status === "active") {
    parts.push(h("button", { type: "button", class: "btn", onclick: openLogin }, "Sign in to vote"));
  }

  if (S.me && b.member_id === S.me.id && (b.status === "active" || b.status === "pending")) {
    const box = h("div");
    const ask = () => box.replaceChildren(h("div", { class: "confirm" }, h("b", null, "Return it early? You'll get +1 late fee and everyone will know. 📕"),
      h("div", { class: "row" }, h("button", { type: "button", class: "btn red", onclick: async () => {
        try { await rpc("withdraw_book", { p_token: S.token }); closeDialog(); await Promise.all([refreshShelf(), loadMembers()]); renderAll(); tsk(); }
        catch (e) { toast(errMsg(e), true); }
      } }, "Yes, return it"), h("button", { type: "button", class: "btn", onclick: () => box.replaceChildren(btn) }, "Never mind"))));
    const btn = h("button", { type: "button", class: "btn red", onclick: ask }, "Return my pick early");
    box.append(btn); parts.push(box);
  }

  if (S.me?.is_admin && (b.status === "pending" || b.status === "active")) {
    const pgs = h("input", { type: "number", min: "1", step: "1", placeholder: "pages", vars: { width: "100px" } });
    const adminRow = h("div", { class: "row" });
    if (b.status === "pending") adminRow.append(h("span", null, "Pages:"), pgs, h("button", { type: "button", class: "btn", onclick: async () => {
      try { await rpc("approve_book", { p_token: S.token, p_book_id: id, p_pages: Math.round(Number(pgs.value)) }); await refreshShelf(); toast("Done."); }
      catch (e) { toast(errMsg(e), true); }
    } }, "Approve"));
    adminRow.append(h("button", { type: "button", class: "btn red", onclick: async () => {
      try { await rpc("pull_book", { p_token: S.token, p_book_id: id }); closeDialog(); await refreshShelf(); toast("Taken off the shelf."); }
      catch (e) { toast(errMsg(e), true); }
    } }, "Take it off the shelf"));
    parts.push(h("div", { class: "confirm" }, h("b", null, "Admin"), adminRow));
  }

  const notesBox = h("div", { class: "notes glit" }, h("span", { class: "none" }, "loading notes..."));
  parts.push(h("h3", null, "Notes"), notesBox);
  if (S.me) {
    const ta = h("textarea", { id: "note-input", rows: 2, placeholder: "what do you think about this one?" });
    ta.value = draft;
    const post = h("button", { type: "button", class: "btn", onclick: async () => {
      if (!ta.value.trim()) return;
      post.disabled = true;
      try { await rpc("add_note", { p_token: S.token, p_book_id: id, p_body: ta.value }); ta.value = ""; ta.dispatchEvent(new Event("input")); await loadNotes(id, notesBox); }
      catch (e) { toast(errMsg(e), true); }
      post.disabled = false;
    } }, "Post note");
    parts.push(h("div", { class: "row" }, withCounter(ta), post));
    setTimeout(() => ta.dispatchEvent(new Event("input")));
  }
  body.replaceChildren(...parts);
  loadNotes(id, notesBox);
}
async function loadNotes(bookId, box) {
  const { data } = await sb.from("notes").select("*").eq("book_id", bookId).order("created_at");
  if (S.openBookId !== bookId) return;
  box.replaceChildren(...(data?.length ? data.map((n) => h("p", null, h("span", { class: "ts" }, `${fmtDay(n.created_at)} ${fmtTime(n.created_at)} `), nameEl(member(n.member_id)), ": ", n.body))
    : [h("span", { class: "none" }, "no notes yet. say something!")]));
  box.scrollTop = box.scrollHeight;
}

async function openLog() {
  const body = dialog("The Log", { wide: true });
  S.logOpen = true;
  const list = h("div", { class: "loglist glit" }, "loading...");
  body.append(h("small", null, "Everything that happened, newest first. Colors = who did it."), list);
  const { data } = await sb.from("log").select("*").order("created_at", { ascending: false }).limit(300);
  const icon = { join: "👋", suggest: "📖", vote: "🔖", withdraw: "📕", pull: "🚫", approve: "✅", round: "📚" };
  list.replaceChildren(...(data?.length ? data.map((l) => h("p", { vars: { "--mc": member(l.member_id)?.color || "#ddd" } },
    h("span", { class: "ts" }, `${fmtDay(l.created_at)} ${fmtTime(l.created_at)}`), `${icon[l.kind] || "•"} ${l.text}`)) : [h("p", null, "Nothing yet. Go pick a book!")]));
}
function openRead() {
  const body = dialog("📚 Books We've Read", { wide: true });
  body.append(S.read.length ? h("div", { class: "hof" }, S.read.map((b) => h("div", null,
    b.cover_url ? coverImg(b) : plainCover(b), h("b", null, b.title), h("span", null, "picked by ", member(b.member_id)?.name || "?"))))
    : h("p", null, "Nothing read yet. Go put some books on the shelf!"));
}
// Crystal Ball of Encouragement and Love: every finished day's saying and how many likes it got (saved at midnight Pacific)
async function openLoveNotes() {
  const body = dialog("🔮 Crystal Ball of Encouragement and Love", { wide: true });
  const list = h("div", { class: "lnotes" }, "loading...");
  body.append(list);
  try { await rpc("archive_love_notes", {}); } catch { /* still show what's saved */ }
  const { data } = await sb.from("love_notes").select("day,body,likes").order("day", { ascending: false });
  const notes = data || [];
  if (!notes.length) { list.replaceChildren(h("p", null, "Nothing saved yet. Today's saying gets saved at midnight, so go give the crystal ball some love!")); return; }
  const best = Math.max(...notes.map((n) => n.likes));
  const pretty = (d) => new Date(d + "T12:00:00Z").toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric", timeZone: "UTC" });
  list.replaceChildren(...notes.map((n) => h("div", { class: "lnote" + (best > 0 && n.likes === best ? " top" : "") },
    best > 0 && n.likes === best ? h("span", { class: "crown" }, "👑 MOST LOVED") : null,
    h("q", null, n.body),
    h("div", { class: "meta" }, h("span", null, h("b", null, n.likes.toLocaleString()), n.likes === 1 ? " like" : " likes"), h("span", null, pretty(n.day))))));
}
function openRules() {
  const body = dialog("The Rules");
  body.append(h("ol", { class: "rules" },
    h("li", null, `One pick each: a book, novella or short story under ${maxPages()} pages.`),
    h("li", null, "You get 3 🔖 bookmarks to vote with. Put 2 in one book for a big vote."),
    h("li", null, "Returning your pick early = +1 late fee. Forever."),
    h("li", null, "The most-bookmarked book wins. Then we all read it.")));
}
function openAdmin() {
  const body = dialog("Admin");
  const box = h("div");
  const pending = S.books.filter((b) => b.status === "pending");
  const { per } = marks();
  const leader = S.books.filter((b) => b.status === "active").sort((a, b) => (per.get(b.id) || 0) - (per.get(a.id) || 0) || a.created_at.localeCompare(b.created_at))[0];
  const ask = () => box.replaceChildren(h("div", { class: "confirm" },
    h("b", null, leader ? `${leader.title} wins with ${per.get(leader.id) || 0} 🔖, and the shelf gets cleared. Do it?` : "No books on the shelf yet."),
    h("div", { class: "row" }, h("button", { type: "button", class: "btn red", disabled: !leader, onclick: async () => {
      try { await rpc("close_round", { p_token: S.token }); closeDialog(); await refreshShelf(); celebrate("WE'RE READING IT!"); }
      catch (e) { toast(errMsg(e), true); }
    } }, "Yes, close it"), h("button", { type: "button", class: "btn", onclick: () => box.replaceChildren(closeBtn) }, "Not yet"))));
  const closeBtn = h("button", { type: "button", class: "btn big", onclick: ask }, "Crown the winner + clear the shelf");
  box.append(closeBtn);
  body.append(
    h("h3", null, "Waiting for your OK"),
    pending.length ? h("div", null, pending.map((b) => h("div", { class: "row" }, h("span", null, `${b.title} (${member(b.member_id)?.name})`),
      h("button", { type: "button", class: "btn", onclick: () => openBook(b.id) }, "Check it")))) : h("span", null, "Nothing waiting."),
    h("h3", null, "Pick the winner"), box,
    h("small", null, "Need a new code for a member? Ask Claude to run scripts/set_codes.py with their name."));
}

// ---------- fun stuff ----------
function celebrate(word = "NEW BOOK!") {
  const colors = ["#ff8fb8", "#ffd166", "#7bd88f", "#ff9f43", "#b99cff", "#f4e1b0"];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce) for (let i = 0; i < 90; i++) {
    const c = h("div", { class: "confetti" + (i % 3 ? "" : " leaf"), vars: {
      left: Math.random() * 100 + "vw", background: colors[i % colors.length], "--dx": (Math.random() * 200 - 100) + "px",
      "--rot": (Math.random() * 1080 - 540) + "deg", "--d": (2.4 + Math.random() * 1.8) + "s", "animation-delay": Math.random() * 0.4 + "s",
    } });
    document.body.append(c); setTimeout(() => c.remove(), 4800);
  }
  const f = h("div", { class: "flourish" }, h("div", null, word));
  document.body.append(f); setTimeout(() => f.remove(), 1900);
  [523, 659, 784, 1047].forEach((fr, i) => blip(fr, i * 0.11));
}
// returning a pick early: an original little librarian goes "tsk tsk tsk" and shushes you
function tsk() {
  const lady = h("div", { class: "dude f1" }, h("div", { class: "bun" }), h("div", { class: "head" }, h("i", { class: "specs" })), h("div", { class: "mouth" }), h("div", { class: "body" }), h("div", { class: "arm2" }), h("div", { class: "arm" }), h("div", { class: "legs" }));
  const bubble = h("div", { class: "bubble" }, "tsk");
  const ov = h("div", { class: "sass", onclick: () => ov.remove() }, h("div", { class: "stage" }, bubble, lady, h("small", null, "(tap to close)")));
  document.body.append(ov);
  const frames = [["f1", "tsk"], ["f2", "tsk tsk"], ["f3", "tsk tsk tsk!"], ["f1", "tsk tsk tsk!"], ["f2", "shhh... late fee. ☝️"], ["f3", "shhh... late fee. ☝️"]];
  frames.forEach(([cls, txt], i) => setTimeout(() => { lady.className = "dude " + cls; bubble.textContent = txt; if (i < 3) blip(880 - i * 90, 0); }, i * 420));
  setTimeout(() => ov.remove(), 3800);
}

// ---------- sign in/out + presence ----------
let room = null;
function setupPresence() {
  room = sb.channel("room", { config: { presence: { key: "tab-" + Math.random().toString(36).slice(2) } } });
  room.on("presence", { event: "sync" }, () => {
    // only real members count; visitors never track, and anything else is ignored
    const now = new Set();
    for (const metas of Object.values(room.presenceState())) for (const m of metas) if (member(m.member_id)) now.add(m.member_id);
    if (S.hereReady) {
      for (const id of now) if (!S.here.has(id)) { addLocalLine(`🔔 ${member(id).name} came in from the cold.`); doorOpen(); }
      for (const id of S.here) if (!now.has(id) && member(id)) { addLocalLine(`🚪 ${member(id).name} has left the room.`); doorClose(); }
    }
    S.here = now; S.hereReady = true; renderHere();
  });
  room.subscribe((status) => { if (status === "SUBSCRIBED") trackPresence(); });
}
async function trackPresence() {
  if (!room) return;
  if (S.me && S.chatOn) await room.track({ member_id: S.me.id });
  else await room.untrack();
}
function addLocalLine(text) {
  S.messages.push({ kind: "local", body: text, created_at: new Date().toISOString() });
  renderChat();
}
function toggleChatOn() {
  audio();
  S.chatOn = !S.chatOn; store.set("bc_chat_on", S.chatOn ? "1" : "0");
  trackPresence(); renderChatMenu(); renderSend();
}
async function signOut() {
  try { await rpc("logout", { p_token: S.token }); } catch { /* already gone */ }
  S.token = null; S.me = null; store.set("bc_token", null);
  afterAuthChange(); toast("Signed out. Bye! 👋");
}
let pep = null;
function afterAuthChange() { trackPresence(); renderAll(); pep?.authChanged(); }

// ---------- live updates ----------
let shelfTimer = null;
async function refreshShelf() { await loadShelf(); renderNav(); renderShelf(); if (S.openBookId) refreshBookDialog(); }
const refreshShelfSoon = () => { clearTimeout(shelfTimer); shelfTimer = setTimeout(refreshShelf, 250); };
function setupRealtime() {
  sb.channel("db")
    .on("postgres_changes", { event: "*", schema: "public", table: "books" }, refreshShelfSoon)
    .on("postgres_changes", { event: "*", schema: "public", table: "votes" }, refreshShelfSoon)
    .on("postgres_changes", { event: "*", schema: "public", table: "rounds" }, refreshShelfSoon)
    .on("postgres_changes", { event: "*", schema: "public", table: "members" }, async () => { await loadMembers(); renderAll(); })
    .on("postgres_changes", { event: "INSERT", schema: "public", table: "messages" }, (p) => {
      S.messages.push(p.new); if (S.messages.length > 200) S.messages.shift();
      renderChat();
      if (S.tab !== "chat" && matchMedia("(max-width: 820px)").matches) { S.unread++; $("unread").hidden = false; $("unread").textContent = S.unread; }
    })
    .on("postgres_changes", { event: "INSERT", schema: "public", table: "notes" }, (p) => {
      if (S.openBookId === p.new.book_id) { const box = $("layer").querySelector(".notes"); if (box) loadNotes(p.new.book_id, box); }
    })
    .on("postgres_changes", { event: "INSERT", schema: "public", table: "log" }, () => { if (S.logOpen) openLog(); })
    .subscribe();
}

// ---------- mobile tabs ----------
$("mtabs").addEventListener("click", (e) => {
  const b = e.target.closest("button[data-tab]"); if (!b) return;
  S.tab = b.dataset.tab;
  document.body.className = "tab-" + S.tab;
  $("mtabs").querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
  if (S.tab === "chat") { S.unread = 0; $("unread").hidden = true; const log = $("chatlog"); log.scrollTop = log.scrollHeight; }
  window.scrollTo({ top: 0 });
});

// ---------- go ----------
(async function start() {
  try {
    await Promise.all([loadMembers(), loadShelf(), loadMessages(), loadFacts(), checkSession()]);
  } catch (e) { toast("Couldn't reach Book Club's database. Try refreshing.", true); }
  if (S.me) S.me = member(S.me.id) || S.me;
  renderTicker(); renderAll();
  pep = initPep({ sb, rpc, h, toast, audio, getToken: () => S.token });
  setupRealtime(); setupPresence();
  if (S.me && !S.me.setup_done) openSetup();
})();
