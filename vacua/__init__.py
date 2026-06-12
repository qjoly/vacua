"""Vacua — modular negative-space font on a 5×9 grid.

A letter's shape is defined by the ABSENCE of vertical strokes in an otherwise
fully filled cell. See `vacua.alphabet.INK_BANDS` for the alphabet's source of
truth.
"""

from .alphabet import INK_BANDS, FULL, N_BANDS, N_COLS, available_chars, letter_filled, segs
from .render import (
    ACCENT_RED,
    DARK,
    INK_BLUE,
    PAPER,
    Style,
    compose_rotation_ligature,
    glyph_on,
    glyph_tile,
    render_chart,
    render_paired_text,
    render_text,
)
from .variants import (
    BOLD,
    CONDENSED,
    MEDIUM,
    MODES,
    REGULAR,
    SOLID,
    SOLID_NARROW,
    THIN_JOINED,
    ULTRA_CONDENSED,
    WEIGHTS,
    style_for,
)

__version__ = "0.1.0"

__all__ = [
    "INK_BANDS", "FULL", "N_BANDS", "N_COLS",
    "available_chars", "letter_filled", "segs",
    "Style", "glyph_tile", "glyph_on", "render_text", "render_chart", "render_paired_text",
    "compose_rotation_ligature",
    "INK_BLUE", "PAPER", "DARK", "ACCENT_RED",
    "REGULAR", "MEDIUM", "BOLD", "SOLID", "SOLID_NARROW", "THIN_JOINED",
    "CONDENSED", "ULTRA_CONDENSED", "WEIGHTS", "MODES", "style_for",
    "__version__",
]
