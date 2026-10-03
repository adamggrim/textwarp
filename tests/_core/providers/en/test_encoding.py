"""Tests for English-specific encoding and decoding functions."""

from textwarp._core.providers.en.encoding import normalize_for_morse


def test_normalize_for_morse():
    original = '“CQD CQD SOS de MGY Position 41.44N 50.24W.”'
    normalized = normalize_for_morse(original)

    assert normalized == '"CQD CQD SOS DE MGY POSITION 41.44N 50.24W."'
