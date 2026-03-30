"""Functions for loading English punctuation rules."""

from typing import cast

from textwarp._core.providers.en.data.loader import load_data

__all__ = ['get_elision_words']


def get_elision_words() -> frozenset[str]:
    """Get a cached `frozenset` of elision words."""
    return frozenset(
        cast(list[str], load_data('elision_words.json')))
