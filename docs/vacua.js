// Vacua — JS port of the alphabet table. Source of truth: vacua/alphabet.py.
// Each letter: {col: [bands the letter PASSES through, i.e. left empty]}.
// Filled bands (drawn bars) are the complement on a 9-band column.

const FULL = [0,1,2,3,4,5,6,7,8];
const INK_BANDS = {
  A:{0:[2,3,4,5,6,7,8],1:[0,1,4],2:[0,1,4],3:[0,1,4],4:[2,3,4,5,6,7,8]},
  B:{0:FULL,1:[0,4,8],2:[0,4,8],3:[0,4,8],4:[1,2,3,5,6,7]},
  C:{0:[2,3,4,5,6],1:[0,1,7,8],2:[0,8],3:[0,8],4:[0,1,2,6,7,8]},
  D:{0:FULL,1:[0,8],2:[0,8],3:[1,7],4:[2,3,4,5,6]},
  E:{0:FULL,1:[0,4,8],2:[0,4,8],3:[0,4,8],4:[0,4,8]},
  F:{0:FULL,1:[0,4],2:[0,4],3:[0,4],4:[0]},
  G:{0:[2,3,4,5,6],1:[0,1,7,8],2:[0,8],3:[0,4,8],4:[2,3,4,8]},
  H:{0:FULL,1:[4],2:[4],3:[4],4:FULL},
  I:{0:[0,1,7,8],1:[0,1,7,8],2:FULL,3:[0,1,7,8],4:[0,1,7,8]},
  J:{0:[7],1:[8],2:[8],3:FULL,4:[0,1,2,3,4,5,6,7,8]},
  K:{0:FULL,1:[4],2:[3,5],3:[2,6],4:[0,1,7,8]},
  L:{0:FULL,1:[8],2:[8],3:[8],4:[8]},
  M:{0:FULL,1:[1,2],2:[3,4],3:[1,2],4:FULL},
  N:{0:FULL,1:[2,3],2:[4],3:[5,6],4:FULL},
  O:{0:[2,3,4,5,6],1:[0,1,7,8],2:[0,8],3:[0,1,7,8],4:[2,3,4,5,6]},
  P:{0:FULL,1:[0,4],2:[0,4],3:[0,4],4:[1,2,3]},
  Q:{0:[2,3,4,5,6],1:[0,1,7,8],2:[0,8],3:[0,1,7],4:[2,3,4,5,6,8]},
  R:{0:FULL,1:[0,4],2:[0,4],3:[0,4,6],4:[1,2,3,7,8]},
  S:{0:[0,1,2,8],1:[0,4,8],2:[0,4,8],3:[0,4,8],4:[0,6,7,8]},
  T:{0:[0,1],1:[0,1],2:FULL,3:[0,1],4:[0,1]},
  U:{0:[0,1,2,3,4,5,6,7],1:[8],2:[8],3:[8],4:[0,1,2,3,4,5,6,7]},
  V:{0:[0,1,2,3,4],1:[5,6],2:[7,8],3:[5,6],4:[0,1,2,3,4]},
  W:{0:FULL,1:[6,7],2:[4,5],3:[6,7],4:FULL},
  X:{0:[0,1,7,8],1:[2,3,5,6],2:[4],3:[2,3,5,6],4:[0,1,7,8]},
  Y:{0:[0,1,2,3],1:[2,3,4],2:FULL,3:[2,3,4],4:[0,1,2,3]},
  Z:{0:[0,1,7,8],1:[0,1,6,7,8],2:[0,1,4,7,8],3:[0,1,2,7,8],4:[0,1,7,8]},
  "?":{0:[1,8],1:[0,3],2:[0,4,5,8],3:[0,3],4:[1,2]},
};

const N_COLS = 5;
const N_BANDS = 9;

function filledBands(ch) {
  const ink = INK_BANDS[ch.toUpperCase()];
  if (!ink) return null;
  const out = {};
  for (let c = 0; c < N_COLS; c++) {
    out[c] = [];
    for (let b = 0; b < N_BANDS; b++) {
      if (!ink[c].includes(b)) out[c].push(b);
    }
  }
  return out;
}

// Merge contiguous bands into segments [start, end] for compact <rect> output.
function segs(bands) {
  if (!bands.length) return [];
  bands = [...new Set(bands)].sort((a, b) => a - b);
  const out = [];
  let start = bands[0], prev = bands[0];
  for (let i = 1; i < bands.length; i++) {
    if (bands[i] === prev + 1) prev = bands[i];
    else { out.push([start, prev]); start = prev = bands[i]; }
  }
  out.push([start, prev]);
  return out;
}

// Render a single glyph as <g> of <rect> bars.
// opts: {cell, barW, color, rotated, marker}
function glyphSVG(ch, opts = {}) {
  const cell = opts.cell ?? 10;
  // Default ratio 6/14 ≈ 0.43 — Python MEDIUM (variants.py).
  const barW = opts.barW ?? cell * (6 / 14);
  const color = opts.color ?? "#0F1B33";
  const showMarker = opts.marker ?? true;

  if (ch === " ") {
    return `<g></g>`;
  }
  const filled = filledBands(ch);
  if (!filled) return `<g></g>`;

  const parts = [];
  for (let c = 0; c < N_COLS; c++) {
    const cx = c * cell + (cell - barW) / 2;
    for (const [s, e] of segs(filled[c])) {
      const y = s * cell;
      const h = (e - s + 1) * cell;
      parts.push(`<rect x="${cx.toFixed(2)}" y="${y}" width="${barW.toFixed(2)}" height="${h}" fill="${color}"/>`);
    }
  }
  // Top-left marker (puce): horizontal nub signalling letter start.
  // Sized to be clearly visible — wider than a bar, ~half a bar tall.
  if (showMarker) {
    const mw = Math.max(barW * 1.6, cell * 0.7);
    const mh = Math.max(2, barW * 0.55);
    parts.push(`<rect x="0" y="-${(mh + 2).toFixed(2)}" width="${mw.toFixed(2)}" height="${mh.toFixed(2)}" fill="${color}"/>`);
  }
  return `<g>${parts.join("")}</g>`;
}

// Render a word as inline SVG. Returns the SVG element.
function renderWord(text, opts = {}) {
  const cell = opts.cell ?? 12;
  const barW = opts.barW ?? cell * (6 / 14);
  const gap = opts.gap ?? cell * 1.6;
  const spaceW = opts.spaceW ?? cell * 3;
  const color = opts.color ?? "#0F1B33";
  const padTop = opts.padTop ?? cell * 0.9;
  const padX = opts.padX ?? cell * 0.5;

  const chars = [...text.toUpperCase()];
  const glyphW = N_COLS * cell;
  let x = padX;
  const groups = [];
  for (const ch of chars) {
    if (ch === " ") { x += spaceW; continue; }
    if (!INK_BANDS[ch]) continue;
    groups.push(`<g transform="translate(${x.toFixed(2)},${padTop})">${glyphSVG(ch, { cell, barW, color })}</g>`);
    x += glyphW + gap;
  }
  const totalW = x + padX - gap;
  const totalH = N_BANDS * cell + padTop + cell * 0.3;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${totalW.toFixed(2)} ${totalH.toFixed(2)}" preserveAspectRatio="xMidYMid meet">${groups.join("")}</svg>`;
}

// Render a rotation-ligature: glyph A vertical + glyph B rotated 90°, overlaid.
function renderLigature(a, b, opts = {}) {
  const cell = opts.cell ?? 16;
  const barW = opts.barW ?? cell * (6 / 14);
  const colorA = opts.colorA ?? "#2E6FE8";
  const colorB = opts.colorB ?? "#E15A3C";
  // Square span = max(5, 9) = 9; centering offset for the 5-wide vertical letter.
  const span = N_BANDS;
  const offx = ((N_BANDS - N_COLS) / 2) * cell;
  const size = span * cell;
  const pad = cell;
  // Letter A: vertical, centered horizontally.
  const aSVG = `<g transform="translate(${offx},0)">${glyphSVG(a, { cell, barW, color: colorA, marker: false })}</g>`;
  // Letter B: rotated 90° clockwise around the square center.
  const bSVG = `<g transform="rotate(90 ${size / 2} ${size / 2}) translate(${offx},0)">${glyphSVG(b, { cell, barW, color: colorB, marker: false })}</g>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${-pad} ${-pad} ${size + pad * 2} ${size + pad * 2}" preserveAspectRatio="xMidYMid meet">${aSVG}${bSVG}</svg>`;
}

// Render full alphabet chart (A-Z + ?).
function renderChart(opts = {}) {
  const cell = opts.cell ?? 10;
  const barW = opts.barW ?? cell * (6 / 14);
  const cols = opts.cols ?? 9;
  const color = opts.color ?? "#0F1B33";
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
  const glyphW = N_COLS * cell;
  const glyphH = N_BANDS * cell;
  const gapX = cell * 2;
  const gapY = cell * 2;
  const padTop = cell * 0.9;
  const rows = Math.ceil(chars.length / cols);
  const totalW = cols * glyphW + (cols - 1) * gapX + cell;
  const totalH = rows * glyphH + (rows - 1) * gapY + padTop * rows + cell;
  const groups = [];
  chars.forEach((ch, i) => {
    const r = Math.floor(i / cols);
    const c = i % cols;
    const x = c * (glyphW + gapX);
    const y = r * (glyphH + gapY + padTop) + padTop;
    groups.push(`<g transform="translate(${x},${y})">${glyphSVG(ch, { cell, barW, color })}</g>`);
  });
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${totalW} ${totalH}" preserveAspectRatio="xMidYMid meet">${groups.join("")}</svg>`;
}

window.Vacua = { renderWord, renderLigature, renderChart, INK_BANDS, glyphSVG };
