"""English-specific functions for encoding and decoding text."""

from textwarp._core.constants import patterns
from textwarp._lib.punctuation import curly_to_straight


def normalize_for_morse(text: str) -> str:
    """
    Normalize a string for Morse code by converting to all caps and
    replacing non-Morse-compatible characters.

    Args:
        text: The string to normalize.

    Returns:
        str: The normalized string.
    """
    straight_text = curly_to_straight(text.upper())
    hyphenated_text = patterns.warping.get_dash().sub('-', straight_text)
    return hyphenated_text.replace('…', '...')
