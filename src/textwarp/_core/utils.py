"""Universal utility functions."""

import importlib.resources
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

__all__ = [
    'change_first_alphabetical_case',
    'find_first_alphabetical_idx',
    'load_json_data',
    'starts_uppercase'
]


def change_first_alphabetical_case(
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
) -> Any:
    """
    Load JSON content from the universal data directory or a
    locale-specific provider's data directory.

    Args:
        relative_path: The path to the JSON file relative to the data
            directory.
        locale: An optional locale for the provider (e.g., 'en').

    Returns:
        Any: The loaded JSON content.
    """
    pkg_files = importlib.resources.files(__package__.split('.')[0])

    if locale:
        resource = pkg_files / '_core' / 'providers' / locale / 'data'
    else:
        resource = pkg_files / '_core' / 'data'

    for part in Path(relative_path).parts:
        resource = resource / part

    return json.loads(resource.read_text(encoding='utf-8'))


def starts_uppercase(text: str) -> bool:
    """
    Check if the first alphabetical character in the text is uppercase.

    Args:
        text: The string to check.

    Returns:
        bool: `True` if the first alphabetical character is uppercase,
            otherwise `False`.
    """
    idx = find_first_alphabetical_idx(text)
    return idx is not None and text[idx].isupper()
