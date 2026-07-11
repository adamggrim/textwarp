"""Functions for converting between programming cases."""

from __future__ import annotations

from textwarp._core.constants import patterns
from textwarp._core.enums import CaseSeparator, TokenType
from textwarp._core.utils import change_first_letter_case
from textwarp._lib.casing.lexing import get_normalized_tokens
from textwarp._lib.casing.string_casing import case_from_string

__all__ = [
    'to_camel_case',
    'to_pascal_case',
    'to_separator_case'
]


def _format_camel_first_word(word: str) -> str:
    """
    Format the first word of a camel case string.

    Lowercases the entire word if it is an acronym, otherwise lowercases
    only the first letter.

    Args:
        word: The word to format.

    Returns:
        str: The correctly formatted starting word.
    """
    if word.isupper():
        return word.lower()
    return change_first_letter_case(word, str.lower)


def _is_separator_case(text: str) -> bool:
    """
    Check whether a string is entirely in a separator case.

    Args:
        text: The string to evaluate.

    Returns:
        bool: True if it is a separator case, otherwise False.
    """
    return bool(
        patterns.cases.get_snake_word().fullmatch(text)
        or patterns.cases.get_kebab_word().fullmatch(text)
        or patterns.cases.get_dot_word().fullmatch(text)
    )


def _word_to_pascal(word: str) -> str:
    """
    Convert a single word to Pascal case.

    Args:
        word: The word to convert.

    Returns:
        str: The converted word.
    """
    if not any(char.isalpha() for char in word):
        return word
    if patterns.cases.get_pascal_word().match(word):
        return word
    if patterns.cases.get_camel_word().match(word):
        return change_first_letter_case(word, str.upper)

    return case_from_string(word)


def to_camel_case(text: str) -> str:
    """
    Convert a string to camel case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    is_separator_case = _is_separator_case(text)
    parts = []
    first_word = True

    for token_type, value in get_normalized_tokens(text):
        if token_type is TokenType.WORD:
            if first_word:
                parts.append(_format_camel_first_word(value))
                first_word = False
            elif is_separator_case and value.islower():
                parts.append(value.capitalize())
            else:
                parts.append(_word_to_pascal(value))
        elif token_type is TokenType.SYMBOL:
            parts.append(value)
            first_word = True

    return ''.join(parts)


def to_pascal_case(text: str) -> str:
    """
    Convert a string to Pascal case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    is_separator_case = _is_separator_case(text)
    parts = []

    for token_type, value in get_normalized_tokens(text):
        if token_type is TokenType.WORD:
            if is_separator_case and value.islower():
                parts.append(value.capitalize())
            else:
                parts.append(_word_to_pascal(value))
        elif token_type is TokenType.SYMBOL:
            parts.append(value)

    return ''.join(parts)


def to_separator_case(
    text: str,
    separator: CaseSeparator
) -> str:
    """
    Convert a string to dot case, kebab case or snake case.

    Args:
        text: The string to convert.
        separator: The separator for the converted string.

    Returns:
        str: The converted string.
    """
    parts = []
    last_was_sep = False
    last_token_type = None

    for token_type, value in get_normalized_tokens(text):
        if token_type is TokenType.WORD:
            if last_token_type is TokenType.WORD:
                parts.append(separator.value)

            parts.append(value.lower())
            last_was_sep = False

        elif token_type is TokenType.SYMBOL:
            parts.append(value)
            last_was_sep = False

        elif token_type is TokenType.SEPARATOR:
            if parts and not last_was_sep:
                parts.append(separator.value)
                last_was_sep = True

        last_token_type = token_type

    cased_text = ''.join(parts)
    return cased_text.rstrip(separator.value)
