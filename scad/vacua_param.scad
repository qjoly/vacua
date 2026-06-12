// =============================================================================
// vacua_param.scad — standalone parametric generator for Vacua plates.
//
// Vacua: negative-space font on a 5 columns × 9 bands grid.
// Each column of a cell is conceptually filled with vertical strokes.
// We REMOVE the strokes where the letter's shape passes: the void draws the letter.
//
// The full alphabet is hard-coded below as tables indexed by character (via a
// lookup function). Editing `text` regenerates the model.
//
// PITFALLS TO MIND:
//   - Non-manifold: bars that cross at the same height produce coincident
//     faces (the "may not be a valid 2-manifold" warning).
//     Solution: (a) wrap each glyph in `union()`, (b) anchor the bars slightly
//     INSIDE the base (start at base_h - 0.4, height relief_h + 0.4).
//   - 90° rotation: the cell is 5×9, so NOT square. For rotation ligatures
//     you MUST work on a square 9×9 base with centering offset
//     offx = (9-5)/2 * cell. (Not used in this file but good to know for
//     variants.)
// =============================================================================

// -------- USER PARAMETERS ---------------------------------------------------
text          = "VACUA";    // Text to engrave (A-Z and ? are supported).
cols_tiles    = 0;          // Number of tile columns; 0 = everything on one line.
merged        = true;       // true: a single shared plate; false: separate tiles.
with_keyring  = false;      // true: adds a keyring on the first tile.

// Grid geometry (mm).
cell          = 2.6;        // Sub-cell size (1 column × 1 band).
bar_w         = 1.2;        // Vertical-stroke thickness.
relief_h      = 1.6;        // Relief height above the base.
base_h        = 1.8;        // Base/plate thickness.
tile_margin   = 1.6;        // Margin around the glyph inside its tile.
tile_gap      = 1.2;        // Gap between tiles (non-merged mode).
plate_border  = 2.4;        // Plate border (merged mode).
plate_r       = 2.5;        // Rounded-corner radius of the plate.
puce_on       = true;       // Show the marker at the top-left of each glyph.
round_bars    = false;      // true: cylindrical bars; false: cuboids.

// Keyring.
ring_outer    = 6.5;
ring_inner    = 3.0;
ring_overlap  = 2.0;        // Overlap depth with the first tile.

$fn = 32;

// -------- ALPHABET TABLE ----------------------------------------------------
// INK_BANDS[col] = list of EMPTY bands (= letter passes here).
// Convention: 0 = top, 8 = bottom. FULL = [0..8] = column entirely emptied.
// FILLED bands (= bars to draw) are the complement.
//
// The `ink_bands(ch, col)` function returns the vector for (ch, col).

function ink_bands(ch, col) =
    (ch == "A") ? [[2,3,4,5,6,7,8],[0,1,4],[0,1,4],[0,1,4],[2,3,4,5,6,7,8]][col] :
    (ch == "B") ? [[0,1,2,3,4,5,6,7,8],[0,4,8],[0,4,8],[0,4,8],[1,2,3,5,6,7]][col] :
    (ch == "C") ? [[2,3,4,5,6],[0,1,7,8],[0,8],[0,8],[0,1,2,6,7,8]][col] :
    (ch == "D") ? [[0,1,2,3,4,5,6,7,8],[0,8],[0,8],[1,7],[2,3,4,5,6]][col] :
    (ch == "E") ? [[0,1,2,3,4,5,6,7,8],[0,4,8],[0,4,8],[0,4,8],[0,4,8]][col] :
    (ch == "F") ? [[0,1,2,3,4,5,6,7,8],[0,4],[0,4],[0,4],[0]][col] :
    (ch == "G") ? [[2,3,4,5,6],[0,1,7,8],[0,8],[0,4,8],[2,3,4,8]][col] :
    (ch == "H") ? [[0,1,2,3,4,5,6,7,8],[4],[4],[4],[0,1,2,3,4,5,6,7,8]][col] :
    (ch == "I") ? [[0,1,7,8],[0,1,7,8],[0,1,2,3,4,5,6,7,8],[0,1,7,8],[0,1,7,8]][col] :
    (ch == "J") ? [[7],[8],[8],[0,1,2,3,4,5,6,7,8],[0,1,2,3,4,5,6,7,8]][col] :
    (ch == "K") ? [[0,1,2,3,4,5,6,7,8],[4],[3,5],[2,6],[0,1,7,8]][col] :
    (ch == "L") ? [[0,1,2,3,4,5,6,7,8],[8],[8],[8],[8]][col] :
    (ch == "M") ? [[0,1,2,3,4,5,6,7,8],[1,2],[3,4],[1,2],[0,1,2,3,4,5,6,7,8]][col] :
    (ch == "N") ? [[0,1,2,3,4,5,6,7,8],[2,3],[4],[5,6],[0,1,2,3,4,5,6,7,8]][col] :
    (ch == "O") ? [[2,3,4,5,6],[0,1,7,8],[0,8],[0,1,7,8],[2,3,4,5,6]][col] :
    (ch == "P") ? [[0,1,2,3,4,5,6,7,8],[0,4],[0,4],[0,4],[1,2,3]][col] :
    (ch == "Q") ? [[2,3,4,5,6],[0,1,7,8],[0,8],[0,1,7],[2,3,4,5,6,8]][col] :
    (ch == "R") ? [[0,1,2,3,4,5,6,7,8],[0,4],[0,4],[0,4,6],[1,2,3,7,8]][col] :
    (ch == "S") ? [[0,1,2,8],[0,4,8],[0,4,8],[0,4,8],[0,6,7,8]][col] :
    (ch == "T") ? [[0,1],[0,1],[0,1,2,3,4,5,6,7,8],[0,1],[0,1]][col] :
    (ch == "U") ? [[0,1,2,3,4,5,6,7],[8],[8],[8],[0,1,2,3,4,5,6,7]][col] :
    (ch == "V") ? [[0,1,2,3,4],[5,6],[7,8],[5,6],[0,1,2,3,4]][col] :
    (ch == "W") ? [[0,1,2,3,4,5,6,7,8],[6,7],[4,5],[6,7],[0,1,2,3,4,5,6,7,8]][col] :
    (ch == "X") ? [[0,1,7,8],[2,3,5,6],[4],[2,3,5,6],[0,1,7,8]][col] :
    (ch == "Y") ? [[0,1,2,3],[2,3,4],[0,1,2,3,4,5,6,7,8],[2,3,4],[0,1,2,3]][col] :
    (ch == "Z") ? [[0,1,7,8],[0,1,6,7,8],[0,1,4,7,8],[0,1,2,7,8],[0,1,7,8]][col] :
    (ch == "?") ? [[1,8],[0,3],[0,4,5,8],[0,3],[1,2]][col] :
    [];

// Filled band at (ch, col, b)? True if `b` is NOT in INK_BANDS[ch][col].
function is_filled(ch, col, b) =
    len(search([b], ink_bands(ch, col))[0]) == 0;

// -------- PRIMITIVES --------------------------------------------------------
N_COLS  = 5;
N_BANDS = 9;
GLYPH_W = N_COLS  * cell;
GLYPH_H = N_BANDS * cell;

// One vertical bar, anchored into the base (cf. anti non-manifold).
module bar(x, y_top, y_bot) {
    h = (y_bot - y_top) + 0.4 + relief_h;
    translate([x, y_top, base_h - 0.4])
        if (round_bars)
            translate([bar_w/2, (y_bot - y_top)/2, 0])
                cylinder(h = h, r = bar_w/2);
        else
            cube([bar_w, y_bot - y_top, h]);
}

// Top-left marker, acts as a visual/reading delimiter.
module puce(x0, y0) {
    if (puce_on) {
        translate([x0, y0 + GLYPH_H + 0.4, base_h - 0.4])
            cube([cell * 1.2, max(bar_w, 0.8), relief_h + 0.4]);
    }
}

// A full glyph (ch) placed at (x0, y0), wrapped in union() (anti non-manifold).
module glyph(ch, x0, y0) {
    union() {
        puce(x0, y0);
        for (col = [0 : N_COLS - 1]) {
            // Walk the bands and draw the contiguous filled segments.
            // No dynamic table: one bar per filled band (will be merged by union()).
            for (b = [0 : N_BANDS - 1]) {
                if (is_filled(ch, col, b)) {
                    x = x0 + col * cell + (cell - bar_w) / 2;
                    // y screen axis: 0 at the top → invert for SCAD (Y up).
                    y_top = y0 + (N_BANDS - 1 - b) * cell;
                    y_bot = y_top + cell;
                    bar(x, y_top, y_bot);
                }
            }
        }
    }
}

// Rounded plate (hull of 4 corner cylinders) — a single printable object.
module rounded_plate(w, h, r, t) {
    hull() {
        translate([r,        r,        0]) cylinder(h = t, r = r);
        translate([w - r,    r,        0]) cylinder(h = t, r = r);
        translate([r,        h - r,    0]) cylinder(h = t, r = r);
        translate([w - r,    h - r,    0]) cylinder(h = t, r = r);
    }
}

// Keyring, overlaps the first tile.
module keyring(x_left, y_center) {
    translate([x_left - ring_outer + ring_overlap, y_center, 0])
        difference() {
            cylinder(h = base_h, r = ring_outer);
            translate([0, 0, -0.5]) cylinder(h = base_h + 1, r = ring_inner);
        }
}

// -------- TEXT COMPOSITION --------------------------------------------------
// Iterate over the characters, build each glyph's position, then place all
// reliefs on ONE shared plate (merged mode) or on separate tiles.

function char_at(s, i) = (i >= len(s)) ? "" : s[i];
function n_chars(s) = len(s);

NTXT = n_chars(text);
ROWS = (cols_tiles == 0) ? 1 : ceil(NTXT / cols_tiles);
COLS = (cols_tiles == 0) ? NTXT : cols_tiles;

TILE_W = GLYPH_W + 2 * tile_margin;
TILE_H = GLYPH_H + 2 * tile_margin + bar_w + 0.8; // marker margin
STEP_X = TILE_W + (merged ? 0 : tile_gap);
STEP_Y = TILE_H + (merged ? 0 : tile_gap);

PLATE_W = COLS * TILE_W + 2 * plate_border;
PLATE_H = ROWS * TILE_H + 2 * plate_border;

module compose() {
    if (merged) {
        union() {
            rounded_plate(PLATE_W, PLATE_H, plate_r, base_h);
            if (with_keyring) keyring(plate_border, plate_border + TILE_H / 2);
            for (i = [0 : NTXT - 1]) {
                r = floor(i / COLS);
                c = i - r * COLS;
                x0 = plate_border + c * TILE_W + tile_margin;
                y0 = plate_border + (ROWS - 1 - r) * TILE_H + tile_margin;
                glyph(char_at(text, i), x0, y0);
            }
        }
    } else {
        for (i = [0 : NTXT - 1]) {
            r = floor(i / COLS);
            c = i - r * COLS;
            tx = c * STEP_X;
            ty = (ROWS - 1 - r) * STEP_Y;
            translate([tx, ty, 0]) {
                union() {
                    rounded_plate(TILE_W, TILE_H, plate_r, base_h);
                    if (with_keyring && i == 0)
                        keyring(0, TILE_H / 2);
                    glyph(char_at(text, i), tile_margin, tile_margin);
                }
            }
        }
    }
}

compose();
