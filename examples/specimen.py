"""Specimen: full alphabet rendered in three weights, plus a word."""

from __future__ import annotations

from pathlib import Path

from vacua import BOLD, MEDIUM, REGULAR, render_chart, render_text

OUT = Path(__file__).resolve().parent.parent / "gallery"
OUT.mkdir(exist_ok=True)


def main() -> None:
    render_chart(style=REGULAR).save(OUT / "chart_regular.png")
    render_chart(style=MEDIUM).save(OUT / "chart_medium.png")
    render_chart(style=BOLD).save(OUT / "chart_bold.png")
    render_text("VACUA", style=BOLD).save(OUT / "word_vacua.png")
    print(f"Specimens written to {OUT}")


if __name__ == "__main__":
    main()
