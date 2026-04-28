"""Public functions for warping text."""

from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING

import regex as re

if TYPE_CHECKING:
    from spacy.tokens import Doc

from textwarp._core.constants import patterns
from textwarp._core.context import ctx
from textwarp._core.enums import CaseSeparator, Casing

from textwarp._lib import (
    casing,
    contractions,
    curly_to_straight,
    encoding,
    manipulation,
    numbers,
    process_as_doc,
    straight_to_curly,
    to_natural_case,
    to_separator_case
)

__all__ = [
    'capitalize',
    'cardinal_to_ordinal',
    'curly_to_straight',
    'expand_contractions',
    'from_binary',
    'from_hexadecimal',
    'from_morse',
    'hyphen_to_en',
    'hyphens_to_em',
    'ordinal_to_cardinal',
    'punct_to_inside',
    'punct_to_outside',
    'random_case',
    'randomize',
    'redact',
    'reverse',
    'straight_to_curly',
    'to_alternating_caps',
    'to_binary',
    'to_camel_case',
    'to_dot_case',
    'to_hexadecimal',
    'to_kebab_case',
    'to_morse',
    'to_pascal_case',
    'to_sentence_case',
    'to_single_spaces',
    'to_snake_case',
    'to_title_case',
    'widen'
]


def capitalize(content: str | Doc) -> str:
    """
    Capitalize each word in a given string or spaCy `Doc`, handling
    special name prefixes and preserving other mid-word capitalizations.

    Args:
        content: The string or spaCy `Doc` to capitalize.

    Returns:
        str: The capitalized string.
    """
    doc = process_as_doc(content)
    return to_natural_case(doc, Casing.START)


def cardinal_to_ordinal(text: str) -> str:
    """
    Convert cardinal numbers in a given string to ordinal numbers.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return numbers.cardinal_to_ordinal(text)


def expand_contractions(content: str | Doc) -> str:
    """
    Expand all contractions in a given string or spaCy `Doc`.

    Args:
        content: The string or spaCy `Doc` to convert.

    Returns:
        str: The converted string.
    """
    if not hasattr(ctx.provider, 'expand_contractions'):
        return content if isinstance(content, str) else content.text

    doc = process_as_doc(content)
    return contractions.expand_contractions(doc)


def from_binary(binary_text: str) -> str:
    """
    Convert a string from binary.

    Args:
        binary_text: The space-separated binary string to convert.

    Returns:
        str: The converted string.
    """
    return encoding.from_binary(binary_text)


def from_hexadecimal(text: str) -> str:
    """
    Convert a string from hexadecimal.

    Args:
        text: The hexadecimal string to convert.

    Returns:
        str: The converted string.
    """
    return encoding.from_hexadecimal(text)


def from_morse(text: str) -> str:
    """
    Convert a string from Morse code.

    Args:
        text: The Morse string to convert.

    Returns:
        str: The converted string (in all caps).
    """
    return encoding.from_morse(text)


def hyphen_to_en(text: str) -> str:
    """
    Convert hyphens in a given string to en dashes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return text.replace('-', '–')


def hyphens_to_em(text: str) -> str:
    """
    Convert em dash stand-ins in a given string to em dashes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return patterns.warping.get_em_dash_stand_in().sub('—', text)


def ordinal_to_cardinal(text: str) -> str:
    """
    Convert ordinal numbers in a given string to cardinal numbers.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return numbers.ordinal_to_cardinal(text)


def punct_to_inside(text: str) -> str:
    """
    Move periods and commas at the end of quotes inside quotation
    marks.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    if not hasattr(ctx.provider, 'punct_outside_pattern'):
        return text

    def _repl(match: re.Match[str]) -> str:
        """
        Reorder periods and commas to move them inside quotation marks.

        Args:
            match: A match object.

        Returns:
            str: The reordered string.
        """
        quote, punct = match.groups()
        return punct + quote

    return ctx.provider.punct_outside_pattern.sub(_repl, text)


def punct_to_outside(text: str) -> str:
    """
    Move periods and commas at the end of quotes to outside quotation
    marks.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    if not hasattr(ctx.provider, 'punct_inside_pattern'):
        return text

    def _repl(match: re.Match[str]) -> str:
        """
        Reorder periods and commas to move them outside quotation
        marks.

        Args:
            match: A match object.

        Returns:
            str: The reordered string.
        """
        punct, quote = match.groups()
        return quote + punct

    return ctx.provider.punct_inside_pattern.sub(_repl, text)


def random_case(text: str) -> str:
    """
    Randomize the casing of each character in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
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


def randomize(text: str) -> str:
    """
    Randomize the characters of a given string.

    Args:
        text: The string to randomize.

    Returns:
        str: The randomized string.
    """
    return manipulation.randomize(text)


def redact(text: str) -> str:
    """
    Redact a string by replacing each word character with a black
    square.

    Args:
        text: The string to redact.

    Returns:
        str: The redacted string.
    """
    return patterns.warping.get_word_character().sub('█', text)


def reverse(text: str) -> str:
    """
    Reverse the characters of a given string.

    Args:
        text: The string to reverse.

    Returns:
        The reversed string.
    """
    return manipulation.reverse(text)


def to_alternating_caps(text: str) -> str:
    """
    Convert a string to alternating caps.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    result: list[str] = []
    # Toggle switch for alternating caps effect.
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


def to_binary(text: str) -> str:
    """
    Convert a string to binary.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string in binary, with each character's
            binary value separated by a space.
    """
    return encoding.to_binary(text)


def to_camel_case(text: str) -> str:
    """
    Convert a string to camel case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return casing.to_camel_case(text)


def to_dot_case(text: str) -> str:
    """
    Convert a string to dot case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return to_separator_case(text, CaseSeparator.DOT)


def to_hexadecimal(text: str) -> str:
    """
    Convert a string to hexadecimal.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string in hexadecimal, with each character's
            hex value separated by a space.
    """
    return encoding.to_hexadecimal(text)


def to_kebab_case(text: str) -> str:
    """
    Convert a string to kebab case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return to_separator_case(text, CaseSeparator.KEBAB)


def to_morse(text: str) -> str:
    """
    Convert a given string to Morse code.

    Letters (A-Z), numbers (0-9) and common punctuation (., ?, !, ,, :,
    ;, +, -, =, @, (, ), ", ', /, &) are all supported.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string, with a single space between
            character codes and three spaces between word codes.
    """
    return encoding.to_morse(text)


def to_pascal_case(text: str) -> str:
    """
    Convert a string to Pascal case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return casing.to_pascal_case(text)


def to_sentence_case(content: str | Doc) -> str:
    """
    Convert a string or spaCy `Doc` to sentence case.

    Args:
        content: The string or spaCy `Doc` to convert.

    Returns:
        str: The converted string.
    """
    doc = process_as_doc(content)
    return to_natural_case(doc, Casing.SENTENCE)


def to_single_spaces(text: str) -> str:
    """
    Convert consecutive spaces to a single space.

    This function preserves leading spaces and tabs.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return manipulation.to_single_spaces(text)


def to_snake_case(text: str) -> str:
    """
    Convert a string to snake case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return to_separator_case(text, CaseSeparator.SNAKE)


def to_title_case(content: str | Doc) -> str:
    """
    Convert a string or spaCy `Doc` to title case, handling special
    name prefixes and preserving other mid-word capitalizations.

    Args:
        content: The string or spaCy `Doc` to convert.

    Returns:
        str: The converted string.
    """
    # Use the large model for identifying titles within titles.
    doc = process_as_doc(content, model_priority='accuracy')
    return to_natural_case(doc, Casing.TITLE)


def widen(text: str) -> str:
    """
    Widen a string by adding a space after each character except
    the last one.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return manipulation.widen(text)
