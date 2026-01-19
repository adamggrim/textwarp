"""A configuration module handling lazy loading of JSON data."""

import json
from functools import lru_cache
from typing import (
    Final,
    cast
)
from pathlib import Path

from ._types import (
    EntityCasingContext,
    JSONType
)

DATA_ROOT: Final = Path(__file__).parent / '_data'


def _load(relative_path: Path | str) -> JSONType:
    """
    Build the path to a file relative to the base directory and
    load its contents as a JSON object.

    Args:
        relative_path: The name of the JSON file.

    Returns:
        JSONType: The JSON file loaded as a Python object.
    """
    # Build a platform-independent path to the JSON file.
    json_file_path = DATA_ROOT / relative_path

    # Load and return the JSON data.
    with open(json_file_path, 'r') as json_file:
        return cast(JSONType, json.load(json_file))


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
            EntityCasing.DIR / 'contextual_entities_map.json'
        ))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_contraction_suffixes() -> list[str]:
        return cast(list[str], _load(
            EntityCasing.DIR / 'contraction_suffixes.json'
        ))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_lowercase_particles() -> set[str]:
        return set(cast(list[str], _load(
            EntityCasing.DIR / 'lowercase_particles.json'
        )))


class StringCasing:
    """A namespace for loading string casing data."""
    DIR: Final = Path('string_casing')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_absolute_map() -> dict[str, str]:
        return cast(dict[str, str], _load(
            StringCasing.DIR / 'absolute_casings_map.json'
        ))

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
    def get_other_prefixed_names_map() -> dict[str, str]:
        return cast(dict[str, str], _load(
            StringCasing.DIR / 'other_prefixed_names_map.json'
        ))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_surname_prefixes() -> list[str]:
        return cast(list[str], _load(StringCasing.DIR / 'surname_prefixes.json'))
