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
ENTITY_CASING_DIR: Final = Path('entity_casing')
CONTRACTION_EXPANSION_DIR: Final = Path('contraction_expansion')
STRING_CASING_DIR: Final = Path('string_casing')


def _load_json_from_data(relative_path: Path | str) -> JSONType:
    """
    Construct the path to a file relative to the base data directory and
    load its contents as a JSON object.

    Args:
        relative_path: The name of the JSON file.

    Returns:
        JSONType: The JSON file loaded as a Python object.
    """
    # Construct a platform-independent path to the JSON file.
    json_file_path = DATA_ROOT / relative_path

    # Load and return the JSON data.
    with open(json_file_path, 'r') as json_file:
        return cast(JSONType, json.load(json_file))


def _get_casings_map(directory: Path) -> dict[str, str]:
    """
    Load the absolute casings map from a given directory.

    Args:
        directory: The directory containing the JSON file.

    Returns:
        dict[str, str]: The absolute casings map.
    """
    return cast(dict[str, str], _load_json_from_data(
        directory / 'absolute_casings_map.json'
    ))


@lru_cache(maxsize=1)
def get_absolute_entity_casings_map() -> dict[str, str]:
    return _get_casings_map(ENTITY_CASING_DIR)


@lru_cache(maxsize=1)
def get_absolute_string_casings_map() -> dict[str, str]:
    return _get_casings_map(STRING_CASING_DIR)


@lru_cache(maxsize=1)
def get_ambiguous_contractions() -> list[str]:
    return cast(list[str], _load_json_from_data(
        CONTRACTION_EXPANSION_DIR / 'ambiguous_contractions.json'
    ))


@lru_cache(maxsize=1)
def get_contextual_entities_map() -> (
    dict[str, list[EntityCasingContext]]
):
    return cast(dict[str, list[EntityCasingContext]], _load_json_from_data(
        ENTITY_CASING_DIR / 'contextual_entities_map.json'
    ))


@lru_cache(maxsize=1)
def get_contraction_suffixes() -> list[str]:
    return cast(list[str], _load_json_from_data(
        ENTITY_CASING_DIR / 'contraction_suffixes.json'
    ))


@lru_cache(maxsize=1)
def get_elision_words() -> set[str]:
    return set(cast(list[str], _load_json_from_data('elision_words.json')))


@lru_cache(maxsize=1)
def get_initialisms_map() -> dict[str, str]:
    return cast(dict[str, str], _load_json_from_data(
        STRING_CASING_DIR / 'initialisms_map.json'
    ))


@lru_cache(maxsize=1)
def get_lowercase_abbreviations() -> set[str]:
    return set(cast(list[str], _load_json_from_data(
        STRING_CASING_DIR / 'lowercase_abbreviations.json'
    )))


@lru_cache(maxsize=1)
def get_lowercase_particles() -> set[str]:
    return set(cast(list[str], _load_json_from_data(
        ENTITY_CASING_DIR / 'lowercase_particles.json'
    )))


@lru_cache(maxsize=1)
def get_map_suffix_exceptions() -> list[str]:
    return cast(list[str], _load_json_from_data(
        STRING_CASING_DIR / 'map_suffix_exceptions.json'
    ))


@lru_cache(maxsize=1)
def get_mixed_case_words_map() -> dict[str, str]:
    return cast(dict[str, str], _load_json_from_data(
        STRING_CASING_DIR / 'mixed_case_words_map.json'
    ))


@lru_cache(maxsize=1)
def get_morse_map() -> dict[str, str]:
    return cast(dict[str, str], _load_json_from_data('morse_map.json'))


@lru_cache(maxsize=1)
def get_name_prefix_exceptions() -> list[str]:
    return cast(list[str], _load_json_from_data(
        STRING_CASING_DIR / 'name_prefix_exceptions.json'
    ))


@lru_cache(maxsize=1)
def get_other_prefixed_names_map() -> dict[str, str]:
    return cast(dict[str, str], _load_json_from_data(
        STRING_CASING_DIR / 'other_prefixed_names_map.json'
    ))


@lru_cache(maxsize=1)
def get_reversed_morse_map() -> dict[str, str]:
    return {value: key for key, value in get_morse_map().items()}


@lru_cache(maxsize=1)
def get_unambiguous_contractions_map() -> dict[str, str]:
    return cast(dict[str, str], _load_json_from_data(
        CONTRACTION_EXPANSION_DIR / 'unambiguous_contractions_map.json'
    ))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_surname_prefixes() -> list[str]:
        return cast(list[str], _load(StringCasing.DIR / 'surname_prefixes.json'))
