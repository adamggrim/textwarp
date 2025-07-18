import json
import os
from typing import Any


# Get the directory of the current file.
file_dir: str = os.path.dirname(__file__)


def load_json_from_data(filename: str) -> dict[str, Any]:
    """
    Construct a path to a file in the 'data' subdirectory and load it
    as a dictionary.

    Args:
        filename: The name of the JSON file.

    Returns:
        dict[str, Any]: The JSON file loaded as a dictionary.
    """
    # Construct a platform-independent path to the JSON file.
    json_file_path: str = os.path.join(file_dir, 'data', filename)

    # Load and return the JSON data.
    with open(json_file_path, 'r') as json_file:
        return json.load(json_file)


# Pairs each character with its Morse code equivalent.
morse_map: dict[str, str] = load_json_from_data('morse_map.json')
# Pairs each contraction with its expanded version.
contractions_map: dict[str, str] = load_json_from_data(
    'contractions_map.json'
)
