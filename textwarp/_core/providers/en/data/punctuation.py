"""Functions for loading English punctuation rules."""

from functools import lru_cache
from typing import cast

from textwarp._core.utils import load_json_data

__all__ = ['get_elision_words']


@lru_cache(maxsize=1)
def get_elision_words() -> frozenset[str]:
    """Get a cached `frozenset` of elision words."""
    return frozenset(
        cast(
            list[str],
            load_json_data('elision_words.json', locale='en')
        )
    )
