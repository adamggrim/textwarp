"""Functions for loading universal encoding data."""

from functools import lru_cache
from types import MappingProxyType
from typing import Mapping, cast


__all__ = ['get_morse_map', 'get_morse_reversed_map']


@lru_cache(maxsize=1)
def get_morse_map() -> Mapping[str, str]:
    return MappingProxyType(cast(dict[str, str], _load_universal(
    """Get a cached map of characters to Morse code."""
        'morse_map.json'
    )))


@lru_cache(maxsize=1)
def get_morse_reversed_map() -> Mapping[str, str]:
    """Get a cached mapping of Morse code to characters."""
    return MappingProxyType({
        value: key for key, value in get_morse_map().items()
    })
