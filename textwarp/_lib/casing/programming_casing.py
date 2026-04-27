"""Functions for converting between programming cases."""

from __future__ import annotations

from typing import Generator

from textwarp._core.constants import patterns
from textwarp._core.enums import CaseSeparator, TokenType
from textwarp._core.utils import change_first_letter_case
from textwarp._lib.casing.string_casing import case_from_string
from textwarp._lib.punctuation import remove_apostrophes

__all__ = [
    'to_camel_case',
    'to_pascal_case',
    'to_separator_case'
]


def _chunk_by_alnum(text: str) -> list[str]:
    """
    Split text into alternating alphanumeric and non-alphanumeric
    chunks.

    Args:
        text: The string to split.

    Returns:
        list[str]: The split chunks, where the first chunk is
            alphanumeric if the string starts with an alphanumeric
            character; otherwise non-alphanumeric.
    """
    if not text:
        return []

    chunks = []
    current_chars = []
    is_alnum = None

    for char in text:
        char_alnum = char.isalnum()
        if is_alnum is None:
            is_alnum = char_alnum

        if char_alnum == is_alnum:
            current_chars.append(char)
        else:
            chunks.append(''.join(current_chars))
            current_chars = [char]
            is_alnum = char_alnum

    if current_chars:
        chunks.append(''.join(current_chars))

    return chunks


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


def _get_normalized_tokens(
    text: str
) -> Generator[tuple[TokenType, str], None, None]:
    """
    Tokenize a string into words, symbols and separators.

    Args:
        text: The string to tokenize.

    Yields:
        Generator[tuple[TokenType, str], None, None]: A generator of
            tuples where the first element is the token type and the
            second is the token string.
    """
    no_apostrophes_text = remove_apostrophes(text)
    chunks = _chunk_by_alnum(no_apostrophes_text)

    for i, chunk in enumerate(chunks):
        if chunk[0].isalnum():
            if (
                not chunk.islower()
                and not chunk.isupper()
                and any(c.isalpha() for c in chunk)
            ):
                for sub in _split_camel_pascal(chunk):
                    yield TokenType.WORD, sub
            else:
                yield TokenType.WORD, chunk
        else:
            is_only_spaces_and_separators = all(
                c.isspace() or c in '.-_' for c in chunk
            )

            if chunk.isspace() and i > 0 and i < len(chunks) - 1:
                if chunks[i - 1][0].isalnum() and chunks[i + 1][0].isalnum():
                    yield TokenType.SEPARATOR, chunk
                    continue

            for char in chunk:
                if char in '.-_':
                    yield TokenType.SEPARATOR, char
                else:
                    if char.isspace() and is_only_spaces_and_separators:
                        yield TokenType.SEPARATOR, char
                    else:
                        yield TokenType.SYMBOL, char


def _split_camel_pascal(text: str) -> list[str]:
    """
    Split camel case or Pascal case into constituent words.

    Args:
        text: The string to split.

    Returns:
        list[str]: The split words.
    """
    if not text:
        return []

    words = []
    current_word = [text[0]]

    for i in range(1, len(text)):
        prev_char = text[i - 1]
        current_char = text[i]
        next_char = text[i + 1] if i + 1 < len(text) else ''

        is_boundary = False

        # Position between an uppercase and lowercase letter.
        if current_char.isupper() and prev_char.islower():
            is_boundary = True
        # Position after an acronym (e.g., after "JSON" in "JSONData").
        elif (
            current_char.isupper()
            and prev_char.isupper()
            and next_char.islower()
        ):
            is_boundary = True
        # Position between a letter and a digit.
        elif prev_char.isalpha() and current_char.isdigit():
            is_boundary = True
        # Position between a digit and a letter.
        elif prev_char.isdigit() and current_char.isalpha():
            is_boundary = True

        if is_boundary:
            words.append(''.join(current_word))
            current_word = [current_char]
        else:
            current_word.append(current_char)

    if current_word:
        words.append(''.join(current_word))

    return words


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
    parts = []
    first_word = True

    for token_type, value in _get_normalized_tokens(text):
        if token_type is TokenType.WORD:
            if first_word:
                parts.append(_format_camel_first_word(value))
                first_word = False
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
    parts = []

    for token_type, value in _get_normalized_tokens(text):
        if token_type is TokenType.WORD:
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

    for token_type, value in _get_normalized_tokens(text):
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
