"""Universal utility functions."""

import importlib.resources
import json
from pathlib import Path
from typing import Callable, cast

from textwarp._core.types import JSONType

__all__ = [
    'change_first_letter_case',
    'find_first_alphabetical_idx',
    'load_json_data'
]


def change_first_letter_case(
    text: str,
    casing_func: Callable[[str], str]
) -> str:
    """
    Change the case of the first letter of a string without modifying
    any other letters.

    Args:
        text: The string to convert.
        casing_func: The function to apply to the first letter
            (i.e., `str.upper` or `str.lower`).

    Returns:
        str: The converted text.
    """
    idx = find_first_alphabetical_idx(text)

    if idx is not None:
        return text[:idx] + casing_func(text[idx]) + text[idx+1:]

    return text


def find_first_alphabetical_idx(text: str) -> int | None:
    """
    Find the index of the first alphabetical character in a string.

    Args:
        text: The string to search.

    Returns:
        int | None: The index of the first alphabetical character, or
            `None` if there are no alphabetical characters.
    """
    for i, char in enumerate(text):
        if char.isalpha():
            return i
    return None


def load_json_data(
    relative_path: str | Path,
    locale: str | None = None
) -> JSONType:
    """
    Load JSON content from the data directory, optionally scoped by
    locale.

    Args:
        relative_path: The path to the JSON file relative to the data
            directory.
        locale: An optional locale for the path (e.g., 'en').

    Returns:
        JSONType: The loaded JSON content.
    """
    pkg_files = importlib.resources.files(__package__.split('.')[0])

    if locale:
        parts = (locale,) + Path(relative_path).parts
    else:
        parts = Path(relative_path).parts

    resource = pkg_files.joinpath('_core', 'data')
    for part in parts:
        resource = resource.joinpath(part)

    return cast(JSONType, json.loads(resource.read_text(encoding='utf-8')))
