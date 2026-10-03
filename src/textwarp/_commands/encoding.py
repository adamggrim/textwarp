"""Runners for encoding and decoding commands."""

from textwarp._lib import encoding as lib_encoding

__all__ = [
    'from_binary',
    'from_hexadecimal',
    'from_morse'
]


def from_binary(binary_text: str) -> str:
    """
    Convert a string from binary, returning the original string if
    decoding fails.
    """
    try:
        return lib_encoding.from_binary(binary_text)
    except ValueError:
        return binary_text


def from_hexadecimal(text: str) -> str:
    """
    Convert a string from hexadecimal, returning the original string if
    decoding fails.
    """
    try:
        return lib_encoding.from_hexadecimal(text)
    except ValueError:
        return text


def from_morse(text: str) -> str:
    """
    Convert a string from Morse code, returning the original string if
    decoding fails.
    """
    try:
        return lib_encoding.from_morse(text)
    except ValueError:
        return text
