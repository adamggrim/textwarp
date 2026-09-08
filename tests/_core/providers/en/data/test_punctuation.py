"""Tests for English punctuation data loading."""

from textwarp._core.providers.en.data import punctuation


def test_punctuation_config():
    """Test that punctuation data converts lists to sets."""
    elision_words = punctuation.get_elision_words()
    assert isinstance(elision_words, frozenset)
    assert 'cause' in elision_words
