"""Rotation ligature: the 2nd letter is the entire glyph rotated 90°.

You read the 2nd letter by rotating the medium a quarter turn: an
orientation-based cipher. Since the cell is 5×9, the tile is rendered square
to allow rotation without overflow.
"""

from __future__ import annotations

from pathlib import Path

from vacua import BOLD, compose_rotation_ligature

OUT = Path(__file__).resolve().parent.parent / "gallery"
OUT.mkdir(exist_ok=True)


def main() -> None:
    for v, r in [("V", "B"), ("A", "C"), ("E", "T"), ("O", "X")]:
        img = compose_rotation_ligature(v, r, style=BOLD)
        img.save(OUT / f"ligature_{v}_{r}.png")
    print("Rotation ligatures rendered.")


if __name__ == "__main__":
    main()
