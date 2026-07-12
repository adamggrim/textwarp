"""Public functions for warping text."""

from __future__ import annotations

from random import choice
from typing import TYPE_CHECKING

import regex as re

if TYPE_CHECKING:
    from spacy.tokens import Doc

from textwarp._core.constants import patterns
from textwarp._core.context import ctx
from textwarp._core.enums import CaseSeparator, Casing, ModelPriority

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
    'from_zalgo',
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
    'to_zalgo',
    'widen'
]


def capitalize(content: str | Doc) -> str:
    """
    Capitalize each word in a string or spaCy `Doc`, handling apecial
    name prefixes and preserving other mid-word capitalizations.
    """
    doc = process_as_doc(content)
    return to_natural_case(doc, Casing.START)


def cardinal_to_ordinal(text: str) -> str:
    """
    Convert cardinal numbers in a string to ordinal numbers.
    """
    return numbers.cardinal_to_ordinal(text)


def expand_contractions(content: str | Doc) -> str:
    """Expand all contractions in a string or spaCy `Doc`."""
    if not hasattr(ctx.provider, 'expand_contractions'):
        return content if isinstance(content, str) else content.text

    doc = process_as_doc(content)
    return contractions.expand_contractions(doc)


def from_binary(binary_text: str) -> str:
    """Convert a string from binary."""
    return encoding.from_binary(binary_text)


def from_hexadecimal(text: str) -> str:
    """Convert a string from hexadecimal."""
    return encoding.from_hexadecimal(text)


def from_morse(text: str) -> str:
    """Convert a string from Morse code."""
    return encoding.from_morse(text)


def from_zalgo(text: str) -> str:
    """Remove Zalgo diacritics from a string."""
    return manipulation.from_zalgo(text)


def hyphen_to_en(text: str) -> str:
    """Convert hyphens in a string to en dashes."""
    return text.replace('-', '–')


def hyphens_to_em(text: str) -> str:
    """Convert em dash stand-ins in a string to em dashes."""
    return patterns.warping.get_em_dash_stand_in().sub('—', text)


def ordinal_to_cardinal(text: str) -> str:
    """Convert ordinal numbers in a string to cardinal numbers."""
    return numbers.ordinal_to_cardinal(text)


def punct_to_inside(text: str) -> str:
    """
    Move periods and commas at the end of quotes inside quotation marks.
    """
    if not hasattr(ctx.provider, 'punct_outside_pattern'):
        return text

    def _repl(match: re.Match[str]) -> str:
        """
        Reorder periods and commas to move them inside quotation marks.
        """
        quote, punct = match.groups()
        return punct + quote

    return ctx.provider.punct_outside_pattern.sub(_repl, text)


def punct_to_outside(text: str) -> str:
    """
    Move periods and commas at the end of quotes to outside quotation
    marks.
    """
    if not hasattr(ctx.provider, 'punct_inside_pattern'):
        return text

    def _repl(match: re.Match[str]) -> str:
        """
        Reorder periods and commas to move them outside quotation
        marks.
        """
        punct, quote = match.groups()
        return quote + punct

    return ctx.provider.punct_inside_pattern.sub(_repl, text)


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


def randomize(text: str) -> str:
    """Randomize the characters of a string."""
    return manipulation.randomize(text)


def redact(text: str) -> str:
    """
    Redact a string by replacing each word character with a black square.
    """
    return patterns.warping.get_word_character().sub('█', text)


def reverse(text: str) -> str:
    """
    Reverse the characters of a string.
    """
    return manipulation.reverse(text)


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
    """Convert a string to camel case."""
    return casing.to_camel_case(text)


def to_dot_case(text: str) -> str:
    """Convert a string to dot case."""
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
    """Convert a string to kebab case."""
    return to_separator_case(text, CaseSeparator.KEBAB)


def to_morse(text: str) -> str:
    """
    Convert a string to Morse code.

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
    """Convert a string to Pascal case."""
    return casing.to_pascal_case(text)


def to_sentence_case(content: str | Doc) -> str:
    """Convert a string or spaCy `Doc` to sentence case."""
    doc = process_as_doc(content)
    return to_natural_case(doc, Casing.SENTENCE)


def to_single_spaces(text: str) -> str:
    """
    Convert consecutive spaces to a single space.

    This function preserves leading spaces and tabs.
    """
    return manipulation.to_single_spaces(text)


def to_snake_case(text: str) -> str:
    """Convert a string to snake case."""
    return to_separator_case(text, CaseSeparator.SNAKE)


def to_title_case(content: str | Doc) -> str:
    """
    Convert a string or spaCy `Doc` to title case, handling special
    name prefixes and preserving other mid-word capitalizations.
    """
    # Use the large spaCy model for identifying titles within titles.
    doc = process_as_doc(content, model_priority=ModelPriority.ACCURACY)
    return to_natural_case(doc, Casing.TITLE)


def to_zalgo(text: str) -> str:
    """Convert a string to Zalgo text."""
    return manipulation.to_zalgo(text)


def widen(text: str) -> str:
    """
    Widen a string by adding a space after each character except
    the last one.
    """
    return manipulation.widen(text)
