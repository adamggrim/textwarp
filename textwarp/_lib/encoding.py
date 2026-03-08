"""Functions for removing encoding and decoding text."""

import statistics
from collections.abc import Generator

import regex as re

from textwarp._core.config import Encoding
from textwarp._core.constants.regexes import WarpingPatterns
from textwarp._lib.punctuation import curly_to_straight

__all__ = [
    'from_binary',
    'from_hexadecimal',
    'from_morse',
    'to_binary',
    'to_hexadecimal',
    'to_morse'
]


def _get_morse_spacing_patterns(text: str) -> tuple[
    re.Pattern[str], re.Pattern[str]
]:
    """
    Determine the number of spaces for character and word separators in
    a given Morse string.

    Args:
        text: The Morse string to analyze.

    Returns:
        A tuple containing the compiled word separator pattern and
        the compiled character separator pattern.
    """
    space_matches = re.findall(r' +', text)

    if not space_matches:
        word_threshold = 3
    else:
        gap_lengths = [len(s) for s in space_matches]

        try:
            char_gap_length = statistics.mode(gap_lengths)
        except statistics.StatisticsError:
            char_gap_length = statistics.median(gap_lengths)

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
        str: The converted string.
    """
    binary_chars = binary_text.split()
    decoded_chars = [chr(int(binary, 2)) for binary in binary_chars]
    return ''.join(decoded_chars)


def from_hexadecimal(text: str) -> str:
    """
    Convert a string from hexadecimal.

    Args:
        text: The hexadecimal string to convert.

    Returns:
        str: The converted string.
    """
    normalized_text = text.replace(' ', '')
    return bytes.fromhex(normalized_text).decode('utf-8')


def from_morse(text: str) -> str:
    """
    Convert a string from Morse code.

    Args:
        text: The Morse string to convert.

    Returns:
        str: The converted string (in all caps).
    """
    text = text.strip()
    word_gap_pattern, char_gap_pattern = _get_morse_spacing_patterns(text)

    words = word_gap_pattern.split(text)
    decoded_words: list[str] = []

    reversed_morse_map = Encoding.get_morse_reversed_map()

    for w in words:
        char_codes: list[str] = char_gap_pattern.split(w)

        decoded_word = ''.join(
            reversed_morse_map.get(code, '') for code in char_codes
        )
        if decoded_word:
            decoded_words.append(decoded_word)

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
    Convert a given string to Morse code.

    Letters (A-Z), numbers (0-9) and common punctuation (., ?, !, ,, :,
    ;, +, -, =, @, (, ), ", ', /, &) are all supported.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string, with a single space between
            character codes and three spaces between word codes.
    """
    def _normalize_for_morse(text: str) -> str:
        """
        Normalize a string for Morse code by converting to all caps and
        replacing non-Morse-compatible characters.

        Args:
            text: The string to normalize.

        Returns:
            str: The normalized string.
        """
        straight_text = curly_to_straight(text.upper())
        hyphenated_text = WarpingPatterns.DASH.sub('-', straight_text)
        return hyphenated_text.replace('…', '...')

    normalized_text = _normalize_for_morse(text)
    morse_map = Encoding.get_morse_map()

    morse_words: Generator[str, None, None] = (
        ' '.join(morse_map[char] for char in word if char in morse_map)
        for word in normalized_text.split()
    )

    return '   '.join(filter(None, morse_words))
