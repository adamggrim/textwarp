"""
Functions for loading English string casing exceptions and prefixes.
"""

from functools import cache
from pathlib import Path
from types import MappingProxyType
from typing import Final, Mapping, cast

from textwarp._core.utils import load_json_data

__all__ = [
    'get_lookup_map',
    'get_lowercase_abbreviations',
    'get_map_suffix_exceptions',
    'get_surname_prefix_exceptions',
    'get_surname_prefixes'
]

DIR: Final = Path('string_casing')


@cache
def get_lookup_map() -> Mapping[str, str]:
    """Get a combined cached map for string casings."""
    absolute_map = cast(
        dict[str, str],
        load_json_data(DIR / 'absolute_casings_map.json', locale='en')
    )
    prefixed_surnames_map = cast(
        dict[str, str],
        load_json_data(DIR / 'prefixed_surnames_map.json', locale='en')
    )
    return MappingProxyType(
        {**prefixed_surnames_map, **absolute_map}
    )


@cache
def get_lowercase_abbreviations() -> frozenset[str]:
    """
    Get a cached `frozenset` of lowercase abbreviations.
    """
    return frozenset(cast(list[str], load_json_data(
        DIR / 'lowercase_abbreviations.json', locale='en'
    )))


@cache
def get_map_suffix_exceptions() -> frozenset[str]:
    """Get a cached `frozenset` of map suffix exceptions."""
    return frozenset(
        cast(
            list[str],
            load_json_data(DIR / 'map_suffix_exceptions.json', locale='en')
        )
    )


@cache
def get_surname_prefix_exceptions() -> frozenset[str]:
    """Get a cached `frozenset` of surname prefix exceptions."""
    return frozenset(
        cast(
            list[str],
            load_json_data(DIR / 'surname_prefix_exceptions.json', locale='en')
        )
    )


@cache
def get_surname_prefixes() -> frozenset[str]:
    """Get a cached `frozenset` of standard surname prefixes."""
    return frozenset(
        cast(
            list[str],
            load_json_data(DIR / 'surname_prefixes.json', locale='en')
        )
    )
