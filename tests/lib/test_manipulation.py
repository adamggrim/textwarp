"""Tests for general string manipulation functions."""

from textwarp._lib.manipulation import (
    randomize,
    reverse,
    to_single_spaces,
    widen
)


def test_randomize():
    """Test that string characters are shuffled but preserved."""
    original = 'things fall apart'
    randomized = randomize(original)

    assert len(randomized) == len(original)
    assert sorted(randomized) == sorted(original)


def test_reverse():
    """Test reversing string characters."""
    assert reverse('number nine, number nine') == 'enin rebmun ,enin rebmun'
    assert reverse('redrum') == 'murder'


def test_to_single_spaces():
    """
    Test collapsing multiple consecutive spaces into a single space.
    """
    assert to_single_spaces(
        'Objects  In  The  Rear  View  Mirror  May  Appear  Closer  Than  '
        'They  Are'
    ) == 'Objects In The Rear View Mirror May Appear Closer Than They Are'
    assert to_single_spaces(
        '\tIn   space,  no   one   can   hear   you   scream.'
    ) == '\tIn space, no one can hear you scream.'


def test_widen():
    """Test adding spaces between characters."""
    assert widen('illimitable ocean') == 'i l l i m i t a b l e   o c e a n'
    assert widen('') == ''
