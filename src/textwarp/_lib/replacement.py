"""Functions for finding and replacing text."""

from typing import Callable

import regex as re

__all__ = [
    'replace_case',
    'replace_regex',
    'replace_text'
]


def replace_case(
    text: str,
    search_pattern: re.Pattern[str],
    conversion_func: Callable[[str], str]
) -> str:
    """
    Replace a case within the text using the provided pattern and
    conversion function, returning the transformed text.

    Args:
        text: The string to transform.
        search_pattern: The compiled regular expression to search for.
        conversion_func: The function to convert the matched text.

    Returns:
        str: The transformed text.
    """
    return search_pattern.sub(
        lambda match: conversion_func(match.group(0)),
        text
    )


def replace_regex(
    text: str,
    regex_text: str,
    replacement_text: str
) -> str:
    """
    Find a regular expression within the text and replace it with the
    target string, returning the transformed text.

    Args:
        text: The string to transform.
        regex_text: The regular expression to find.
        replacement_text: The string to replace the match with.

    Returns:
        str: The transformed text.
    """
    return re.sub(regex_text, replacement_text, text)


def replace_text(
    text: str,
    text_to_replace: str,
    replacement_text: str
) -> str:
    """
    Find a string to replace within the text and replace it with the
    target string, returning the transformed text.

    Args:
        text: The string to transform.
        text_to_replace: The string to replace.
        replacement_text: The string to replace the match with.

    Returns:
        str: The transformed text.
    """
    return text.replace(text_to_replace, replacement_text)
