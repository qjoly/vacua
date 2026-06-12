"""Image rendering tests — determinism and invariants."""

from __future__ import annotations

import hashlib
import io

import pytest

from vacua import (
    Style,
    available_chars,
    compose_rotation_ligature,
    glyph_tile,
    render_chart,
    render_text,
    style_for,
)


def _digest(img) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return hashlib.sha256(buf.getvalue()).hexdigest()


class TestDeterminism:
    def test_same_text_same_pixels(self) -> None:
        a = render_text("VACUA")
        b = render_text("VACUA")
        assert _digest(a) == _digest(b)

    def test_same_chart_same_pixels(self) -> None:
        assert _digest(render_chart()) == _digest(render_chart())

    def test_glyph_tile_square(self) -> None:
        """The tile is square: prerequisite for 90° rotation without overflow."""
        for ch in available_chars():
            t = glyph_tile(ch)
            assert t.width == t.height, f"{ch}: non-square tile ({t.size})"


class TestVariants:
    @pytest.mark.parametrize("weight", ["regular", "medium", "bold"])
    def test_weights_render(self, weight: str) -> None:
        img = render_text("ABC", style=style_for(weight))
        assert img.width > 0 and img.height > 0

    @pytest.mark.parametrize("mode", ["spaced", "joined", "solid"])
    def test_modes_render(self, mode: str) -> None:
        img = render_text("EFLT", style=style_for("medium", mode))
        assert img.width > 0 and img.height > 0

    def test_unknown_weight_raises(self) -> None:
        with pytest.raises(ValueError):
            style_for("ultralight")  # type: ignore[arg-type]


class TestRotationLigature:
    def test_ligature_canvas_is_square(self) -> None:
        """A rotation ligature's base must be square (conceptually 9×9)."""
        img = compose_rotation_ligature("A", "B")
        assert img.width == img.height

    def test_ligature_uses_two_colors(self) -> None:
        img = compose_rotation_ligature("V", "B").convert("RGB")
        colors = {img.getpixel((x, y)) for x in range(0, img.width, 4) for y in range(0, img.height, 4)}
        # At least 3 colors: paper, blue, red.
        assert len(colors) >= 3
