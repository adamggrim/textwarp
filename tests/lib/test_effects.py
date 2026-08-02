"""Tests for visual and structural text effects."""

from hypothesis import given, strategies

from textwarp._lib.effects import (
    randomize,
    reverse,
    widen,
    _GRAPHEME_PATTERN
)


def test_randomize():
    original = 'all shook up'
    randomized = randomize(original)

    assert len(randomized) == len(original)
    assert sorted(randomized) == sorted(original)


def test_reverse():
    assert reverse('number nine, number nine') == 'enin rebmun ,enin rebmun'
    assert reverse('redrum') == 'murder'


def test_widen():
    assert widen('wide open spaces') == 'w i d e   o p e n   s p a c e s'
    assert widen('') == ''


@given(strategies.text())
def test_reverse_symmetry(s):
    reversed = reverse(s)
    # Only enforce perfect symmetry if the previous reversal did not
    # merge any grapheme clusters.
    if (
        len(_GRAPHEME_PATTERN.findall(s))
        == len(_GRAPHEME_PATTERN.findall(reversed))
    ):
        assert reverse(reversed) == s


@given(strategies.text())
def test_randomize_properties(s):
    result = randomize(s)
    assert len(result) == len(s)
    assert set(result) == set(s)


@given(strategies.text(
    alphabet=strategies.characters(blacklist_categories=('Cs', 'Cn'))
))
def test_widen_properties(s):
    expected_length = max(0, (len(s) * 2) - 1)
    assert len(widen(s)) == expected_length
