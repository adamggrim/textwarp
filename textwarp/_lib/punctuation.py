"""Functions for converting between straight and curly quotes."""

import regex as re

from .._core import WarpingPatterns

__all__ = [
    'curly_to_straight',
    'remove_apostrophes',
    'straight_to_curly'
]


def _replace_opening_quote(match: re.Match[str]) -> str:
    """
    Convert a sequence of straight quotes to opening curly quotes in a
    given match.

    Args:
        match: A match object where the first captured group is a
            string of one or more consecutive straight quote
            characters.

    Returns:
        str: A string of opening curly quotes.
    """
    quote_chars = match.group(1) or match.group(2) or ''
    if quote_chars.startswith("'"):
        return '‘' * len(quote_chars)
    else:
        return '“' * len(quote_chars)


def curly_to_straight(text: str) -> str:
    """
    Convert curly quotes to straight quotes in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    translation_table = str.maketrans({
        # Curly opening single quotes to straight single quotes
        '’': "'",
        # Curly opening double quotes to straight double quotes
        '”': '"',
        # Curly closing single quotes to straight single quotes
        '‘': "'",
        # Curly closing double quotes to straight double quotes
        '“': '"'
    })
    return text.translate(translation_table)


def remove_apostrophes(text: str) -> str:
    """
    Remove apostrophes from a string without removing single quotes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return WarpingPatterns.APOSTROPHE_IN_WORD.sub('', text)


def straight_to_curly(text: str) -> str:
    """
    Convert straight quotes to curly quotes in a given string.

    Args:
        text: The string to convert.

    Returns:
        curly_text: The converted string.
    """
    # Replace intra-word apostrophes and apostrophes in elisions.
    curly_text = WarpingPatterns.APOSTROPHE_IN_WORD.sub('’', text)

    # Replace opening straight quotes with opening curly quotes.
    curly_text = WarpingPatterns.OPENING_STRAIGHT_QUOTES.sub(
        _replace_opening_quote, curly_text
    )

    # Replace any remaining straight single quotes with closing curly
    # single quotes.
    curly_text = curly_text.replace("'", '’')

    # Replace any remaining straight double quotes with closing curly
    # double quotes.
    curly_text = curly_text.replace('"', '”')

    return curly_text
