# Pitfalls to know

These pitfalls came up during the design. They are recalled in the code where
relevant, but centralized here for newcomers.

## Conceptual

### You draw the VOID, not the letter

The most common mistake when porting the system elsewhere: drawing the
letter as in a classic design. **NO.** You start from a cell full of vertical
strokes and **remove** the strokes where the letter passes. `INK_BANDS[ch][col]`
lists the *emptied* bands, not the *drawn* bands.

### "Thin strokes that touch" is a contradiction

As soon as two thin strokes touch, they form a block. Thinness is only
visible with whitespace around. So `solid` mode necessarily produces full
blocks — this is intentional.

## Geometric

### The 5×9 cell is not square

For any rotation (especially 90° rotation ligatures), you need a square base
`span = max(N_COLS, N_BANDS) = 9` with a centering offset for the vertical
letter. Otherwise the rotated glyph overflows.

See `compose_rotation_ligature` in `vacua/render.py`.
