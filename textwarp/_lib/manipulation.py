"""Functions for manipulating a given string."""

from random import shuffle

from textwarp._core.constants.regexes import WarpingPatterns

__all__ = [
    'randomize',
    'reverse',
    'to_single_spaces',
    'widen'
]


def randomize(text: str) -> str:
    """
    Randomize the characters of a given string.

    Args:
        text: The string to randomize.

    Returns:
        str: The randomized string.
    """
    # Convert the string into a list of characters.
    char_list = list(text)
    shuffle(char_list)
    return ''.join(char_list)


def reverse(text: str) -> str:
    """
    Reverses the characters of a given string.

    Args:
        text: The string to reverse.

    Returns:
        The reversed string.
    """
    return text[::-1]


def to_single_spaces(text: str) -> str:
    """
    Convert consecutive spaces to a single space.

    This function preserves leading spaces and tabs.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return WarpingPatterns.MULTIPLE_SPACES.sub(' ', text)


def widen(text: str) -> str:
    """
    Widen a string by adding a space after each character except
    the last one.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return ' '.join(text)
