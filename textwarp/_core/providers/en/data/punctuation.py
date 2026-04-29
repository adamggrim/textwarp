"""Functions for loading English punctuation rules."""

from functools import cache

from textwarp._core.utils import load_json_data

__all__ = ['get_elision_words']


@cache
def get_elision_words() -> frozenset[str]:
    """Get a cached `frozenset` of elision words."""
    return frozenset(load_json_data('elision_words.json', locale='en'))
