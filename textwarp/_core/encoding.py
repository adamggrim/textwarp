"""Functions for loading universal encoding data."""

from functools import cache
from types import MappingProxyType
from typing import Mapping

from textwarp._core.utils import load_json_data

__all__ = ['get_morse_map', 'get_morse_reversed_map']


@cache
def get_morse_map() -> Mapping[str, str]:
    """Get a cached map of characters to Morse code."""
    return MappingProxyType(load_json_data('morse_map.json'))


@cache
def get_morse_reversed_map() -> Mapping[str, str]:
    """Get a cached map of Morse code to characters."""
    return MappingProxyType({
        value: key for key, value in get_morse_map().items()
    })
