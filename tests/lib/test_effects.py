"""Tests for visual and structural text effects."""

from textwarp._lib.effects import (
    randomize,
    reverse,
    widen
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
