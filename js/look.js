// The club's look, granny-square afghan style: yarn colors, a photo wallpaper (real photos of grandma's
// things, tiled) and a crochet border around every panel. The admin picks one of each in the Admin
// dialog; the choice lives in the club_look table (columns colorway = yarn, wallpaper, frame).
// The borders are SVGs drawn here from the yarn colors, so any border works with any yarn.

export const DEFAULT_LOOK = {
  club_name: "Book Club", tagline: "like game club but for books",
  colorway: "rainbow", wallpaper: "granny", frame: "rounds",
};

// accent = the club's name + headings, rounds = the three crochet rounds on most panels (inside out),
// rounds2 = the rounds on the chat + Daily Reading, pastels = button + card colors, edge = the dark
// outline yarn, paper = the cream inside every panel
export const COLORWAYS = {
  rainbow:   { name: "Rainbow scraps",   accent: "#d6336c", rounds: ["#e8590c", "#fcc419", "#1098ad"], rounds2: ["#7950f2", "#ff8fb1", "#fcc419"], pastels: ["#fcc419", "#ff8fb1", "#96f2d7", "#ffd8a8", "#d0bfff"], edge: "#1b1b1b", paper: "#fffaf0" },
  harvest:   { name: "Avocado & gold",   accent: "#b4521b", rounds: ["#7d8a2a", "#e0a526", "#8a4b1e"], rounds2: ["#c2651a", "#f0d37a", "#5e6b1d"], pastels: ["#f2d16b", "#cdd68a", "#f4b183", "#ead3b0", "#e6c46d"], edge: "#3b2414", paper: "#fff8ea" },
  sherbet:   { name: "Sherbet",          accent: "#c2255c", rounds: ["#ff8787", "#ffd43b", "#74c0fc"], rounds2: ["#b197fc", "#63e6be", "#ffa8a8"], pastels: ["#ffe066", "#ffc9c9", "#a5d8ff", "#c3fae8", "#eebefa"], edge: "#2b1b33", paper: "#fffaf3" },
  christmas: { name: "Christmas afghan", accent: "#c92a2a", rounds: ["#2b8a3e", "#f8f9fa", "#c92a2a"], rounds2: ["#c92a2a", "#f8f9fa", "#2b8a3e"], pastels: ["#ffc9c9", "#b2f2bb", "#fff3bf", "#ffe3e3", "#d3f9d8"], edge: "#1b1b1b", paper: "#fffbf3" },
  baby:      { name: "Baby blanket",     accent: "#d6336c", rounds: ["#a5d8ff", "#fcc2d7", "#fff3bf"], rounds2: ["#d3f9d8", "#e5dbff", "#ffd8a8"], pastels: ["#fff3bf", "#fcc2d7", "#a5d8ff", "#d3f9d8", "#e5dbff"], edge: "#5c4b6b", paper: "#fffdf8" },
  violet:    { name: "African violet",   accent: "#6a2c91", rounds: ["#b197fc", "#69a84f", "#e599f7"], rounds2: ["#e599f7", "#f8f0fc", "#69a84f"], pastels: ["#e5dbff", "#d3f9d8", "#f3d9fa", "#fff3bf", "#d0bfff"], edge: "#2d1b3d", paper: "#fffbff" },
  ribbon:    { name: "Blue ribbon",      accent: "#1c4b8f", rounds: ["#c92a2a", "#f8f9fa", "#1c4b8f"], rounds2: ["#4dabf7", "#ffe066", "#1c4b8f"], pastels: ["#a5d8ff", "#ffc9c9", "#fff3bf", "#d0ebff", "#ffe066"], edge: "#10203a", paper: "#fffcf6" },
};

// ---------- wallpapers: real photos (Wikimedia Commons, see credits.html), tiled ----------
// size = how wide one tile shows on screen, ground = its average color (shows while it loads)
export const WALLPAPERS = {
  granny:   { name: "Granny squares",     size: 360, ground: "#8f7b7a" },
  afghan:   { name: "'70s afghan",        size: 300, ground: "#756b5d" },
  quilt:    { name: "Irish chain quilt",  size: 360, ground: "#56422f" },
  doilies:  { name: "Doilies on velvet",  size: 400, ground: "#6d5c5d" },
  doily:    { name: "Big red doily",      size: 190, ground: "#ad5454" },
  candy:    { name: "Candy dish",         size: 340, ground: "#dcb6bd" },
  willow:   { name: "Blue willow",        size: 420, ground: "#becadb" },
  roses:    { name: "Rose china",         size: 320, ground: "#ab9d9e" },
  rosebud:  { name: "Rosebud stripe",     size: 220, ground: "#c0bca9" },
  calico:   { name: "Calico",             size: 240, ground: "#807867" },
  toile:    { name: "Red toile",          size: 320, ground: "#b0837b" },
  chenille: { name: "Chenille bedspread", size: 280, ground: "#535c1e" },
  rug:      { name: "The good rug",       size: 420, ground: "#a5664e" },
  buttons:  { name: "Button tin",         size: 420, ground: "#63462a" },
  xstitch:  { name: "Cross-stitch",       size: 300, ground: "#ab6a6e" },
};
const WALL_DIR = new URL("../img/wall/", import.meta.url).href;
export const wallUrl = (id, thumb = false) => `${WALL_DIR}${id}${thumb ? "-t" : ""}.jpg`;

// ---------- borders ----------
// Each is a 150x150 picture used as a border-image sliced at 30: the corners stay put and the middle
// 90 of each side repeats, so every pattern here repeats every 6, 10, 15, 30 or 90 units.
const N = 150;
const enc = (body) => `url("data:image/svg+xml,${encodeURIComponent(`<svg xmlns='http://www.w3.org/2000/svg' width='${N}' height='${N}' viewBox='0 0 ${N} ${N}'>${body}</svg>`)}")`;
const sq = (o, fill) => `<rect x='${o}' y='${o}' width='${N - 2 * o}' height='${N - 2 * o}' fill='${fill}'/>`;
// little dark/light dashes along a round so it reads as yarn, not paint
const yarn = (o, w) => `<rect x='${o}' y='${o}' width='${N - 2 * o}' height='${N - 2 * o}' fill='none' stroke='#000' stroke-opacity='.22' stroke-width='${w}' stroke-dasharray='3 3'/>`
  + `<rect x='${o}' y='${o}' width='${N - 2 * o}' height='${N - 2 * o}' fill='none' stroke='#fff' stroke-opacity='.28' stroke-width='${w * 0.35}' stroke-dasharray='2 4' stroke-dashoffset='-3.5'/>`;
const sides = (g) => [0, 90, 180, 270].map((r) => `<g transform='rotate(${r} 75 75)'>${g}</g>`).join("");
const range = (from, to, step) => { const a = []; for (let x = from; x <= to + 1e-6; x += step) a.push(+x.toFixed(2)); return a; };

export const FRAMES = {
  rounds: { name: "Three rounds", draw: (c, r) => enc(sq(0, c.edge) + sq(7, r[2]) + sq(13, r[1]) + sq(19, r[0]) + sq(25, c.paper) + yarn(10, 3.4) + yarn(16, 3.4) + yarn(22, 3.4)) },
  shell: { name: "Shell stitch", cutout: true, draw: (c, r) => {
    const shells = range(7.5, 142.5, 15).map((x) => `<circle cx='${x}' cy='12' r='7.5' fill='${r[0]}' stroke='${c.edge}' stroke-width='2'/><circle cx='${x}' cy='12' r='3' fill='none' stroke='#000' stroke-opacity='.25' stroke-width='1.4'/>`).join("");
    return enc(sides(shells) + sq(12, c.edge) + sq(14.5, r[2]) + sq(19.5, r[1]) + sq(24.5, c.paper) + yarn(17, 3) + yarn(22, 3));
  } },
  granny: { name: "Granny squares", draw: (c, r) => {
    const sets = [[r[2], r[1], c.accent], [c.accent, r[0], r[1]], [r[1], r[2], r[0]]];
    const one = (x, [a, b, m]) => `<rect x='${x}' y='0' width='30' height='30' fill='${c.edge}'/><rect x='${x + 2.5}' y='2.5' width='25' height='25' fill='${a}'/>`
      + `<rect x='${x + 7}' y='7' width='16' height='16' fill='${c.edge}'/><rect x='${x + 8}' y='8' width='14' height='14' fill='${b}'/>`
      + `<rect x='${x + 12}' y='12' width='6' height='6' fill='${m}'/>`
      + `<rect x='${x + 5}' y='5' width='20' height='20' fill='none' stroke='#000' stroke-opacity='.22' stroke-width='3' stroke-dasharray='2.5 2.5'/>`;
    return enc(sides([0, 30, 60, 90, 120].map((x, i) => one(x, sets[i % 3])).join("")));
  } },
  ricrac: { name: "Ric-rac", draw: (c, r) => {
    const pts = range(-7.5, 157.5, 7.5).map((x, i) => `${x},${i % 2 ? 21 : 9.5}`).join(" ");
    const zig = `<polyline points='${pts}' fill='none' stroke='${c.edge}' stroke-width='7.5' stroke-linejoin='round'/><polyline points='${pts}' fill='none' stroke='${r[0]}' stroke-width='4.5' stroke-linejoin='round'/>`;
    return enc(sq(0, c.edge) + sq(3.5, r[1]) + `<clipPath id='k'><path fill-rule='evenodd' d='M3.5 3.5H146.5V146.5H3.5ZM26.5 26.5V123.5H123.5V26.5Z'/></clipPath><g clip-path='url(#k)'>${sides(zig)}</g>` + sq(26.5, c.edge) + sq(28, c.paper));
  } },
  blanket: { name: "Blanket stitch", draw: (c, r) => {
    const ticks = range(7.5, 142.5, 15).map((x) => `<path d='M${x} 18V8'/>`).join("");
    const st = `<g stroke='${c.edge}' stroke-opacity='.35' stroke-width='4.2' stroke-linecap='round' fill='none' transform='translate(.6 .9)'><path d='M0 18H150'/>${ticks}</g>`
      + `<g stroke='${c.paper}' stroke-width='3' stroke-linecap='round' fill='none'><path d='M0 18H150'/>${ticks}</g>`;
    return enc(sq(0, c.edge) + sq(3, r[2]) + `<clipPath id='k'><path fill-rule='evenodd' d='M3 3H147V147H3ZM24 24V126H126V24Z'/></clipPath><g clip-path='url(#k)'>${sides(st)}</g>` + sq(24, c.edge) + sq(26, c.paper));
  } },
};

export function lookOf(row) {
  const l = { ...DEFAULT_LOOK, ...(row || {}) };
  if (!COLORWAYS[l.colorway]) l.colorway = DEFAULT_LOOK.colorway;
  if (!WALLPAPERS[l.wallpaper]) l.wallpaper = DEFAULT_LOOK.wallpaper;
  if (!FRAMES[l.frame]) l.frame = DEFAULT_LOOK.frame;
  return l;
}

// two letters, e.g. for an icon: "Book Club" -> "BC", "The Oak Street Readers" -> "OS"
export function monogram(name) {
  const words = String(name || "").split(/\s+/).filter((w) => /^[\p{L}\p{N}]/u.test(w) && !/^(the|a|an|of|and|&)$/i.test(w));
  return (words.slice(0, 2).map((w) => w[0]).join("") || "BC").toUpperCase();
}

// the CSS variables for one look
export function lookVars(l) {
  const c = COLORWAYS[l.colorway], w = WALLPAPERS[l.wallpaper], f = FRAMES[l.frame];
  const v = {
    "--accent": c.accent, "--edge": c.edge, "--paper": c.paper,
    "--r1": c.rounds[0], "--r2": c.rounds[1], "--r3": c.rounds[2],
    "--q1": c.rounds2[0], "--q2": c.rounds2[1], "--q3": c.rounds2[2],
    "--ground": w.ground, "--wallpaper": `url("${wallUrl(l.wallpaper)}")`, "--tile": `${w.size}px`,
    "--frame": f.draw(c, c.rounds), "--frame2": f.draw(c, c.rounds2),
  };
  c.pastels.forEach((p, i) => { v[`--b${i + 1}`] = p; });
  return v;
}

export function applyLook(row, { remember = true } = {}) {
  const l = lookOf(row);
  const root = document.documentElement;
  const vars = lookVars(l);
  for (const [k, v] of Object.entries(vars)) root.style.setProperty(k, v);
  root.dataset.frame = FRAMES[l.frame].cutout ? "cutout" : "solid";
  root.dataset.ground = "light";
  if (remember) {
    // the little script in index.html puts this back before the page first paints
    try { localStorage.setItem("bc_look", JSON.stringify({ v: 2, vars, frame: root.dataset.frame, ground: root.dataset.ground, name: l.club_name, tagline: l.tagline })); } catch { /* private mode */ }
  }
  return l;
}
