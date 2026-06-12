# 3D printing Vacua

Vacua is made of **straight segments only**, so it lends itself well to
3D printing, laser engraving and CNC.

## Recommended pipeline

1. Generate the `.scad` with the Python wrapper:
   ```bash
   python -m vacua "VACUA" --scad --out out/vacua.scad
   ```
   (The wrapper includes `scad/vacua_param.scad`; place the wrapper in the
   `scad/` folder so the `include <vacua_param.scad>` resolves.)

2. Open the `.scad` in OpenSCAD, tweak as needed:
   - `cell`, `bar_w` (size / bar thickness)
   - `relief_h`, `base_h` (thickness)
   - `merged = true` for a single plate
   - `with_keyring = true` for a keychain

3. Export as STL → slice → print.

## Exposed parameters

| Variable | Role |
|----------|------|
| `text` | string to engrave |
| `cell` | sub-cell size (mm) |
| `bar_w` | stroke thickness |
| `relief_h` | relief height |
| `base_h` | plate thickness |
| `tile_margin` | margin around the glyph inside its tile |
| `tile_gap` | gap between tiles (non-merged mode) |
| `plate_border` | border of the shared plate |
| `plate_r` | rounded-corner radius |
| `puce_on` | enable the letter-start marker |
| `round_bars` | cylindrical bars instead of cuboids |
| `cols_tiles` | number of tile columns (0 = single line) |
| `merged` | shared plate (true) or separate tiles (false) |
| `with_keyring` | add a keyring |
| `ring_outer`, `ring_inner`, `ring_overlap` | keyring geometry |
