"""Functions for converting between cardinal and ordinal numbers."""

from textwarp._core.context import ctx

__all__ = [
    'cardinal_to_ordinal',
    'ordinal_to_cardinal'
]


def cardinal_to_ordinal(text: str) -> str:
    """
    Convert cardinal numbers in a given string to ordinal numbers
    using the active language provider.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return ctx.provider.cardinal_to_ordinal(text)


def ordinal_to_cardinal(text: str) -> str:
    """
    Convert ordinal numbers in a given string to cardinal numbers
    using the active language provider.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return ctx.provider.ordinal_to_cardinal(text)
