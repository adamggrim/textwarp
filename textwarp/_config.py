import json
from typing import (
    Any,
    Final,
    TypeAlias,
    cast
)
from pathlib import Path

# Define a type for JSON data.
JSONType: TypeAlias = (
    dict[str, Any] | list[Any] | str | int | float | bool | None
)

# Path to the base directory for data files.
data_root = Path(__file__).parent / '_data'


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
    json_file_path = data_root / relative_path

    # Load and return the JSON data.
    with open(json_file_path, 'r') as json_file:
        return cast(JSONType, json.load(json_file))


# Capitalization mappings for entities with multiple possible
# capitalizations.
AMBIGUOUS_CAPITALIZATIONS: Final[dict[str, list[dict[str, Any]]]] = cast(
    [str, list[dict[str, Any]]],
    _load_json_from_data(
        Path('_entity_capitalization') / 'ambiguous_capitalizations_map.json'
    )
)

# Capitalization mappings for contractions that can expand to multiple
# phrases.
AMBIGUOUS_CONTRACTIONS: Final[list[str]] = cast(
    list[str],
    _load_json_from_data(
        Path('_contraction_expansion') / 'ambiguous_contractions.json'
    )
)

# Abbreviations that are always capitalized.
CAPITALIZED_ABBREVIATIONS_MAP: Final[dict[str, str]] = cast(
    dict[str, str],
    _load_json_from_data(
        Path('_string_capitalization') / 'capitalized_abbreviations_map.json'
    )
)

# Suffix tokens derived from contractions.
CONTRACTION_SUFFIX_TOKENS: Final[list[str]] = cast(
    list[str],
    _load_json_from_data(
        Path('_entity_capitalization') / 'contraction_suffix_tokens.json'
    )
)

# Map pairing each custom entity with its capitalized version.
CUSTOM_ENTITIES_MAP: Final[dict[str, str]] = cast(
    dict[str, str],
    _load_json_from_data(
        Path('_entity_capitalization') / 'custom_entities_map.json'
    )
)

# Words that are elided for certain contractions.
ELISION_WORDS: Final[set[str]] = set(
    cast(
        list[str],
        _load_json_from_data(Path('elision_words.json')))
)

# Map pairing each initialism with its capitalized version.
INITIALISMS_MAP: Final[dict[str, str]] = cast(
    dict[str, str],
    _load_json_from_data(
        Path('_string_capitalization') / 'initialisms_map.json'
    )
)

# Abbreviations that are always lowercase.
LOWERCASE_ABBREVIATIONS: Final[set[str]] = set(
    cast(
        list[str],
        _load_json_from_data(
            Path('_string_capitalization') / 'lowercase_abbreviations.json'
        )
    )
)

# Lowercase particles that are not capitalized in title case.
LOWERCASE_PARTICLES: Final[set[str]] = set(
    cast(
        list[str],
        _load_json_from_data(
            Path('_entity_capitalization') / 'lowercase_particles.json'
        )
    )
)

# Suffixes to split off from map-capitalized words.
MAP_SUFFIX_EXCEPTIONS: Final[list[str]] = cast(
    list[str],
    _load_json_from_data(
        Path('_string_capitalization') / 'map_suffix_exceptions.json'
    )
)

# Map pairing each mixed-case word with its lowercase version.
MIXED_CASE_WORDS_MAP: Final[dict[str, str]] = cast(
    dict[str, str],
    _load_json_from_data(
        Path('_string_capitalization') / 'mixed_case_words_map.json'
    )
)

# Map pairing each character with its Morse code equivalent.
MORSE_MAP: Final[dict[str, str]] = cast(
    dict[str, str],
    _load_json_from_data(Path('morse_map.json'))
)

# Words with name prefixes that do not follow standard prefix rules.
NAME_PREFIX_EXCEPTIONS: Final[list[str]] = cast(
    list[str],
    _load_json_from_data(
        Path('_string_capitalization') / 'name_prefix_exceptions.json'
    )
)

# Name prefixes that necessitate special name casing.
NAME_PREFIXES: Final[list[str]] = cast(
    list[str],
    _load_json_from_data(
        Path('_string_capitalization') / 'name_prefixes.json'
    )
)

# Map pairing each prefixed name not following standard prefix rules
# with its capitalized version.
OTHER_PREFIXED_NAMES_MAP: Final[dict[str, str]] = cast(
    dict[str, str],
    _load_json_from_data(
        Path('_string_capitalization') / 'other_prefixed_names_map.json'
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
        Path('_contraction_expansion') / 'unambiguous_contractions_map.json'
    )
)
