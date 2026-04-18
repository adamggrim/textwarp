"""Tests for universal utility functions."""

from textwarp._core.utils import (
    change_first_letter_case, find_first_alphabetical_idx
)


def test_change_first_letter_case():
    """Test changing only the first alphabetical character's case."""
    assert change_first_letter_case('101 dalmations', str.upper) == (
        '101 Dalmations'
    )
    assert change_first_letter_case('bang', str.upper) == 'Bang'
    assert change_first_letter_case('WHIMPER', str.lower) == 'wHIMPER'
    assert change_first_letter_case('!!!', str.upper) == '!!!'


def test_find_first_alphabetical_idx_standard():
    """Test standard strings starting with letters."""
    assert find_first_alphabetical_idx(
        'Alexander and the Terrible, Horrible, No Good, Very Bad Day'
    ) == 0
    assert find_first_alphabetical_idx(
        "Baron Munchausen's Narrative of His Marvellous Travels and "
        'Campaigns in Russia'
    ) == 0


def test_find_first_alphabetical_idx_with_numbers():
    """Test strings starting with digits."""
    assert find_first_alphabetical_idx('2001: A Space Odyssey') == 6
    assert find_first_alphabetical_idx('3 Body Problem') == 2
    assert find_first_alphabetical_idx('Fahrenheit 451') == 0


def test_find_first_alphabetical_idx_with_symbols():
    """Test strings starting with punctuation or whitespace."""
    assert find_first_alphabetical_idx('    I am, I am, I am.') == 4
    assert find_first_alphabetical_idx('[They do not move.]') == 1
    assert find_first_alphabetical_idx(
        '"Kick me under the table all you want."'
    ) == 1


def test_find_first_alphabetical_idx_no_letters():
    """Test strings that contain no alphabetical characters."""
    assert find_first_alphabetical_idx('2009') is None
    assert find_first_alphabetical_idx('!!!') is None
    assert find_first_alphabetical_idx('') is None
    assert find_first_alphabetical_idx('   ') is None
