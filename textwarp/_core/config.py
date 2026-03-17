"""A configuration module handling lazy loading of JSON data."""

import importlib.resources
import json
from functools import lru_cache
from types import MappingProxyType
from typing import Final, Mapping, cast
from pathlib import Path

from textwarp._core.types import (
    EntityCasingContext,
    JSONType
)
from textwarp._core.context import ctx

__all__ = [
    'ContractionExpansion',
    'Encoding',
    'EntityCasing',
    'Punctuation',
    'StringCasing',
    'TokenCasing'
]


def _load(relative_path: str | Path) -> JSONType:
    """
    Load JSON content using importlib.resources for zip safety.
    Determine language-specific data using the active locale.

    Args:
        relative_path: The name of the JSON file or subpath.

    Returns:
        JSONType: The JSON file loaded as a Python object.
    """
    pkg_files = importlib.resources.files(__package__)
    path_obj = Path(relative_path)

    if path_obj.name == 'morse_map.json':
        parts = path_obj.parts
    else:
        parts = (ctx.locale,) + path_obj.parts

    resource = pkg_files.joinpath('data', *parts)

    return cast(JSONType, json.loads(resource.read_text(encoding='utf-8')))


class ContractionExpansion:
    """A namespace for loading contraction expansion data."""
    DIR: Final = Path('contraction_expansion')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_ambiguous_map() -> tuple[str, ...]:
        return tuple(cast(list[str], _load(
            ContractionExpansion.DIR / 'ambiguous_contractions.json'
        )))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_common_stateless_participles() -> tuple[str, ...]:
        return tuple(cast(list[str], _load(
            ContractionExpansion.DIR / 'common_stateless_participles.json'
        )))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_idiomatic_map() -> Mapping[str, str]:
        return MappingProxyType(cast(dict[str, str], _load(
            ContractionExpansion.DIR / 'idiomatic_phrases.json'
        )))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_unambiguous_map() -> Mapping[str, str]:
        return MappingProxyType(cast(dict[str, str], _load(
            ContractionExpansion.DIR / 'unambiguous_contractions_map.json'
        )))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_whatcha_are_words() -> tuple[str, ...]:
        return tuple(cast(list[str], _load(
            ContractionExpansion.DIR / 'whatcha_are_words.json'
        )))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_whatcha_have_words() -> tuple[str, ...]:
        return tuple(cast(list[str], _load(
            ContractionExpansion.DIR / 'whatcha_have_words.json'
        )))


class Encoding:
    """A namespace for encoding and decoding translation data."""

    @staticmethod
    @lru_cache(maxsize=1)
    def get_morse_map() -> Mapping[str, str]:
        return MappingProxyType(cast(dict[str, str], _load('morse_map.json')))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_morse_reversed_map() -> Mapping[str, str]:
        return MappingProxyType({
            value: key for key, value in Encoding.get_morse_map().items()
        })


class EntityCasing:
    """A namespace for loading entity casing data."""
    DIR: Final = Path('entity_casing')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_absolute_map() -> Mapping[str, str]:
        return MappingProxyType(cast(dict[str, str], _load(
            EntityCasing.DIR / 'absolute_casings_map.json'
        )))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_contextual_map() -> Mapping[str, tuple[EntityCasingContext, ...]]:
        raw_map = cast(dict[str, list[EntityCasingContext]], _load(
            EntityCasing.DIR / 'contextual_casings_map.json'
        ))
        return MappingProxyType({
            key: tuple(contexts) for key, contexts in raw_map.items()
        })

    @staticmethod
    @lru_cache(maxsize=1)
    def get_contraction_suffixes() -> tuple[str, ...]:
        return tuple(cast(list[str], _load(
            EntityCasing.DIR / 'contraction_suffixes.json'
        )))


class Punctuation:
    """A namespace for loading punctuation data."""

    @staticmethod
    @lru_cache(maxsize=1)
    def get_elision_words() -> frozenset[str]:
        return frozenset(cast(list[str], _load('elision_words.json')))


class StringCasing:
    """A namespace for loading string casing data."""
    DIR: Final = Path('string_casing')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_lookup_map() -> Mapping[str, str]:
        absolute_map = cast(dict[str, str], _load(
            StringCasing.DIR / 'absolute_casings_map.json'
        ))
        prefixed_surnames_map = cast(dict[str, str], _load(
            StringCasing.DIR / 'prefixed_surnames_map.json'
        ))
        return MappingProxyType({**prefixed_surnames_map, **absolute_map})

    @staticmethod
    @lru_cache(maxsize=1)
    def get_lowercase_abbreviations() -> frozenset[str]:
        return frozenset(cast(list[str], _load(
            StringCasing.DIR / 'lowercase_abbreviations.json'
        )))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_map_suffix_exceptions() -> tuple[str, ...]:
        return tuple(cast(list[str], _load(
            StringCasing.DIR / 'map_suffix_exceptions.json'
        )))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_surname_prefix_exceptions() -> tuple[str, ...]:
        return tuple(cast(list[str], _load(
            StringCasing.DIR / 'surname_prefix_exceptions.json'
        )))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_surname_prefixes() -> tuple[str, ...]:
        return tuple(cast(list[str], _load(
            StringCasing.DIR / 'surname_prefixes.json'
        )))


class TokenCasing:
    """A namespace for loading token casing data."""
    @staticmethod
    @lru_cache(maxsize=1)
    def get_lowercase_particles() -> frozenset[str]:
        return frozenset(cast(list[str], _load(
            EntityCasing.DIR / 'lowercase_particles.json'
        )))
