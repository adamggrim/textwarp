"""Functions for removing encoding and decoding text."""

from collections.abc import Generator

from .punctuation import curly_to_straight
from .._core import (
    Encoding,
    WarpingPatterns
)

__all__ = [
    'from_binary',
    'from_hexadecimal',
    'from_morse',
    'to_binary',
    'to_hexadecimal',
    'to_morse'
]


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
    chars = [chr(int(hex_char, 16)) for hex_char in text.split()]
    return ''.join(chars)


def from_morse(text: str) -> str:
    """
    Convert a string from Morse code.

    Args:
        text: The Morse string to convert.

    Returns:
        str: The converted string (in all caps).
    """
    words = text.strip().split('   ')
    decoded_words: list[str] = []

    reversed_morse_map = Encoding.get_morse_reversed_map()

    for w in words:
        char_codes: list[str] = w.split()
        decoded_word = ''.join(
            reversed_morse_map.get(code, '') for code in char_codes
        )
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
    straight_text = curly_to_straight(text)
    hex_chars = [format(ord(char), '02x') for char in straight_text]
    return ' '.join(hex_chars)


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
