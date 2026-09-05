"""Functions that apply visual effects to text."""

import unicodedata
from random import choice, randint, shuffle

import regex as re

from textwarp._core.constants import patterns

__all__ = [
    'random_case',
    'randomize',
    'redact',
    'reverse',
    'to_alternating_caps',
    'to_zalgo',
    'unzalgo',
    'widen'
]

UP_MARKS = tuple(
    [chr(i) for i in range(0x0300, 0x0316)]
    + [chr(i) for i in range(0x033D, 0x0345)]
    + [chr(i) for i in range(0x0350, 0x0358)]
    + [chr(i) for i in range(0x0363, 0x0370)]
)
MID_MARKS = tuple(
    [chr(i) for i in range(0x0334, 0x033D)]
    + [chr(0x0338)]
)
DOWN_MARKS = tuple(
    [chr(i) for i in range(0x0316, 0x0334)]
    + [chr(i) for i in range(0x0347, 0x034A)]
    + [chr(i) for i in range(0x0359, 0x035C)]
)

_GRAPHEME_PATTERN = re.compile(r'\X')


def randomize(text: str) -> str:
    """Randomize the characters of a string."""
    char_list = list(text)
    shuffle(char_list)
    return ''.join(char_list)


def reverse(text: str) -> str:
    """Reverse the characters of a string."""
    return ''.join(reversed(_GRAPHEME_PATTERN.findall(text)))


def to_zalgo(text: str) -> str:
    """Convert a string to Zalgo text."""
    result = []
    for char in text:
        result.append(char)
        if char.isalnum():
            for _ in range(randint(1, 2)):
                result.append(choice(UP_MARKS))
            if choice([True, False]):
                result.append(choice(MID_MARKS))
            for _ in range(randint(1, 2)):
                result.append(choice(DOWN_MARKS))

    return ''.join(result)


def unzalgo(text: str) -> str:
    """Remove Zalgo diacritics from a string."""
    return ''.join(
        char for char in text
        if not unicodedata.combining(char)
    )


def widen(text: str) -> str:
    """
    Widen a string by adding a space after each character except the
    last one.
    """
    return ' '.join(text)


def random_case(text: str) -> str:
    """Randomize the casing of each character in a string."""
    result: list[str] = []

    for char in text:
        if char.isalpha():
            if choice([True, False]):
                result.append(char.upper())
            else:
                result.append(char.lower())
        else:
            result.append(char)

    return ''.join(result)


def redact(text: str) -> str:
    """
    Redact a string by replacing each word character with a black
    square.
    """
    return patterns.warping.get_word_char().sub('█', text)


def to_alternating_caps(text: str) -> str:
    """Convert a string to alternating caps."""
    result: list[str] = []
    upper = False

    for char in text:
        if char.isalpha():
            if upper:
                result.append(char.upper())
            else:
                result.append(char.lower())
            upper = not upper
        else:
            result.append(char)

    return ''.join(result)
