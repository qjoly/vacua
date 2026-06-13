"""
Canonical image rendering for Vacua.

All image outputs (specimens, chart, ligatures) MUST go through
`glyph_tile` / `glyph_on` to guarantee identical rendering everywhere.

Strategy: supersampling (×SS) then LANCZOS downscale → crisp edges without aliasing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from PIL import Image, ImageDraw

from .alphabet import INK_BANDS, N_BANDS, N_COLS, SPACE, letter_filled, segs

# Project reference colors.
INK_BLUE = (46, 111, 232, 255)
PAPER = (244, 242, 236, 255)
DARK = (15, 27, 51, 255)
ACCENT_RED = (225, 90, 60, 255)

# Supersampling factor for the LANCZOS downscale.
SS = 4


@dataclass(frozen=True)
class Style:
    """Rendering parameters for a glyph.

    - `cell`: size of a sub-cell (1 column × 1 band) in pixels.
    - `stroke`: thickness of the vertical stroke, in pixels (before SS).
    - `column_mode`: "spaced" (separated columns), "joined" (tight but not
      merged), "solid" (merged → full blocks).
    - `column_gap`: gap between columns for "spaced" (px).
    - `puce`: display the letter-start marker.
    - `color`: stroke color.
    """

    cell: int = 12
    stroke: int = 6
    column_mode: str = "spaced"  # "spaced" | "joined" | "solid"
    column_gap: int = 2
    puce: bool = True
    color: tuple[int, int, int, int] = INK_BLUE
    tracking: int | None = None  # inter-glyph spacing in px; None → cell // 2


def _column_x_offsets(style: Style) -> list[int]:
    """X position (left) of each column inside the glyph cell."""
    if style.column_mode == "solid":
        # Adjacent columns: a column's width = stroke (strokes touch each other).
        return [c * style.stroke for c in range(N_COLS)]
    if style.column_mode == "joined":
        # Tight columns with 1 px of play — thin stroke remains visible.
        step = style.stroke + 1
        return [c * step for c in range(N_COLS)]
    # "spaced"
    step = style.stroke + style.column_gap
    # Center within a wide cell = `cell` per column.
    return [c * style.cell + (style.cell - style.stroke) // 2 for c in range(N_COLS)]


def glyph_width(style: Style) -> int:
    """Total glyph width in pixels (before SS)."""
    if style.column_mode == "solid":
        return N_COLS * style.stroke
    if style.column_mode == "joined":
        return N_COLS * (style.stroke + 1)
    return N_COLS * style.cell


def glyph_height(style: Style) -> int:
    """Total glyph height in pixels (before SS)."""
    return N_BANDS * style.cell


def _draw_glyph_ss(draw: ImageDraw.ImageDraw, ch: str, x0: int, y0: int, style: Style) -> None:
    """Draw a glyph into `draw` at (x0, y0), in already-supersampled coordinates."""
    ss = SS
    color = style.color
    cell = style.cell * ss
    stroke = style.stroke * ss

    xs = [v * ss for v in _column_x_offsets(style)]
    filled = letter_filled(ch)

    for col in range(N_COLS):
        for a, b in segs(filled[col]):
            x = x0 + xs[col]
            y_top = y0 + a * cell
            y_bot = y0 + (b + 1) * cell
            draw.rectangle([x, y_top, x + stroke, y_bot], fill=color)

    if style.puce:
        # Marker: short horizontal stroke at the top-left, indicating the letter start.
        # Sized to read clearly — wider than a bar, ~half a bar tall.
        puce_w = max(int(stroke * 1.6), cell * 7 // 10)
        puce_h = max(ss * 2, stroke * 55 // 100)
        draw.rectangle(
            [x0, y0 - puce_h - ss * 2, x0 + puce_w, y0 - ss * 2],
            fill=color,
        )


def glyph_tile(ch: str, style: Style | None = None, rotated: bool = False) -> Image.Image:
    """Render ONE glyph onto a square RGBA layer (base = max(w, h)).

    The square base is required for the 90° rotation (cf. ligatures): a 5×9 cell
    is NOT square, so rotating without a square base would overflow.
    """
    style = style or Style()
    w = glyph_width(style)
    h = glyph_height(style)
    span = max(w, h)
    offx = (span - w) // 2
    offy = (span - h) // 2

    ss = SS
    img = Image.new("RGBA", (span * ss, span * ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    _draw_glyph_ss(draw, ch, offx * ss, offy * ss, style)
    img = img.resize((span, span), Image.LANCZOS)

    if rotated:
        # 90° counter-clockwise rotation. Vertical strokes become horizontal.
        img = img.rotate(90, expand=False, resample=Image.BICUBIC)
    return img


def glyph_on(
    canvas: Image.Image,
    ch: str,
    x: int,
    y: int,
    style: Style | None = None,
    rotated: bool = False,
) -> int:
    """Compose a glyph onto `canvas` at (x, y). Returns the new X position (advance)."""
    style = style or Style()
    if ch == SPACE:
        return x + glyph_width(style)

    tile = glyph_tile(ch, style=style, rotated=rotated)
    span = tile.width
    # Place the (square) tile so that the glyph (centered in the tile) lands at (x, y).
    offx = (span - glyph_width(style)) // 2
    offy = (span - glyph_height(style)) // 2
    canvas.alpha_composite(tile, (x - offx, y - offy))
    tracking = style.cell // 2 if style.tracking is None else style.tracking
    return x + glyph_width(style) + tracking


def render_text(
    text: str,
    style: Style | None = None,
    background: tuple[int, int, int, int] = PAPER,
    margin: int = 24,
) -> Image.Image:
    """Render a string. Unknown characters are ignored."""
    style = style or Style()
    text = text.upper()

    gw = glyph_width(style)
    gh = glyph_height(style)
    tracking = style.cell // 2 if style.tracking is None else style.tracking
    advance = gw + tracking

    visible = [c for c in text if c == SPACE or c in INK_BANDS]
    width = margin * 2 + max(0, sum(advance for _ in visible) - tracking)
    width = max(width, gw + 2 * margin)
    height = margin * 2 + gh + (style.stroke + 4)  # +margin for the marker

    img = Image.new("RGBA", (width, height), background)
    x = margin
    y = margin + (style.stroke + 4)
    for ch in text:
        if ch == SPACE:
            x += advance
            continue
        try:
            x = glyph_on(img, ch, x, y, style=style)
        except KeyError:
            # Undefined character → silently ignored.
            continue
    return img


def render_chart(
    style: Style | None = None,
    cols: int = 6,
    background: tuple[int, int, int, int] = PAPER,
    margin: int = 32,
    chars: Iterable[str] | None = None,
) -> Image.Image:
    """Specimen chart A-Z (+ ?) laid out on a `cols`-column grid."""
    style = style or Style()
    from .alphabet import available_chars
    items = list(chars) if chars is not None else available_chars()

    gw = glyph_width(style)
    gh = glyph_height(style)
    pad_x = style.cell * 2
    pad_y = style.cell * 2
    cell_w = gw + pad_x
    cell_h = gh + pad_y + (style.stroke + 4)

    rows = (len(items) + cols - 1) // cols
    width = margin * 2 + cols * cell_w
    height = margin * 2 + rows * cell_h

    img = Image.new("RGBA", (width, height), background)
    for i, ch in enumerate(items):
        r, c = divmod(i, cols)
        x = margin + c * cell_w + pad_x // 2
        y = margin + r * cell_h + pad_y // 2 + (style.stroke + 4)
        glyph_on(img, ch, x, y, style=style)
    return img


def render_paired_text(
    text: str,
    style: Style | None = None,
    background: tuple[int, int, int, int] = PAPER,
    margin: int = 24,
    pair_gap: int | None = None,
    color_rotated: tuple[int, int, int, int] = ACCENT_RED,
    mono: bool = False,
) -> Image.Image:
    """Render a word as OVERLAID letter PAIRS (2nd letter rotated 90°).

    Example: "CAFE" → tile[C + rotated A] | tile[F + rotated E] side by side.
    If the word has an ODD number of letters, the last one is rendered alone
    (no rotation), in a cell of the same size.

    Spaces in `text` insert a break: the current pair is interrupted, a visual
    space is skipped, and a new pair starts.
    """
    style = style or Style()
    text = text.upper()
    # In mono mode, the rotated letter uses the same color as the vertical one.
    # Caveat: in monochrome, the two glyphs become visually indistinguishable
    # by color — reading relies purely on orientation (vertical vs. horizontal).
    style_r = Style(
        cell=style.cell, stroke=style.stroke, column_mode=style.column_mode,
        column_gap=style.column_gap, puce=style.puce,
        color=style.color if mono else color_rotated,
    )

    # Build the list of tiles to compose: each entry is either
    # ("pair", a, b), ("single", a), or ("space",).
    items: list[tuple] = []
    buf: list[str] = []
    for ch in text:
        if ch == SPACE:
            if buf:
                # Orphan letter before the space: rendered solo.
                items.append(("single", buf.pop()))
            items.append(("space",))
            continue
        if ch not in INK_BANDS:
            continue
        buf.append(ch)
        if len(buf) == 2:
            items.append(("pair", buf[0], buf[1]))
            buf.clear()
    if buf:
        items.append(("single", buf[0]))

    # A tile is `span = max(gw, gh)` (square base); at equal width, pairs and
    # singles align vertically.
    tile_size = max(glyph_width(style), glyph_height(style))
    gap = tile_size // 6 if pair_gap is None else pair_gap

    n_visual = sum(1 for it in items if it[0] != "space")
    n_spaces = sum(1 for it in items if it[0] == "space")
    width = margin * 2 + n_visual * tile_size + max(0, n_visual - 1) * gap + n_spaces * tile_size // 2
    height = margin * 2 + tile_size + (style.stroke + 4)

    img = Image.new("RGBA", (width, height), background)
    x = margin
    y = margin + (style.stroke + 4)
    for it in items:
        if it[0] == "space":
            x += tile_size // 2
            continue
        if it[0] == "pair":
            _, a, b = it
            tile_v = glyph_tile(a, style=style, rotated=False)
            tile_r = glyph_tile(b, style=style_r, rotated=True)
            img.alpha_composite(tile_v, (x, y))
            img.alpha_composite(tile_r, (x, y))
        else:  # single
            _, a = it
            tile_v = glyph_tile(a, style=style, rotated=False)
            img.alpha_composite(tile_v, (x, y))
        x += tile_size + gap
    return img


def compose_rotation_ligature(
    ch_vertical: str,
    ch_rotated: str,
    style: Style | None = None,
    background: tuple[int, int, int, int] = PAPER,
    margin: int = 24,
    color_rotated: tuple[int, int, int, int] = ACCENT_RED,
) -> Image.Image:
    """90° rotation ligature: `ch_vertical` (normal) + `ch_rotated` (rotated).

    PITFALL: the cell is 5×9, so we work on a square base span = max(5, 9) * cell
    = 9 * cell. The vertical letter is horizontally centered; the rotated letter
    covers the whole base after rotation.
    """
    style = style or Style()
    tile_v = glyph_tile(ch_vertical, style=style, rotated=False)
    # Build a copy of the style with the accent color for the 2nd letter.
    style_r = Style(
        cell=style.cell, stroke=style.stroke, column_mode=style.column_mode,
        column_gap=style.column_gap, puce=style.puce, color=color_rotated,
    )
    tile_r = glyph_tile(ch_rotated, style=style_r, rotated=True)

    span = tile_v.width
    width = span + margin * 2
    height = span + margin * 2
    img = Image.new("RGBA", (width, height), background)
    img.alpha_composite(tile_v, (margin, margin))
    img.alpha_composite(tile_r, (margin, margin))
    return img
