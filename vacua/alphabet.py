"""
Vacua alphabet definition — SOURCE OF TRUTH.

Vacua is a negative-space font on a 5 columns × 9 bands grid. Each cell is
conceptually filled with vertical strokes; the letter's shape is obtained by
REMOVING the strokes where the letter passes.

`INK_BANDS[ch][col]` = list of bands (0 = top, 8 = bottom) that belong to the
letter's shape, i.e. the bands to leave EMPTY in that column. The FILLED bands
(actually drawn) are the complement.

KEY PITFALL: you do not draw the letter. You draw everything EXCEPT the letter.
"""

from __future__ import annotations

# Column entirely "drawn" by the letter (= every band emptied of vertical strokes).
FULL = list(range(9))

# Reserved character representing the inter-word space (no glyph rendered).
SPACE = " "

INK_BANDS: dict[str, dict[int, list[int]]] = {
    'A': {0: [2, 3, 4, 5, 6, 7, 8], 1: [0, 1, 4], 2: [0, 1, 4], 3: [0, 1, 4], 4: [2, 3, 4, 5, 6, 7, 8]},
    'B': {0: FULL, 1: [0, 4, 8], 2: [0, 4, 8], 3: [0, 4, 8], 4: [1, 2, 3, 5, 6, 7]},
    'C': {0: [2, 3, 4, 5, 6], 1: [0, 1, 7, 8], 2: [0, 8], 3: [0, 8], 4: [0, 1, 2, 6, 7, 8]},
    'D': {0: FULL, 1: [0, 8], 2: [0, 8], 3: [1, 7], 4: [2, 3, 4, 5, 6]},
    'E': {0: FULL, 1: [0, 4, 8], 2: [0, 4, 8], 3: [0, 4, 8], 4: [0, 4, 8]},
    'F': {0: FULL, 1: [0, 4], 2: [0, 4], 3: [0, 4], 4: [0]},
    'G': {0: [2, 3, 4, 5, 6], 1: [0, 1, 7, 8], 2: [0, 8], 3: [0, 4, 8], 4: [2, 3, 4, 8]},
    'H': {0: FULL, 1: [4], 2: [4], 3: [4], 4: FULL},
    # Hollow serifs at top AND bottom prevent confusion with T.
    'I': {0: [0, 1, 7, 8], 1: [0, 1, 7, 8], 2: FULL, 3: [0, 1, 7, 8], 4: [0, 1, 7, 8]},
    'J': {0: [7], 1: [8], 2: [8], 3: FULL, 4: [0, 1, 2, 3, 4, 5, 6, 7, 8]},
    'K': {0: FULL, 1: [4], 2: [3, 5], 3: [2, 6], 4: [0, 1, 7, 8]},
    'L': {0: FULL, 1: [8], 2: [8], 3: [8], 4: [8]},
    'M': {0: FULL, 1: [1, 2], 2: [3, 4], 3: [1, 2], 4: FULL},
    'N': {0: FULL, 1: [2, 3], 2: [4], 3: [5, 6], 4: FULL},
    'O': {0: [2, 3, 4, 5, 6], 1: [0, 1, 7, 8], 2: [0, 8], 3: [0, 1, 7, 8], 4: [2, 3, 4, 5, 6]},
    'P': {0: FULL, 1: [0, 4], 2: [0, 4], 3: [0, 4], 4: [1, 2, 3]},
    'Q': {0: [2, 3, 4, 5, 6], 1: [0, 1, 7, 8], 2: [0, 8], 3: [0, 1, 7], 4: [2, 3, 4, 5, 6, 8]},
    'R': {0: FULL, 1: [0, 4], 2: [0, 4], 3: [0, 4, 6], 4: [1, 2, 3, 7, 8]},
    'S': {0: [0, 1, 2, 8], 1: [0, 4, 8], 2: [0, 4, 8], 3: [0, 4, 8], 4: [0, 6, 7, 8]},
    # T's full bottom distinguishes it from I (otherwise the two glyphs are identical).
    'T': {0: [0, 1], 1: [0, 1], 2: FULL, 3: [0, 1], 4: [0, 1]},
    'U': {0: [0, 1, 2, 3, 4, 5, 6, 7], 1: [8], 2: [8], 3: [8], 4: [0, 1, 2, 3, 4, 5, 6, 7]},
    'V': {0: [0, 1, 2, 3, 4], 1: [5, 6], 2: [7, 8], 3: [5, 6], 4: [0, 1, 2, 3, 4]},
    'W': {0: FULL, 1: [6, 7], 2: [4, 5], 3: [6, 7], 4: FULL},
    'X': {0: [0, 1, 7, 8], 1: [2, 3, 5, 6], 2: [4], 3: [2, 3, 5, 6], 4: [0, 1, 7, 8]},
    # Sharp V of voids to avoid confusion with T/I.
    'Y': {0: [0, 1, 2, 3], 1: [2, 3, 4], 2: FULL, 3: [2, 3, 4], 4: [0, 1, 2, 3]},
    # Explicit staircase diagonal.
    'Z': {0: [0, 1, 7, 8], 1: [0, 1, 6, 7, 8], 2: [0, 1, 4, 7, 8], 3: [0, 1, 2, 7, 8], 4: [0, 1, 7, 8]},
    '?': {0: [1, 8], 1: [0, 3], 2: [0, 4, 5, 8], 3: [0, 3], 4: [1, 2]},
}

# Canonical glyph grid dimensions.
N_COLS = 5
N_BANDS = 9


def letter_filled(ch: str) -> dict[int, list[int]]:
    """FILLED bands (= vertical strokes to draw) per column, for `ch`.

    Complement of INK_BANDS: everything that is not part of the letter's shape.
    """
    ch = ch.upper()
    if ch not in INK_BANDS:
        raise KeyError(f"Character not defined in Vacua: {ch!r}")
    ink = INK_BANDS[ch]
    return {col: [b for b in range(N_BANDS) if b not in ink[col]] for col in range(N_COLS)}


def segs(bands: list[int]) -> list[tuple[int, int]]:
    """Merge a list of contiguous bands into segments (start, end_inclusive).

    Example: [0, 1, 2, 5, 6] → [(0, 2), (5, 6)]. Useful to reduce the number of
    primitives at render time (image or 3D).
    """
    if not bands:
        return []
    bands = sorted(set(bands))
    out: list[tuple[int, int]] = []
    start = prev = bands[0]
    for b in bands[1:]:
        if b == prev + 1:
            prev = b
        else:
            out.append((start, prev))
            start = prev = b
    out.append((start, prev))
    return out


def available_chars() -> list[str]:
    """Defined characters: A-Z in alphabetical order, then punctuation.

    We do NOT sort by raw ASCII: otherwise `?` (63) would come before `A` (65),
    which would put the question mark at the head of the specimen chart.
    """
    letters = sorted(c for c in INK_BANDS if c.isalpha())
    others = sorted(c for c in INK_BANDS if not c.isalpha())
    return letters + others
