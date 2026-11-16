// The club's look: colors, wallpaper (page background) and frame (the border on every panel).
// The admin picks one of each in the Admin dialog; the choice lives in the club_look table.
// Every pattern is a small SVG drawn here from the chosen colors, so any wallpaper or frame
// works with any colors.

export const DEFAULT_LOOK = {
  club_name: "Book Club", tagline: "★ like game club but for books ★",
  colorway: "claret", wallpaper: "floral", frame: "rule",
};

// ground = page background, motif = wallpaper print, soft = second print color,
// accent = headings, buttons and frames, paper = panels
export const COLORWAYS = {
  claret:     { name: "Claret",      ground: "#efe6d8", motif: "#8e2534", soft: "#7d8a63", accent: "#7a1d2b", paper: "#fffbf4" },
  rose:       { name: "Rosewater",   ground: "#f5e4e1", motif: "#c0607a", soft: "#7f9c7a", accent: "#963652", paper: "#fffaf8" },
  sage:       { name: "Sage",        ground: "#e4e8da", motif: "#58724f", soft: "#c48b79", accent: "#3f5a3a", paper: "#fdfdf7" },
  lavender:   { name: "Lavender",    ground: "#ebe5f1", motif: "#7c66a7", soft: "#c4a35e", accent: "#55437d", paper: "#fdfbff" },
  cornflower: { name: "Cornflower",  ground: "#e3e9f3", motif: "#3f61a8", soft: "#d0a24c", accent: "#2b4784", paper: "#fbfcff" },
  butter:     { name: "Butter",      ground: "#f6edcb", motif: "#c27b2d", soft: "#5f8b69", accent: "#874a18", paper: "#fffdf4" },
  ink:        { name: "Ink & Paper", ground: "#f1eee7", motif: "#2a2622", soft: "#8d877d", accent: "#25211e", paper: "#fffefb" },
  midnight:   { name: "Midnight",    ground: "#1d2238", motif: "#c9aa62", soft: "#7f8ab6", accent: "#26315c", paper: "#fbf8f1", dark: true },
};

const enc = (w, h, body) => `url("data:image/svg+xml,${encodeURIComponent(`<svg xmlns='http://www.w3.org/2000/svg' width='${w}' height='${h}' viewBox='0 0 ${w} ${h}'>${body}</svg>`)}")`;
const f = (n) => +n.toFixed(2);

// a five-petal flower and a leaf, for the floral prints
function flower(cx, cy, r, petal, middle) {
  let s = "";
  for (let k = 0; k < 5; k++) {
    const a = (k * 72 - 90) * Math.PI / 180;
    s += `<circle cx='${f(cx + Math.cos(a) * r)}' cy='${f(cy + Math.sin(a) * r)}' r='${f(r * 0.78)}' fill='${petal}'/>`;
  }
  return s + `<circle cx='${cx}' cy='${cy}' r='${f(r * 0.5)}' fill='${middle}'/>`;
}
const leaf = (x, y, rot, col) => `<ellipse cx='${x}' cy='${y}' rx='3.6' ry='1.5' fill='${col}' transform='rotate(${rot} ${x} ${y})'/>`;
const star4 = (x, y, r, col) => `<path fill='${col}' d='M${x} ${y - r}Q${x} ${y} ${x + r} ${y}Q${x} ${y} ${x} ${y + r}Q${x} ${y} ${x - r} ${y}Q${x} ${y} ${x} ${y - r}Z'/>`;

// ---------- wallpapers (page background tiles) ----------
export const WALLPAPERS = {
  floral: { name: "Ditsy floral", draw: (c) => enc(128, 128, `<g opacity='.5'>
    ${leaf(30, 33, 40, c.soft)}${leaf(15, 34, -30, c.soft)}${flower(23, 26, 3.5, c.motif, c.ground)}
    ${leaf(95, 82, 120, c.soft)}${leaf(86, 93, 20, c.soft)}${flower(90, 76, 3.5, c.motif, c.ground)}
    ${leaf(50, 112, -60, c.soft)}${flower(44, 106, 2.6, c.motif, c.ground)}
    ${flower(96, 20, 2.1, c.soft, c.ground)}${flower(18, 86, 2.1, c.soft, c.ground)}${flower(62, 56, 2.1, c.soft, c.ground)}
    <g fill='${c.motif}'><circle cx='64' cy='14' r='1'/><circle cx='118' cy='50' r='1'/><circle cx='34' cy='64' r='1'/><circle cx='112' cy='112' r='1'/><circle cx='78' cy='118' r='.8'/></g></g>`) },
  stripe: { name: "Regency stripe", draw: (c) => enc(40, 14, `<rect width='15' height='14' fill='${c.motif}' opacity='.07'/>
    <rect x='18' width='1' height='14' fill='${c.motif}' opacity='.3'/><rect x='21' width='1' height='14' fill='${c.motif}' opacity='.3'/>
    <circle cx='7.5' cy='7' r='1.2' fill='${c.motif}' opacity='.35'/>`) },
  trellis: { name: "Trellis", draw: (c) => enc(44, 44, `<path d='M22 0L44 22L22 44L0 22Z' fill='none' stroke='${c.motif}' stroke-width='.8' opacity='.3'/>
    <g fill='${c.soft}' opacity='.75'><circle cx='22' cy='19.8' r='1.7'/><circle cx='22' cy='24.2' r='1.7'/><circle cx='19.8' cy='22' r='1.7'/><circle cx='24.2' cy='22' r='1.7'/></g>
    <circle cx='22' cy='22' r='.9' fill='${c.motif}'/>
    <g fill='${c.motif}' opacity='.45'><circle cx='0' cy='0' r='1.4'/><circle cx='44' cy='0' r='1.4'/><circle cx='0' cy='44' r='1.4'/><circle cx='44' cy='44' r='1.4'/></g>`) },
  gingham: { name: "Gingham", draw: (c) => enc(22, 22, `<rect width='11' height='22' fill='${c.motif}' opacity='.13'/><rect width='22' height='11' fill='${c.motif}' opacity='.13'/>`) },
  dots: { name: "Polka dot", draw: (c) => enc(30, 30, `<g fill='${c.motif}' opacity='.38'><circle cx='7.5' cy='7.5' r='2.6'/><circle cx='22.5' cy='22.5' r='2.6'/></g>`) },
  stars: { name: "Starry", draw: (c) => enc(64, 64, `${star4(16, 16, 5, c.motif)}${star4(46, 42, 3.4, c.motif)}
    <g fill='${c.soft}'><circle cx='44' cy='12' r='1'/><circle cx='12' cy='48' r='1.2'/><circle cx='30' cy='30' r='.8'/><circle cx='58' cy='58' r='.8'/></g>`.replace(/<path/g, "<path opacity='.55'")) },
  hearts: { name: "Sweethearts", draw: (c) => {
    const heart = (x, y) => `<path transform='translate(${x} ${y})' d='M0 2.2C0-.6 3.6-.9 4 1.7C4.4-.9 8-.6 8 2.2C8 4.8 5 6.4 4 8C3 6.4 0 4.8 0 2.2Z'/>`;
    return enc(36, 36, `<g fill='${c.motif}' opacity='.42'>${heart(5, 5)}${heart(23, 23)}</g>`);
  } },
  check: { name: "Checkerboard", draw: (c) => enc(24, 24, `<g fill='${c.motif}' opacity='.1'><rect width='12' height='12'/><rect x='12' y='12' width='12' height='12'/></g>`) },
  ruled: { name: "Ruled paper", draw: (c) => enc(24, 24, `<rect y='23' width='24' height='1' fill='${c.soft}' opacity='.4'/>`) },
  linen: { name: "Plain linen", draw: (c) => enc(6, 6, `<rect y='2' width='6' height='.6' fill='${c.motif}' opacity='.06'/><rect x='4' width='.6' height='6' fill='${c.motif}' opacity='.05'/>`) },
};

// ---------- frames (the border around every panel) ----------
// Each one is a 36x36 picture used as a border-image sliced at 12px: the corners stay put and the
// middle 12px of each side repeats, so the patterns all repeat every 3, 6 or 12px.
const RING = "M0 0H36V36H0ZM12 12V24H24V12Z";
const sides = (g) => [0, 90, 180, 270].map((r) => `<g transform='rotate(${r} 18 18)'>${g}</g>`).join("");
const line = (d, t, col) => `<rect x='${d}' y='${d}' width='${36 - 2 * d}' height='${t}' fill='${col}'/>`; // one side of a nested rectangle
const ringWith = (fill, defs = "") => `${defs}<path fill-rule='evenodd' d='${RING}' fill='${fill}'/>`;
const frame = (body) => enc(36, 36, body);

export const FRAMES = {
  rule: { name: "Double rule", draw: (c) => frame(ringWith(c.paper) + sides(line(1, 0.9, c.accent) + line(3.6, 2.4, c.accent) + line(8.4, 0.9, c.accent))) },
  stamp: { name: "Postage stamp", cutout: true, draw: (c) => {
    let holes = ""; for (let x = 3; x < 36; x += 6) holes += `<circle cx='${x}' cy='0' r='2.3'/>`;
    return frame(`<defs><mask id='m'><path fill-rule='evenodd' d='${RING}' fill='#fff'/><g fill='#000'>${sides(holes)}</g></mask></defs>
      <path fill-rule='evenodd' d='${RING}' fill='#fffefa' mask='url(#m)'/>${sides(line(7.6, 0.9, c.accent))}`);
  } },
  scallop: { name: "Scalloped lace", cutout: true, draw: (c) => {
    const bumps = [6, 18, 30].map((x) => `<circle cx='${x}' cy='6' r='6'/>`).join("");
    const eyes = [6, 18, 30].map((x) => `<circle cx='${x}' cy='5' r='1.3'/>`).join("");
    return frame(`<defs><mask id='m'><rect width='36' height='36' fill='#fff'/><rect x='12' y='12' width='12' height='12' fill='#000'/><g fill='#000'>${sides(eyes)}</g></mask></defs>
      <g fill='#fffefa' mask='url(#m)'>${sides(`<rect x='0' y='6' width='36' height='6'/>` + bumps)}</g>${sides(line(10, 0.9, c.accent))}`);
  } },
  stitch: { name: "Stitched ribbon", draw: (c) => frame(ringWith(c.accent) +
    sides(`<path d='M6 6H30' stroke='${c.paper}' stroke-width='1.1' stroke-dasharray='3 3' fill='none' opacity='.9'/>` + line(0, 0.8, "rgba(0,0,0,.25)") + line(11.2, 0.8, "rgba(0,0,0,.25)"))) },
  gingham: { name: "Gingham ribbon", draw: (c) => frame(ringWith("url(#g)", `<defs><pattern id='g' width='6' height='6' patternUnits='userSpaceOnUse'>
      <rect width='6' height='6' fill='${c.paper}'/><rect width='3' height='6' fill='${c.accent}' opacity='.5'/><rect width='6' height='3' fill='${c.accent}' opacity='.5'/></pattern></defs>`) + sides(line(0, 0.8, c.accent))) },
  floral: { name: "Floral ribbon", draw: (c) => frame(ringWith("url(#p)", `<defs><pattern id='p' width='12' height='12' patternUnits='userSpaceOnUse'>
      <rect width='12' height='12' fill='${c.accent}'/>${flower(6, 6, 1.75, c.paper, c.soft)}</pattern></defs>`)) },
  dots: { name: "Polka ribbon", draw: (c) => frame(ringWith("url(#p)", `<defs><pattern id='p' width='12' height='12' patternUnits='userSpaceOnUse'>
      <rect width='12' height='12' fill='${c.accent}'/><g fill='${c.paper}'><circle cx='3' cy='3' r='1.4'/><circle cx='9' cy='9' r='1.4'/></g></pattern></defs>`)) },
  check: { name: "Checkerboard", draw: (c) => frame(ringWith("url(#p)", `<defs><pattern id='p' width='6' height='6' patternUnits='userSpaceOnUse'>
      <rect width='6' height='6' fill='${c.paper}'/><g fill='${c.accent}'><rect width='3' height='3'/><rect x='3' y='3' width='3' height='3'/></g></pattern></defs>`)) },
  flannel: { name: "Flannel", draw: (c) => frame(ringWith("url(#p)", `<defs><pattern id='p' width='12' height='12' patternUnits='userSpaceOnUse'>
      <rect width='12' height='12' fill='${c.accent}'/><g fill='#000' opacity='.28'><rect width='4' height='12'/><rect width='12' height='4'/></g>
      <g fill='${c.soft}' opacity='.7'><rect x='7' width='1' height='12'/><rect y='7' width='12' height='1'/></g></pattern></defs>`)) },
};

export function lookOf(row) {
  const l = { ...DEFAULT_LOOK, ...(row || {}) };
  if (!COLORWAYS[l.colorway]) l.colorway = DEFAULT_LOOK.colorway;
  if (!WALLPAPERS[l.wallpaper]) l.wallpaper = DEFAULT_LOOK.wallpaper;
  if (!FRAMES[l.frame]) l.frame = DEFAULT_LOOK.frame;
  return l;
}

// two letters for the wax seal: "Book Club" -> "BC", "The Oak Street Readers" -> "OS"
export function monogram(name) {
  const words = String(name || "").split(/\s+/).filter((w) => /^[\p{L}\p{N}]/u.test(w) && !/^(the|a|an|of|and|&)$/i.test(w));
  return (words.slice(0, 2).map((w) => w[0]).join("") || "BC").toUpperCase();
}

// the CSS variables for one look
export function lookVars(l) {
  const c = COLORWAYS[l.colorway];
  return {
    "--ground": c.ground, "--motif": c.motif, "--soft": c.soft, "--accent": c.accent, "--paper": c.paper,
    "--on-ground": c.dark ? "#efe6d2" : "#3d322b",
    "--wallpaper": WALLPAPERS[l.wallpaper].draw(c),
    "--frame": FRAMES[l.frame].draw(c),
  };
}

export function applyLook(row, { remember = true } = {}) {
  const l = lookOf(row);
  const root = document.documentElement;
  const vars = lookVars(l);
  for (const [k, v] of Object.entries(vars)) root.style.setProperty(k, v);
  root.dataset.frame = FRAMES[l.frame].cutout ? "cutout" : "solid";
  root.dataset.ground = COLORWAYS[l.colorway].dark ? "dark" : "light";
  if (remember) {
    // the little script in index.html puts this back before the page first paints
    try { localStorage.setItem("bc_look", JSON.stringify({ vars, frame: root.dataset.frame, ground: root.dataset.ground, name: l.club_name, tagline: l.tagline })); } catch { /* private mode */ }
  }
  return l;
}
