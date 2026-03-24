"""Tests for English-specific regular expressions."""

import pytest

from textwarp._core.providers.en_rules.regexes import EnWarpingPatterns


def test_en_warping_patterns_is_non_instantiable():
    """Verify that `EnWarpingPatterns` cannot be instantiated."""
    with pytest.raises(
        RuntimeError, match='EnWarpingPatterns cannot be instantiated'
    ):
        EnWarpingPatterns()


def test_get_apostrophe_in_word():
    """
    Test the regular expression matching apostrophes inside words or
    elisions.
    """
    pattern = EnWarpingPatterns.get_apostrophe_in_word()
    match = pattern.search("It's")
    assert match is not None
    assert match.group(0) == "'"
    assert pattern.search("'n'") is not None


def test_get_cardinal():
    """Test the regular expression matching cardinal numbers."""
    pattern = EnWarpingPatterns.get_cardinal()
    match = pattern.search('The year is 1984.')
    assert match is not None
    assert match.group(0) == '1984'
    assert pattern.search('1984th') is None


def test_get_ordinal():
    """Test the regular expression matching ordinal numbers."""
    pattern = EnWarpingPatterns.get_ordinal()
    match = pattern.search('Thursday, May 12th')
    assert match is not None
    assert match.group(0) == '12th'
    assert pattern.search('12') is None


def test_get_n_t_suffix():
    """
    Test the regular expression matching negative contraction suffixes.
    """
    pattern = EnWarpingPatterns.get_n_t_suffix()

    match = pattern.search("can't")
    assert match is not None

    match_curly = pattern.search('won’t')
    assert match_curly is not None
