"""Vacua alphabet tests — completeness, determinism, structure."""

from __future__ import annotations

import string

import pytest

from vacua.alphabet import (
    FULL,
    INK_BANDS,
    N_BANDS,
    N_COLS,
    available_chars,
    letter_filled,
    segs,
)


class TestAlphabet:
    def test_full_constant_matches_grid(self) -> None:
        assert FULL == list(range(N_BANDS))

    def test_alphabet_complete(self) -> None:
        """A-Z + ? must all be defined."""
        expected = set(string.ascii_uppercase) | {"?"}
        assert set(INK_BANDS.keys()) == expected

    @pytest.mark.parametrize("ch", sorted(INK_BANDS.keys()))
    def test_each_glyph_has_five_columns(self, ch: str) -> None:
        assert set(INK_BANDS[ch].keys()) == set(range(N_COLS))

    @pytest.mark.parametrize("ch", sorted(INK_BANDS.keys()))
    def test_bands_are_in_range(self, ch: str) -> None:
        for col, bands in INK_BANDS[ch].items():
            for b in bands:
                assert 0 <= b < N_BANDS, f"{ch} col {col} band {b} out of range"

    @pytest.mark.parametrize("ch", sorted(INK_BANDS.keys()))
    def test_letter_has_some_void(self, ch: str) -> None:
        """An invisible letter (zero void) would be a bug: there must be a shape."""
        total_void = sum(len(b) for b in INK_BANDS[ch].values())
        assert total_void > 0, f"{ch} has no visible stroke"

    @pytest.mark.parametrize("ch", sorted(INK_BANDS.keys()))
    def test_letter_has_some_filled(self, ch: str) -> None:
        """A 100% empty letter (FULL everywhere) would have no bars left — not a letter."""
        all_full = all(set(INK_BANDS[ch][col]) == set(FULL) for col in range(N_COLS))
        assert not all_full, f"{ch} has all its columns emptied (FULL everywhere)"


class TestDeterminism:
    def test_letter_filled_is_complement(self) -> None:
        for ch in INK_BANDS:
            filled = letter_filled(ch)
            for col in range(N_COLS):
                expected = [b for b in range(N_BANDS) if b not in INK_BANDS[ch][col]]
                assert filled[col] == expected

    def test_letter_filled_case_insensitive(self) -> None:
        assert letter_filled("a") == letter_filled("A")

    def test_letter_filled_unknown_raises(self) -> None:
        with pytest.raises(KeyError):
            letter_filled("@")

    def test_same_input_same_output(self) -> None:
        for ch in INK_BANDS:
            assert letter_filled(ch) == letter_filled(ch)


class TestSegments:
    def test_empty(self) -> None:
        assert segs([]) == []

    def test_single(self) -> None:
        assert segs([3]) == [(3, 3)]

    def test_contiguous(self) -> None:
        assert segs([0, 1, 2]) == [(0, 2)]

    def test_split(self) -> None:
        assert segs([0, 1, 2, 5, 6]) == [(0, 2), (5, 6)]

    def test_sorts_and_dedupes(self) -> None:
        assert segs([2, 0, 1, 1]) == [(0, 2)]


class TestDistinctness:
    """I, T, Y, Z were hand-tuned to avoid collisions."""

    @pytest.mark.parametrize("a,b", [("I", "T"), ("I", "Y"), ("T", "Y")])
    def test_i_t_y_distinct(self, a: str, b: str) -> None:
        assert INK_BANDS[a] != INK_BANDS[b], f"{a} and {b} are identical"


def test_available_chars_letters_first() -> None:
    """A-Z first (alphabetical order), punctuation at the end.

    Without this, `?` (ASCII 63) would come before `A` (65) in a raw sort,
    which would put the question mark at the head of the specimen chart.
    """
    chars = available_chars()
    letters = [c for c in chars if c.isalpha()]
    others = [c for c in chars if not c.isalpha()]
    assert letters == sorted(letters)
    assert chars == letters + others
    assert chars[0] == "A"
    assert chars[-1] == "?"
