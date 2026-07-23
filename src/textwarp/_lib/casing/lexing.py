"""Tokenization and chunking functions."""

from __future__ import annotations

from typing import Generator

from textwarp._core.enums import TokenType
from textwarp._lib.punctuation import remove_apostrophes

__all__ = ['get_normalized_tokens']


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


def _process_non_alnum_chunk(
    chunk: str,
    prev_chunk: str | None,
    next_chunk: str | None
) -> Generator[tuple[TokenType, str], None, None]:
    """
    Process a non-alphanumeric chunk into separator or symbol tokens.
    """
    is_between_alnum = (
        prev_chunk is not None and prev_chunk[0].isalnum()
        and next_chunk is not None and next_chunk[0].isalnum()
    )

    if chunk.isspace() and is_between_alnum:
        yield TokenType.SEPARATOR, chunk
        return

    for char in chunk:
        if char in '.-_' or char.isspace():
            yield TokenType.SEPARATOR, char
        else:
            yield TokenType.SYMBOL, char


def _split_camel_pascal(text: str) -> list[str]:
    """Split camel case or Pascal case into constituent words."""
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


def get_normalized_tokens(
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
    num_chunks = len(chunks)

    for i, chunk in enumerate(chunks):
        if chunk[0].isalnum():
            for sub in _split_camel_pascal(chunk):
                yield TokenType.WORD, sub
            continue

        prev_chunk = chunks[i - 1] if i > 0 else None
        next_chunk = chunks[i + 1] if i < num_chunks - 1 else None

        yield from _process_non_alnum_chunk(chunk, prev_chunk, next_chunk)
