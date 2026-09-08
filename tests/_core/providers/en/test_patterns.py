"""Tests for English-specific regular expressions."""

from textwarp._core.providers.en.patterns import (
    get_apostrophe_in_word,
    get_n_t_suffix
)


def test_get_apostrophe_in_word():
    pattern = get_apostrophe_in_word()
    match = pattern.search('It’s')
    assert match is not None
    assert match.group(0) == '’'
    assert pattern.search('’n’') is not None


def test_get_n_t_suffix():
    pattern = get_n_t_suffix()

    match = pattern.search('can’t')
    assert match is not None

    match_curly = pattern.search('won’t')
    assert match_curly is not None
