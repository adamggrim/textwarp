"""Tests for apostrophe and quote character constants."""

from textwarp._core.constants.apostrophes import OPEN_QUOTES


def test_open_quotes_is_frozenset():
    """Verify that `OPEN_QUOTES` is an immutable `frozenset`."""
    assert isinstance(OPEN_QUOTES, frozenset)


def test_open_quotes_contains_expected_chars():
    """
    Verify that OPEN_QUOTES contains standard opening quote characters.
    """
    assert '"' in OPEN_QUOTES
    assert '“' in OPEN_QUOTES
    assert "'" in OPEN_QUOTES
    assert '‘' in OPEN_QUOTES


def test_open_quotes_excludes_closing_chars_and_other_chars():
    """Verify that closing quotes and standard text are excluded."""
    assert '”' not in OPEN_QUOTES
    assert '’' not in OPEN_QUOTES
    assert all(not char.isalnum() for char in OPEN_QUOTES)
    assert all(not char.isspace() for char in OPEN_QUOTES)
