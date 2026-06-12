# Full specification — Vacua

## 1. Principle

Vacua is a **modular**, **generative** **negative-space** font. The concept
fits in one sentence: each letter occupies a cell filled with vertical
strokes, and it is **the absence of some strokes — the void — that draws the
letter**. The shape is never marked by matter; it is marked by its absence.

Vacua is a **display/titling** font: the priority is visual impact and
concept, not body-text legibility.

**Lineage.** Vacua belongs to the family of modular typefaces (cf. Wim
Crouwel's *New Alphabet*, 1967) and generative typography (the glyphs are
produced by a deterministic script, not hand-drawn). It started as a variant
of a system called "Epetri" and has had its own identity since.

## 2. Grid

- **5 columns** (horizontal resolution)
- **9 bands** (vertical resolution, `0` = top, `8` = bottom)
- a **marker** at the top-left corner: a short stroke that signals the start
  of each letter and acts as a **delimiter** (no inter-letter space needed).

The 5-column system was preferred to 4 because it renders round letters
(C, O, Q) better.

## 3. Data model

```python
INK_BANDS[ch][col] = list of bands belonging to the letter's shape
                     (so they must be left EMPTY)
```

The **filled** bands (= drawn bars) are the complement:
`[b for b in range(9) if b not in INK_BANDS[ch][col]]`.

`FULL = [0..8]` means "column entirely emptied", because the whole column
belongs to the letter's shape.

## 4. Hand-tuned decisions

A few letters are **hand-tuned** because they were colliding:

| Letter | Correction |
|--------|------------|
| I | hollow serifs at top AND bottom |
| T | full bottom kept (without it, I and T are identical) |
| Y | sharp V of voids |
| Z | explicit staircase diagonal |

Do not "simplify" these definitions.

## 5. Accepted limitations

- **Angular** letters (E, F, H, I, L, T) read very well.
- **Round** ones (C, O, Q) and **diagonals** (K, X, Z) are more suggested
  than drawn — inherent to the 5-column resolution, and it reinforces the
  cryptic feel. Do not try to "fix" them.

## 6. Variants

| Variant | Effect |
|---------|--------|
| Regular / Medium / Bold | thin → medium → thick stroke; same voids |
| Solid | merged columns → blocks, only the void remains |
| Solid narrow | Solid with thin columns → slender glyph |
| Thin joined | thin strokes, tight columns but not merged |
| Condensed / ultra-condensed | narrower glyphs |

All variants are **parameters of the same renderer**, not separate alphabets.

## 7. Rotation ligatures

Two letters can be condensed: the 2nd one is the **entire glyph rotated 90°**.
Its strokes become horizontal *through the rotation*, not by a redesign. We
overlay a vertical and a horizontal letter → woven grid. The 2nd letter is
recovered by rotating the medium a quarter turn: an orientation-based cipher.

**Geometric pitfall.** The cell is 5×9, so it is NOT square. A 90° rotation
does not fit in the same box. You MUST use a square base
`span = max(5, 9) = 9` with a centering offset `offx = (9-5)/2 * cell` for
the vertical letter.

## 8. Reference colors

| Role | RGB |
|------|-----|
| Main ink (blue) | `(46, 111, 232)` |
| Paper | `(244, 242, 236)` |
| Dark | `(15, 27, 51)` |
| Accent (red, 2nd letter of a ligature) | `(225, 90, 60)` |
