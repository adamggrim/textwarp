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
    """
    cased_word = case_from_string(word)

    # Preserve mixed-case words starting with a lowercase letter.
    if cased_word and cased_word[0].islower() and not cased_word.islower():
        return cased_word

    if word.isupper():
        return word.lower()
    return change_first_letter_case(word, str.lower)


def _is_separator_case(text: str) -> bool:
    """Check whether a string is entirely in a separator case."""
    return bool(
        patterns.cases.get_snake_word().fullmatch(text)
        or patterns.cases.get_kebab_word().fullmatch(text)
        or patterns.cases.get_dot_word().fullmatch(text)
    )


def _to_camel_or_pascal(text: str, is_camel: bool) -> str:
    """Shared logic for camel and Pascal case conversion."""
    is_separator_case = _is_separator_case(text)
    parts = []
    is_first_word = True
    prev_token_type = None

    for token_type, value in get_normalized_tokens(text):
        match token_type:
            case TokenType.WORD:
                if is_first_word and is_camel:
                    parts.append(_format_camel_first_word(value))
                elif is_separator_case and value.islower():
                    parts.append(value.capitalize())
                else:
                    parts.append(_word_to_pascal(value))
                is_first_word = False

            case TokenType.SYMBOL:
                parts.append(value)

            case TokenType.SEPARATOR:
                if prev_token_type is TokenType.SYMBOL and value.isspace():
                    parts.append(value)

        prev_token_type = token_type

    return ''.join(parts)


def _word_to_pascal(word: str) -> str:
    """Convert a single word to Pascal case."""
    if not any(char.isalpha() for char in word):
        return word
    if patterns.cases.get_pascal_word().match(word):
        return word
    if patterns.cases.get_camel_word().match(word):
        return change_first_letter_case(word, str.upper)

    # Uppercase the first letter for dictionary lookups.
    cased_word = case_from_string(word)

    return change_first_letter_case(cased_word, str.upper)


def to_camel_case(text: str) -> str:
    """Convert a string to camel case."""
    return _to_camel_or_pascal(text, is_camel=True)


def to_pascal_case(text: str) -> str:
    """Convert a string to Pascal case."""
    return _to_camel_or_pascal(text, is_camel=False)


def to_separator_case(
    text: str,
    separator: CaseSeparator
) -> str:
    """Convert a string to dot case, kebab case or snake case."""
    parts = []
    prev_was_separator = False
    prev_token_type = None

    for token_type, value in get_normalized_tokens(text):
        if token_type is TokenType.WORD:
            if prev_token_type is TokenType.WORD:
                parts.append(separator.value)

            parts.append(value.lower())
            prev_was_separator = False

        elif token_type is TokenType.SYMBOL:
            parts.append(value)
            prev_was_separator = False

        elif token_type is TokenType.SEPARATOR:
            if prev_token_type is TokenType.SYMBOL and value.isspace():
                parts.append(value)
                prev_was_separator = False
            elif parts and not prev_was_separator:
                parts.append(separator.value)
                prev_was_separator = True

        prev_token_type = token_type

    cased_text = ''.join(parts)
    return cased_text.rstrip(separator.value)
