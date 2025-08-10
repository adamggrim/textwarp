import json
import os
from typing import Union


# Get the directory of the current file.
file_dir: str = os.path.dirname(__file__)

# Define a type for JSON data.
JSONType = Union[dict, list, str, int, float, bool, None]


def load_json_from_data(filename: str) -> JSONType:
    """
    Construct a path to a file in the 'data' subdirectory and load it
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


# Abbreviations that are followed by a period.
ABBREVIATIONS: set[str] = set(load_json_from_data('abbreviations.json'))

# Suffixes derived from contractions.
CONTRACTION_SUFFIX_SET: set[str] = set(load_json_from_data(
    'contraction_sufixes.json'
))

# Pairs each contraction with its expanded version.
CONTRACTIONS_MAP: dict[str, str] = load_json_from_data(
    'contractions_map.json'
)

# Words that are elided for certain contractions.
ELISION_WORDS: set[str] = set(load_json_from_data('elision_words.json'))

# Common initialisms to uppercase.
INITIALISMS: set[str] = set(load_json_from_data('initialisms.json'))

# Lowercase particles that should not be capitalized in title case.
LOWERCASE_PARTICLES: set[str] = set(load_json_from_data(
    'lowercase_particles.json'
))

# Pairs each mixed-case word with its lowercase version.
MIXED_CASE_WORDS: dict[str, str] = load_json_from_data(
    'mixed_case_words.json'
)

# Pairs each character with its Morse code equivalent.
MORSE_MAP: dict[str, str] = load_json_from_data('morse_map.json')
