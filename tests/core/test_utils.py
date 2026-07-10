"""Tests for universal utility functions."""

from textwarp._core.utils import (
    change_first_letter_case, find_first_alphabetical_idx, load_json_data
)


def test_change_first_letter_case():
    """Test changing only the first alphabetical character's case."""
    assert change_first_letter_case('bang', str.upper) == 'Bang'
    assert change_first_letter_case('WHIMPER', str.lower) == 'wHIMPER'
    assert change_first_letter_case('!!!', str.upper) == '!!!'


def test_find_first_alphabetical_idx_standard():
    """Test standard strings starting with letters."""
    assert find_first_alphabetical_idx(
        'To strive, to seek, to find, and not to yield'
    ) == 0
    assert find_first_alphabetical_idx(
        'We shall not cease from exploration'
    ) == 0


def test_find_first_alphabetical_idx_with_numbers():
    """Test strings starting with digits."""
    assert find_first_alphabetical_idx(
        'Freedom is the freedom to say that 2 + 2 = 4.') == 0
    assert find_first_alphabetical_idx(
        '451—the temperature at which book-paper catches fire, and burns'
    ) == 4


def test_find_first_alphabetical_idx_with_symbols():
    """Test strings starting with punctuation or whitespace."""
    assert find_first_alphabetical_idx(
        '    dumb blankness, full of meaning'
    ) == 4
    assert find_first_alphabetical_idx('(pretending to search)') == 1


def test_find_first_alphabetical_idx_no_letters():
    """Test strings that contain no alphabetical characters."""
    assert find_first_alphabetical_idx('1885') is None
    assert find_first_alphabetical_idx('!!!') is None
    assert find_first_alphabetical_idx('') is None
    assert find_first_alphabetical_idx('   ') is None

def test_load_json_data():
    """Test that JSON data can be loaded with and without a locale."""
    morse_data = load_json_data('morse_map.json')
    assert isinstance(morse_data, dict)
    assert 'A' in morse_data

    en_elision_data = load_json_data('elision_words.json', locale='en')
    assert isinstance(en_elision_data, list)
    assert 'cause' in en_elision_data
