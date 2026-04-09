"""Tests for English-specific text encoding functions."""

from textwarp._core.providers.en.encoding import normalize_for_morse


def test_normalize_for_morse():
    """
    Test that English text is properly normalized for Morse conversion.
    """
    text = '“CQD CQD SOS de MGY Position 41.44N 50.24W.”'
    normalized = normalize_for_morse(text)

    assert normalized == '"CQD CQD SOS DE MGY POSITION 41.44N 50.24W."'
