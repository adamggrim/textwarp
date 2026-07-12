"""Tests for general string manipulation functions."""

from textwarp._lib.manipulation import (
    randomize,
    reverse,
    to_single_spaces,
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


def test_to_single_spaces():
    assert to_single_spaces(
        'Objects  In  The  Rear  View  Mirror  May  Appear  Closer  Than  '
        'They  Are'
    ) == 'Objects In The Rear View Mirror May Appear Closer Than They Are'
    assert (
        to_single_spaces('\tCome   together,   right   now')
        == '\tCome together, right now'
    )


def test_widen():
    assert widen('wide open spaces') == 'w i d e   o p e n   s p a c e s'
    assert widen('') == ''
