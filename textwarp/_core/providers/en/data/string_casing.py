"""
Functions for loading English string casing exceptions and prefixes.
"""

from functools import lru_cache
from pathlib import Path
from types import MappingProxyType
from typing import Final, Mapping, cast

from textwarp._core.providers.en.data.loader import load_data

__all__ = [
    'get_lookup_map',
    'get_lowercase_abbreviations',
    'get_map_suffix_exceptions',
    'get_surname_prefix_exceptions',
    'get_surname_prefixes'
]

DIR: Final = Path('string_casing')


@lru_cache(maxsize=1)
def get_lookup_map() -> Mapping[str, str]:
    """Get a combined cached mapping for string casings."""
    absolute_map = cast(
        dict[str, str],
        load_data(DIR / 'absolute_casings_map.json')
    )
    prefixed_surnames_map = cast(
        dict[str, str],
        load_data(DIR / 'prefixed_surnames_map.json')
    )
    return MappingProxyType(
        {**prefixed_surnames_map, **absolute_map}
    )


@lru_cache(maxsize=1)
def get_lowercase_abbreviations() -> frozenset[str]:
    """
    Get a cached `frozenset` of lowercase abbreviations.
    """
    return frozenset(cast(list[str], load_data(
        DIR / 'lowercase_abbreviations.json'
    )))


@lru_cache(maxsize=1)
def get_map_suffix_exceptions() -> frozenset[str]:
    """Get a cached `frozenset` of map suffix exceptions."""
    return frozenset(
        cast(
            list[str],
            load_data(DIR / 'map_suffix_exceptions.json')
        )
    )


@lru_cache(maxsize=1)
def get_surname_prefix_exceptions() -> frozenset[str]:
    """Get a cached `frozenset` of surname prefix exceptions."""
    return frozenset(
        cast(
            list[str],
            load_data(DIR / 'surname_prefix_exceptions.json')
        )
    )


@lru_cache(maxsize=1)
def get_surname_prefixes() -> frozenset[str]:
    """Get a cached `frozenset` of standard surname prefixes."""
    return frozenset(
        cast(
            list[str],
            load_data(DIR / 'surname_prefixes.json')
        )
    )
