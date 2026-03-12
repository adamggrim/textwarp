"""Tests for general string manipulation functions."""

from textwarp._lib.manipulation import (
    randomize,
    reverse,
    to_single_spaces,
    widen
)


def test_randomize():
    """Test that string characters are shuffled but preserved."""
    original = "textwarp"
    randomized = randomize(original)

    assert len(randomized) == len(original)
    assert sorted(randomized) == sorted(original)


def test_reverse():
    """Test reversing string characters."""
    assert reverse('redrum') == 'murder'
    assert reverse('number nine, number nine') == 'enin rebmun ,enin rebmun'


def test_to_single_spaces():
    """
    Test collapsing multiple consecutive spaces into a single space.
    """
    assert to_single_spaces(
        'Come  with  me  if  you  want  to  live.'
    ) == 'Come with me if you want to live.'
    assert to_single_spaces(
        '\tA   long   time   ago   in   a   galaxy   far   far   away....'
    ) == '\tA long time ago in a galaxy far far away....'


def test_widen():
    """Test adding spaces between characters."""
    assert widen("textwarp") == "t e x t w a r p"
    assert widen('E T') == 'E   T'
    assert widen('') == ''
