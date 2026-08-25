"""Functions for encoding and decoding text."""

import statistics
from collections.abc import Generator

import regex as re

from textwarp._core.context import ctx
from textwarp._core.encoding import get_morse_map, get_morse_reversed_map

__all__ = [
    'from_binary',
    'from_hexadecimal',
    'from_morse',
    'to_binary',
    'to_hexadecimal',
    'to_morse'
]

_SPACES_PATTERN = re.compile(r' +')


def _get_morse_spacing_patterns(
    text: str
) -> tuple[re.Pattern[str], re.Pattern[str]]:
    """
    Determine the number of spaces for character and word separators in
    a given Morse string.

    Args:
        text: The Morse string to analyze.

    Returns:
        A tuple containing the compiled word separator pattern and the
        compiled character separator pattern.
    """
    space_matches = _SPACES_PATTERN.findall(text)

    if not space_matches:
        word_threshold = 3
    else:
        gap_lengths = [len(s) for s in space_matches]

        modes = statistics.multimode(gap_lengths)
        char_gap_length = int(min(modes)) if modes else int(
            statistics.median(gap_lengths)
        )

        long_gap_lengths = [L for L in gap_lengths if L > char_gap_length]

        if long_gap_lengths:
            word_gap_length = statistics.median(long_gap_lengths)
            gap_midpoint = (char_gap_length + word_gap_length) / 2
            word_threshold = int(gap_midpoint + 0.5)
        else:
            word_threshold = int(char_gap_length + 2)

    word_gap_pattern = re.compile(rf' {{{word_threshold},}}')
    char_gap_pattern = re.compile(rf' {{1,{max(1, word_threshold - 1)}}}')

    return word_gap_pattern, char_gap_pattern


def from_binary(binary_text: str) -> str:
    """
    Convert a string from binary.

    Args:
        binary_text: The space-separated binary string to convert.

    Returns:
        str: The converted string, or the original string if decoding fails.
    """
    binary_chars = binary_text.split()
    decoded_chars: list[str] = []

    for binary in binary_chars:
        try:
            decoded_chars.append(chr(int(binary, 2)))
        except ValueError:
            return binary_text

    return ''.join(decoded_chars)


def from_hexadecimal(text: str) -> str:
    """
    Convert a string from hexadecimal.

    Args:
        text: The hexadecimal string to convert.

    Returns:
        str: The converted string, or the original string if decoding
            fails.
    """
    normalized_text = text.replace(' ', '')
    try:
        return bytes.fromhex(normalized_text).decode('utf-8')
    except ValueError:
        return text


def from_morse(text: str) -> str:
    """
    Convert a string from Morse code.

    Args:
        text: The Morse string to convert.

    Returns:
        str: The converted string (in all caps).
    """
    stripped_text = text.strip()
    if not stripped_text:
        return text

    word_gap_pattern, char_gap_pattern = _get_morse_spacing_patterns(
        stripped_text
    )
    words = word_gap_pattern.split(stripped_text)

    decoded_words: list[str] = []
    reversed_morse_map = get_morse_reversed_map()

    for w in words:
        char_codes: list[str] = char_gap_pattern.split(w)
        decoded_word_chars: list[str] = []

        for code in char_codes:
            if code not in reversed_morse_map:
                return text
            decoded_word_chars.append(reversed_morse_map[code])

        decoded_words.append(''.join(decoded_word_chars))

    return ' '.join(decoded_words)


def to_binary(text: str) -> str:
    """
    Convert a string to binary.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string in binary, with each character's
            binary value separated by a space.
    """
    binary_chars = [format(ord(char), '08b') for char in text]
    return ' '.join(binary_chars)


def to_hexadecimal(text: str) -> str:
    """
    Convert a string to hexadecimal.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string in hexadecimal, with each character's
            hex value separated by a space.
    """
    return text.encode('utf-8').hex(' ')


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
    normalized_text = ctx.provider.normalize_for_morse(text)

    morse_map = get_morse_map()

    morse_words: Generator[str, None, None] = (
        ' '.join(morse_map[char] for char in word if char in morse_map)
        for word in normalized_text.split()
    )

    return '   '.join(filter(None, morse_words))
