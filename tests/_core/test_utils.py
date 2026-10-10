"""Tests for universal utility functions."""

import pytest

from textwarp._core.utils import (
    change_first_alphabetical_case,
    find_first_alphabetical_idx,
    load_json_data
)


@pytest.mark.parametrize('text, casing_func, expected', [
    ('bang', str.upper, 'Bang'),
    ('WHIMPER', str.lower, 'wHIMPER'),
    ('!!!', str.upper, '!!!')
])
def test_change_first_alphabetical_case(text, casing_func, expected):
    assert change_first_alphabetical_case(text, casing_func) == expected


@pytest.mark.parametrize('text, expected_idx', [
    ('To strive, to seek, to find, and not to yield', 0),
    ('We shall not cease from exploration', 0),
    ('Freedom is the freedom to say that 2 + 2 = 4.', 0),
    ('451—the temperature at which book-paper catches fire, and burns', 4),
    ('    dumb blankness, full of meaning', 4),
    ('(pretending to search)', 1),
    ('1885', None),
    ('!!!', None),
    ('', None),
    ('   ', None)
])
def test_find_first_alphabetical_idx(text, expected_idx):
    assert find_first_alphabetical_idx(text) == expected_idx


def test_load_json_data():
    """Test that JSON data can be loaded with and without a locale."""
    morse_data = load_json_data('morse_map.json')
    assert isinstance(morse_data, dict)
    assert 'A' in morse_data

    en_elision_data = load_json_data('elision_words.json', locale='en')
    assert isinstance(en_elision_data, list)
    assert 'cause' in en_elision_data
