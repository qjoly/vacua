"""Build a real installable TTF from Vacua's INK_BANDS grid.

Each glyph is a set of filled vertical bars (one per FILLED band-segment per
column). The grid is 5 columns × 9 bands; we map it onto a 1000-unit em with a
configurable bar width and column gap so the exported TTF matches the on-screen
Vacua specimen.

Usage:
    python scripts/build_font.py                 # writes dist/Vacua-Regular.ttf
    python scripts/build_font.py --weight bold   # uses BOLD variant proportions
    python scripts/build_font.py -o my.ttf
"""

from __future__ import annotations

import argparse
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

from vacua.alphabet import INK_BANDS, N_BANDS, N_COLS, letter_filled, segs
from vacua.variants import WEIGHTS


# ---- Grid → em-units mapping -------------------------------------------------

UPM = 1000           # units per em (standard for TTF)
BAND_H = 100         # 9 bands × 100 = 900 units tall
ASCENT = 900
DESCENT = -100


def units_per_col(weight_style) -> tuple[int, int]:
    """Return (bar_width, col_gap) in em-units from a `Style`.

    We preserve the screen ratio bar/cell exactly: bar = stroke/cell, gap derived
    from column_gap/cell. Solid modes collapse the gap to zero.
    """
    cell = weight_style.cell
    stroke = weight_style.stroke
    gap = getattr(weight_style, "column_gap", 0) if weight_style.column_mode == "spaced" else 0
    # Anchor bar width at 100 units when stroke == cell (full-density reference),
    # so bar in units = stroke/cell * 100.
    bar = round(stroke / cell * BAND_H)
    col_gap = round(gap / cell * BAND_H)
    return max(bar, 20), col_gap


def build_glyph(ch: str, bar_w: int, col_gap: int) -> tuple[object, int]:
    """Build a TTGlyph for `ch` and return (glyph, advance_width)."""
    pen = TTGlyphPen(None)
    filled = letter_filled(ch)

    col_pitch = bar_w + col_gap
    for col in range(N_COLS):
        x0 = col * col_pitch
        x1 = x0 + bar_w
        for b_start, b_end in segs(filled[col]):
            # Band 0 is at the top → y descends as band index grows.
            y_top = ASCENT - b_start * BAND_H
            y_bot = ASCENT - (b_end + 1) * BAND_H
            pen.moveTo((x0, y_bot))
            pen.lineTo((x0, y_top))
            pen.lineTo((x1, y_top))
            pen.lineTo((x1, y_bot))
            pen.closePath()

    advance = N_COLS * col_pitch + col_gap  # trailing side-bearing
    return pen.glyph(), advance


def build_space(col_gap: int, bar_w: int) -> tuple[object, int]:
    pen = TTGlyphPen(None)
    advance = 3 * (bar_w + col_gap)
    return pen.glyph(), advance


def build_font(weight: str = "regular") -> FontBuilder:
    style = WEIGHTS[weight]
    bar_w, col_gap = units_per_col(style)

    fb = FontBuilder(UPM, isTTF=True)

    glyph_order = [".notdef", "space"] + sorted(c for c in INK_BANDS)
    cmap: dict[int, str] = {0x20: "space"}
    glyphs: dict[str, object] = {}
    metrics: dict[str, tuple[int, int]] = {}

    # .notdef — empty box
    pen = TTGlyphPen(None)
    notdef_w = N_COLS * (bar_w + col_gap)
    pen.moveTo((50, 0)); pen.lineTo((50, ASCENT)); pen.lineTo((notdef_w - 50, ASCENT))
    pen.lineTo((notdef_w - 50, 0)); pen.closePath()
    glyphs[".notdef"] = pen.glyph()
    metrics[".notdef"] = (notdef_w, 0)

    space_g, space_w = build_space(col_gap, bar_w)
    glyphs["space"] = space_g
    metrics["space"] = (space_w, 0)

    for ch in sorted(INK_BANDS):
        name = glyph_name(ch)
        if name in glyphs:  # shouldn't happen, but be safe
            continue
        if name not in glyph_order:
            glyph_order.append(name)
        g, w = build_glyph(ch, bar_w, col_gap)
        glyphs[name] = g
        metrics[name] = (w, 0)
        cmap[ord(ch)] = name
        # Also map lowercase to the same glyph (Vacua is uppercase-only).
        if ch.isalpha():
            cmap[ord(ch.lower())] = name

    # Rebuild glyph_order to match exactly what we created (sorted predictable).
    glyph_order = [".notdef", "space"] + [glyph_name(c) for c in sorted(INK_BANDS)]

    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=ASCENT, descent=DESCENT)
    weight_class = {"regular": 400, "medium": 500, "bold": 700}.get(weight, 400)
    is_bold = weight == "bold"
    # fsSelection bits: 0=italic, 5=bold, 6=regular (mutually exclusive with bold/italic).
    fs_selection = (1 << 5) if is_bold else (1 << 6)
    fb.setupOS2(
        sTypoAscender=ASCENT, sTypoDescender=DESCENT,
        usWinAscent=ASCENT, usWinDescent=-DESCENT,
        usWeightClass=weight_class,
        fsSelection=fs_selection,
        achVendID="VACU",
    )

    family = f"Vacua {weight.title()}"
    fb.setupNameTable({
        "familyName": "Vacua",
        "styleName": weight.title(),
        "uniqueFontIdentifier": f"Vacua-{weight.title()}-0.1.0",
        "fullName": family,
        "psName": f"Vacua-{weight.title()}",
        "version": "Version 0.1.0",
    })
    fb.setupPost()
    return fb


def glyph_name(ch: str) -> str:
    if ch.isalpha():
        return ch.upper()  # PostScript-friendly: A, B, …, Z
    return {"?": "question"}.get(ch, f"uni{ord(ch):04X}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--weight", choices=sorted(WEIGHTS), default="regular")
    ap.add_argument("-o", "--output", type=Path, default=None)
    ap.add_argument("--all", action="store_true",
                    help="Export every weight to dist/")
    args = ap.parse_args()

    weights = sorted(WEIGHTS) if args.all else [args.weight]
    out_dir = Path("dist")
    out_dir.mkdir(exist_ok=True)

    for w in weights:
        fb = build_font(w)
        path = args.output if args.output and not args.all else out_dir / f"Vacua-{w.title()}.ttf"
        fb.save(str(path))
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
