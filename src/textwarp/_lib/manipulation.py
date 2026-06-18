"""Functions for manipulating a given string."""

import unicodedata
from random import choice, randint, shuffle

import regex as re

from textwarp._core.constants import patterns

__all__ = [
    'from_zalgo',
    'randomize',
    'reverse',
    'to_single_spaces',
    'widen',
    'zalgo'
]


def from_zalgo(text: str) -> str:
    """
    Remove Zalgo diacritics.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return ''.join(
        char for char in text
        if not unicodedata.combining(char)
    )


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
    Reverse the characters of a given string.

    Args:
        text: The string to reverse.

    Returns:
        The reversed string.
    """
    return ''.join(reversed(re.findall(r'\X', text)))


def to_single_spaces(text: str) -> str:
    """
    Convert consecutive spaces to a single space.

    This function preserves leading spaces and tabs.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return patterns.warping.get_multiple_spaces().sub(' ', text)


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

def zalgo(text: str) -> str:
    """
    Convert a string to Zalgo text.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    up_marks = (
        [chr(i) for i in range(0x0300, 0x0316)]
        + [chr(i) for i in range(0x033D, 0x0345)]
        + [chr(i) for i in range(0x0350, 0x0358)]
        + [chr(i) for i in range(0x0363, 0x0370)]
    )
    down_marks = (
        [chr(i) for i in range(0x0316, 0x0334)]
        + [chr(i) for i in range(0x0347, 0x034A)]
        + [chr(i) for i in range(0x0359, 0x035C)]
    )
    mid_marks = (
        [chr(i) for i in range(0x0334, 0x033D)]
        + [chr(0x0338)]
    )

    result = []
    for char in text:
        result.append(char)
        if char.isalnum():
            for _ in range(randint(1, 3)):
                result.append(choice(up_marks))
            for _ in range(randint(1, 2)):
                result.append(choice(mid_marks))
            for _ in range(randint(1, 3)):
                result.append(choice(down_marks))

    return ''.join(result)
