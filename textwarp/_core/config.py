"""A configuration module handling lazy loading of JSON data."""

import importlib.resources
import json
from functools import lru_cache
from typing import (
    Final,
    cast
)
from pathlib import Path

from .types import (
    EntityCasingContext,
    JSONType
)

__all__ = [
    'ContractionExpansion',
    'Encoding',
    'EntityCasing',
    'StringCasing',
    'TokenCasing'
]


def _load(relative_path: str | Path) -> JSONType:
    """
    Load JSON content using importlib.resources for zip safety.

    Args:
        relative_path: The name of the JSON file.

    Returns:
        JSONType: The JSON file loaded as a Python object.
    """
    pkg_files = importlib.resources.files(__package__)
    parts = Path(relative_path).parts
    resource = pkg_files.joinpath('data', *parts)

    return cast(JSONType, json.loads(resource.read_text(encoding='utf-8')))


class ContractionExpansion:
    """A namespace for loading contraction expansion data."""
    DIR: Final = Path('contraction_expansion')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_ambiguous_map() -> list[str]:
        return cast(list[str], _load(
            ContractionExpansion.DIR / 'ambiguous_contractions.json'
        ))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_elision_words() -> set[str]:
        return set(cast(list[str], _load('elision_words.json')))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_unambiguous_map() -> dict[str, str]:
        return cast(dict[str, str], _load(
            ContractionExpansion.DIR / 'unambiguous_contractions_map.json'
        ))


class Encoding:
    """A namespace for encoding and decoding translation data."""

    @staticmethod
    @lru_cache(maxsize=1)
    def get_morse_map() -> dict[str, str]:
        return cast(dict[str, str], _load('morse_map.json'))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_morse_reversed_map() -> dict[str, str]:
        return {value: key for key, value in Encoding.get_morse_map().items()}


class EntityCasing:
    """A namespace for loading entity casing data."""
    DIR: Final = Path('entity_casing')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_absolute_map() -> dict[str, str]:
        return cast(dict[str, str], _load(
            EntityCasing.DIR / 'absolute_casings_map.json'
        ))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_contextual_map() -> dict[str, list[EntityCasingContext]]:
        return cast(dict[str, list[EntityCasingContext]], _load(
            EntityCasing.DIR / 'contextual_casings_map.json'
        ))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_contraction_suffixes() -> list[str]:
        return cast(list[str], _load(
            EntityCasing.DIR / 'contraction_suffixes.json'
        ))


class StringCasing:
    """A namespace for loading string casing data."""
    DIR: Final = Path('string_casing')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_lookup_map() -> dict[str, str]:
        """
        Merge absolute casings and other prefixed names into one map.
        """
        absolute_map = cast(dict[str, str], _load(
            StringCasing.DIR / 'absolute_casings_map.json'
        ))
        prefixed_names_map = cast(dict[str, str], _load(
            StringCasing.DIR / 'prefixed_names_map.json'
        ))
        # Absolute map overrides prefixed names map if there is a collision.
        return {**prefixed_names_map, **absolute_map}

    @staticmethod
    @lru_cache(maxsize=1)
    def get_lowercase_abbreviations() -> set[str]:
        return set(cast(list[str], _load(
            StringCasing.DIR / 'lowercase_abbreviations.json'
        )))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_map_suffix_exceptions() -> list[str]:
        return cast(list[str], _load(
            StringCasing.DIR / 'map_suffix_exceptions.json'
        ))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_name_prefix_exceptions() -> list[str]:
        return cast(list[str], _load(
            StringCasing.DIR / 'name_prefix_exceptions.json'
        ))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_surname_prefixes() -> list[str]:
        return cast(list[str], _load(StringCasing.DIR / 'surname_prefixes.json'))


class TokenCasing:
    """A namespace for loading token casing data."""
    @staticmethod
    @lru_cache(maxsize=1)
    def get_lowercase_particles() -> set[str]:
        return set(cast(list[str], _load(
            EntityCasing.DIR / 'lowercase_particles.json'
        )))
