"""A configuration module handling lazy loading of JSON data."""

import json
from typing import (
    Any,
    Final,
    TypeAlias,
    TypedDict,
    cast
)
from pathlib import Path


class CapitalizationContext(TypedDict):
    """
    The capitalization context for a custom entity.

    Attributes:
        casing: The capitalization to apply.
        pos_sequences: A list of parts-of-speech sequences for the
            entity.
        ngrams: A list of ngrams to check for.

    """
    casing: str
    pos_sequences: list[list[str]]
    ngrams: list[str]


# A type for JSON data.
JSONType: TypeAlias = (
    dict[str, Any] | list[Any] | str | int | float | bool | None
)

DATA_ROOT: Final = Path(__file__).parent / '_data'
ENTITY_CAPITALIZATION_DIR: Final = Path('entity_capitalization')
CONTRACTION_EXPANSION_DIR: Final = Path('contraction_expansion')
STRING_CAPITALIZATION_DIR: Final = Path('string_capitalization')


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


# Map pairing each custom entity with its capitalized version.
ABSOLUTE_CAPITALIZATIONS_MAP: Final[dict[str, str]] = cast(
    dict[str, str],
    _load_json_from_data(
        ENTITY_CAPITALIZATION_DIR / 'absolute_capitalizations_map.json'
    )
)

# Capitalization mappings for contractions that can expand to multiple
# phrases.
AMBIGUOUS_CONTRACTIONS: Final[list[str]] = cast(
    list[str],
    _load_json_from_data(
        CONTRACTION_EXPANSION_DIR / 'ambiguous_contractions.json'
    )
)

# Abbreviations that are always capitalized.
CAPITALIZED_ABBREVIATIONS_MAP: Final[dict[str, str]] = cast(
    dict[str, str],
    _load_json_from_data(
        STRING_CAPITALIZATION_DIR / 'capitalized_abbreviations_map.json'
    )
)

# Capitalization mappings for entities with multiple possible
# capitalizations depending on context.
CONTEXTUAL_CAPITALIZATIONS_MAP: Final[
    dict[str, list[CapitalizationContext]]
] = cast(
    dict[str, list[CapitalizationContext]],
    _load_json_from_data(
        ENTITY_CAPITALIZATION_DIR / 'contextual_capitalizations_map.json'
    )
)

# Suffix tokens derived from contractions.
CONTRACTION_SUFFIXES: Final[list[str]] = cast(
    list[str],
    _load_json_from_data(
        ENTITY_CAPITALIZATION_DIR / 'contraction_suffixes.json'
    )
)

# Words that are commonly elided.
ELISION_WORDS: Final[set[str]] = set(
    cast(list[str], _load_json_from_data('elision_words.json'))
)

# Map pairing each initialism with its capitalized version.
INITIALISMS_MAP: Final[dict[str, str]] = cast(
    dict[str, str],
    _load_json_from_data(
        STRING_CAPITALIZATION_DIR / 'initialisms_map.json'
    )
)

# Abbreviations that are always lowercase.
LOWERCASE_ABBREVIATIONS: Final[set[str]] = set(
    cast(
        list[str],
        _load_json_from_data(
            STRING_CAPITALIZATION_DIR / 'lowercase_abbreviations.json'
        )
    )
)

# Lowercase particles that are not capitalized in title case.
LOWERCASE_PARTICLES: Final[set[str]] = set(
    cast(
        list[str],
        _load_json_from_data(
            ENTITY_CAPITALIZATION_DIR / 'lowercase_particles.json'
        )
    )
)

# Suffixes to split off from map-capitalized words.
MAP_SUFFIX_EXCEPTIONS: Final[list[str]] = cast(
    list[str],
    _load_json_from_data(
        STRING_CAPITALIZATION_DIR / 'map_suffix_exceptions.json'
    )
)

# Map pairing each mixed-case word with its lowercase version.
MIXED_CASE_WORDS_MAP: Final[dict[str, str]] = cast(
    dict[str, str],
    _load_json_from_data(
        STRING_CAPITALIZATION_DIR / 'mixed_case_words_map.json'
    )
)

# Map pairing each character with its Morse code equivalent.
MORSE_MAP: Final[dict[str, str]] = cast(
    dict[str, str],
    _load_json_from_data('morse_map.json')
)

# Words with name prefixes that do not follow standard prefix rules.
NAME_PREFIX_EXCEPTIONS: Final[list[str]] = cast(
    list[str],
    _load_json_from_data(
        STRING_CAPITALIZATION_DIR / 'name_prefix_exceptions.json'
    )
)

# Name prefixes that necessitate special name casing.
NAME_PREFIXES: Final[list[str]] = cast(
    list[str],
    _load_json_from_data(STRING_CAPITALIZATION_DIR / 'name_prefixes.json')
)

# Map pairing each prefixed name not following standard prefix rules
# with its capitalized version.
OTHER_PREFIXED_NAMES_MAP: Final[dict[str, str]] = cast(
    dict[str, str],
    _load_json_from_data(
        STRING_CAPITALIZATION_DIR / 'other_prefixed_names_map.json'
    )
)

# Map for decoding Morse code.
REVERSED_MORSE_MAP: Final[dict[str, str]] = {
    value: key for key, value in MORSE_MAP.items()
}

# Map pairing each unambiguous contraction with its expanded version.
UNAMBIGUOUS_CONTRACTIONS_MAP: Final[dict[str, str]] = cast(
    dict[str, str],
    _load_json_from_data(
        CONTRACTION_EXPANSION_DIR / 'unambiguous_contractions_map.json'
    )
)
