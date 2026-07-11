"""Tests for Zalgo text functions."""

import unicodedata

from textwarp.warping import from_zalgo, to_zalgo


def test_zalgo_text():
    """Verify that `from_zalgo` removes all diacritics."""
    original_text = 'textwarp'
    zalgonized_text = to_zalgo(original_text)

    # Zalgonized text should be longer than the original.
    assert len(zalgonized_text) > len(original_text)

    assert from_zalgo(zalgonized_text) == original_text


def test_from_zalgo_on_plain_text():
    """Verify that `from_zalgo` does not change plain text."""
    original_text = 'plain text'
    assert from_zalgo(original_text) == original_text


def test_zalgo_and_unicode():
    """Verify Zalgo text correctly handles Unicode special cases."""
    original_text = 'café'
    zalgonized_text = to_zalgo(original_text)

    cleaned_text = from_zalgo(zalgonized_text)

    assert (
        unicodedata.normalize('NFC', cleaned_text)
        == unicodedata.normalize('NFC', original_text)
    )
