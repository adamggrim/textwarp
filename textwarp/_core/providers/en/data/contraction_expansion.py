"""Functions for loading English contraction expansion rules."""

from functools import lru_cache
from pathlib import Path
from types import MappingProxyType
from typing import Final, Mapping, cast

from textwarp._core.utils import load_json_data

__all__ = [
    'get_ambiguous_map',
    'get_common_stateless_participles',
    'get_idiomatic_map',
    'get_unambiguous_map',
    'get_whatcha_are_words',
    'get_whatcha_have_words'
]

DIR: Final = Path('contraction_expansion')


@lru_cache(maxsize=1)
def get_ambiguous_map() -> tuple[str, ...]:
    """Get a cached tuple of ambiguous contractions."""
    return tuple(
        cast(
            list[str],
            load_json_data(DIR / 'ambiguous_contractions.json', locale='en')
        )
    )


@lru_cache(maxsize=1)
def get_common_stateless_participles() -> tuple[str, ...]:
    """Get a cached tuple of common stateless participles."""
    return tuple(
        cast(
            list[str],
            load_json_data(
                DIR / 'common_stateless_participles.json', locale='en'
            )
        )
    )


@lru_cache(maxsize=1)
def get_idiomatic_map() -> Mapping[str, str]:
    """Get a cached map of idiomatic phrases."""
    return MappingProxyType(
        cast(
            dict[str, str],
            load_json_data(DIR / 'idiomatic_phrases.json', locale='en')
        )
    )


@lru_cache(maxsize=1)
def get_to_verb_words() -> frozenset[str]:
    """
    Get a cached `frozenset` of words that expand to 'to' despite noun
    tags.
    """
    return frozenset(
        cast(
            list[str],
            load_json_data(DIR / 'to_verb_words.json', locale='en')
        )
    )


@lru_cache(maxsize=1)
def get_unambiguous_map() -> Mapping[str, str]:
    """Get a cached map of unambiguous contractions."""
    return MappingProxyType(
        cast(
            dict[str, str],
            load_json_data(
                DIR / 'unambiguous_contractions_map.json', locale='en'
            )
        )
    )


@lru_cache(maxsize=1)
def get_whatcha_are_words() -> tuple[str, ...]:
    """
    Get a cached tuple of "whatcha" "are" replacement words.
    """
    return tuple(
        cast(
            list[str],
            load_json_data(DIR / 'whatcha_are_words.json', locale='en')
        )
    )


@lru_cache(maxsize=1)
def get_whatcha_have_words() -> tuple[str, ...]:
    """
    Get a cached tuple of "whatcha" "have" replacement words.
    """
    return tuple(
        cast(
            list[str],
            load_json_data(DIR / 'whatcha_have_words.json', locale='en')
        )
    )
