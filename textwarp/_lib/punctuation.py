"""Functions for converting between straight and curly quotes."""

from textwarp._core.context import ctx

__all__ = [
    'curly_to_straight',
    'remove_apostrophes',
    'straight_to_curly'
]


def curly_to_straight(text: str) -> str:
    """
    Convert curly quotes in a given string to straight quotes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return ctx.provider.curly_to_straight(text)


def remove_apostrophes(text: str) -> str:
    """
    Remove apostrophes from a string without removing single quotes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return ctx.provider.remove_apostrophes(text)


def straight_to_curly(text: str) -> str:
    """
    Convert straight quotes in a given string to curly quotes.

    Args:
        text: The string to convert.

    Returns:
        curly_text: The converted string.
    """
    return ctx.provider.straight_to_curly(text)
