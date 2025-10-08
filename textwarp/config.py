import json
import os
from typing import Final, Union, cast


# Get the directory of the current file.
file_dir: str = os.path.dirname(__file__)

# Define a type for JSON data.
JSONType = Union[dict, list, str, int, float, bool, None]


def load_json_from_data(filename: str) -> JSONType:
    """
    Construct a path to a file in the ``data`` subdirectory and load it
    as a dictionary.

    Args:
        filename: The name of the JSON file.

    Returns:
        JSONType: The JSON file loaded as a Python object.
    """
    # Construct a platform-independent path to the JSON file.
    json_file_path: str = os.path.join(file_dir, 'data', filename)

    # Load and return the JSON data.
    with open(json_file_path, 'r') as json_file:
        return json.load(json_file)


# Contractions that can expand to multiple phrases.
AMBIGUOUS_CONTRACTIONS: Final[list[str]] = list(load_json_from_data(
    'ambiguous_contractions.json'
))

# Abbreviations that are always capitalized.
CAPITALIZED_ABBREVIATIONS_MAP: Final[dict[str, str]] = load_json_from_data(
    'capitalized_abbreviations_map.json'
)

# Suffix tokens derived from contractions.
CONTRACTION_SUFFIX_TOKENS: Final[list[str]] = list(load_json_from_data(
    'contraction_suffix_tokens.json'
))

# Map pairing each contraction with its expanded version.
CONTRACTIONS_MAP: Final[dict[str, str]] = load_json_from_data(
    'contractions_map.json'
)

# Words that are elided for certain contractions.
ELISION_WORDS: Final[set[str]] = set(load_json_from_data('elision_words.json'))

# Map pairing each initialism with its capitalized version.
INITIALISMS_MAP: Final[dict[str, str]] = load_json_from_data(
    'initialisms_map.json'
)

# Abbreviations that are always lowercase.
LOWERCASE_ABBREVIATIONS: Final[set[str]] = set(load_json_from_data(
    'lowercase_abbreviations.json'
))

# Lowercase particles that are not capitalized in title case.
LOWERCASE_PARTICLES: Final[set[str]] = set(load_json_from_data(
    'lowercase_particles.json'
))

# Suffixes to split off from map-capitalized words.
MAP_SUFFIX_EXCEPTIONS: Final[list[str]] = list(load_json_from_data(
    'map_suffix_exceptions.json'
))

# Map pairing each mixed-case word with its lowercase version.
MIXED_CASE_WORDS_MAP: Final[dict[str, str]] = load_json_from_data(
    'mixed_case_words_map.json'
)

# Map pairing each character with its Morse code equivalent.
MORSE_MAP: Final[dict[str, str]] = load_json_from_data('morse_map.json')

# Name prefixes that necessitate special name casing.
NAME_PREFIXES: Final[list[str]] = list(load_json_from_data(
    'name_prefixes.json')
)

# Words with name prefixes that do not follow standard prefix rules.
NAME_PREFIX_EXCEPTIONS: Final[list[str]] = list(load_json_from_data(
    'name_prefix_exceptions.json'
))

# Map pairing each prefixed name not following standard prefix rules
# with its capitalized version.
OTHER_PREFIXED_NAMES_MAP: Final[dict[str, str]] = load_json_from_data(
    'other_prefixed_names_map.json'
)

# Map for decoding Morse code.
REVERSED_MORSE_MAP: Final[dict[str, str]] = {
    value: key for key, value in MORSE_MAP.items()
}
