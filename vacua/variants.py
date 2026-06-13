"""
Style variants for Vacua: weights, column modes, ligatures.

All variants are PARAMETERS of the same canonical renderer (`render.py`).
None of them alters `INK_BANDS`. It is the same typeface seen under different
settings.
"""

from __future__ import annotations

from dataclasses import replace

from .render import Style

# --- Weights ------------------------------------------------------------------
# The stroke stays vertical; we vary `stroke` and `cell` to densify.

REGULAR = Style(cell=14, stroke=4, column_mode="spaced", column_gap=3)
MEDIUM = Style(cell=14, stroke=6, column_mode="spaced", column_gap=2)
BOLD = Style(cell=14, stroke=9, column_mode="spaced", column_gap=2)

# --- Column modes -------------------------------------------------------------
# "solid": strokes touch → merge into blocks; only the letter's VOID remains.
# Consequence: very readable for E/F/L/T, unreadable for C/O/Q.
# Important conceptual note: "thin strokes THAT TOUCH" is a contradiction —
# as soon as two thin strokes touch, they form a block. Thinness is only visible
# with whitespace around them. So "no spacing" necessarily implies blocks.

SOLID = Style(cell=14, stroke=10, column_mode="solid")
SOLID_NARROW = Style(cell=14, stroke=6, column_mode="solid")
THIN_JOINED = Style(cell=14, stroke=3, column_mode="joined")

# --- Condensed / ultra-condensed ----------------------------------------------

CONDENSED = Style(cell=12, stroke=4, column_mode="spaced", column_gap=1)
ULTRA_CONDENSED = Style(cell=10, stroke=3, column_mode="joined")

# Ultra-compact: glyphs use the "joined" column packing (no intra-glyph gap)
# AND `tracking=1` so consecutive letters are separated by a single pixel —
# almost touching. The puce sits above the glyph body, so it stays readable
# even at this density.
ULTRA_COMPACT = Style(
    cell=10, stroke=3, column_mode="joined", tracking=1,
)


WEIGHTS: dict[str, Style] = {
    "regular": REGULAR,
    "medium": MEDIUM,
    "bold": BOLD,
}

MODES: dict[str, Style] = {
    "spaced": MEDIUM,
    "joined": THIN_JOINED,
    "solid": SOLID,
    "solid-narrow": SOLID_NARROW,
    "condensed": CONDENSED,
    "ultra-condensed": ULTRA_CONDENSED,
    "ultra-compact": ULTRA_COMPACT,
}


def style_for(weight: str = "medium", column_mode: str | None = None) -> Style:
    """Return a `Style` combining a weight and, optionally, a column mode.

    If `column_mode` is provided, it overrides the weight's column mode.
    """
    base = WEIGHTS.get(weight.lower())
    if base is None:
        raise ValueError(f"Unknown weight: {weight!r}. Available: {list(WEIGHTS)}")
    if column_mode:
        if column_mode.lower() not in {"spaced", "joined", "solid"}:
            raise ValueError(f"Unknown column mode: {column_mode!r}")
        base = replace(base, column_mode=column_mode.lower())
    return base
