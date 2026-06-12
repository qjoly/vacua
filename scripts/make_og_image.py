"""Generate docs/og.png — 1200×630 social share card for Vacua."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from vacua import BOLD, PAPER, render_text
from vacua.render import DARK, INK_BLUE
from vacua.variants import style_for

OUT = Path(__file__).resolve().parent.parent / "docs" / "og.png"
W, H = 1200, 630


def _try_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Futura.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> None:
    canvas = Image.new("RGBA", (W, H), PAPER)

    style = style_for("bold", "spaced")
    word = render_text("VACUA", style=style, background=(0, 0, 0, 0), margin=0)

    target_w = int(W * 0.78)
    scale = target_w / word.width
    new_size = (int(word.width * scale), int(word.height * scale))
    word = word.resize(new_size, Image.LANCZOS)

    wx = (W - word.width) // 2
    wy = int(H * 0.30)
    canvas.alpha_composite(word, (wx, wy))

    draw = ImageDraw.Draw(canvas)

    title_font = _try_font(46)
    tag_font = _try_font(26)

    title = "VACUA"
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, int(H * 0.08)), title, font=title_font, fill=DARK)

    tagline = "a negative-space font  ·  5 × 9 grid  ·  the void is the letter"
    tagw = draw.textlength(tagline, font=tag_font)
    draw.text(((W - tagw) / 2, int(H * 0.84)), tagline, font=tag_font, fill=INK_BLUE)

    bar_y = int(H * 0.93)
    draw.rectangle([(W // 2 - 60, bar_y), (W // 2 + 60, bar_y + 4)], fill=DARK)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({W}×{H})")


if __name__ == "__main__":
    main()
