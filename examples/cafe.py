"""Render the word CAFE in several variants."""

from __future__ import annotations

from pathlib import Path

from vacua import MEDIUM, SOLID, THIN_JOINED, render_text

OUT = Path(__file__).resolve().parent.parent / "gallery"
OUT.mkdir(exist_ok=True)


def main() -> None:
    render_text("CAFE", style=MEDIUM).save(OUT / "cafe_medium.png")
    render_text("CAFE", style=SOLID).save(OUT / "cafe_solid.png")
    render_text("CAFE", style=THIN_JOINED).save(OUT / "cafe_thin_joined.png")
    print("CAFE rendered in 3 variants.")


if __name__ == "__main__":
    main()
