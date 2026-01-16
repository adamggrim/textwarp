"""Functions for converting between cardinal and ordinal numbers."""

import regex as re

from ._constants import WarpingPatterns


def cardinal_to_ordinal(text: str) -> str:
    """
    Convert cardinal numbers to ordinal numbers in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    def _replace_cardinal(match: re.Match[str]) -> str:
        """
        Helper function to replace a matched cardinal number with an
        ordinal.

        Args:
            match: A match object representing a cardinal
                number found in the string.

        Returns:
            str: The ordinal version of the matched cardinal.
        """
        number_str = match.group(0)
        number = int(number_str.replace(',', ''))

        suffix: str
        if 10 <= number % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')

        return number_str + suffix

    return WarpingPatterns.CARDINAL.sub(_replace_cardinal, text)


def ordinal_to_cardinal(text: str) -> str:
    """
    Convert ordinal numbers to cardinal numbers in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    def _replace_ordinal(match: re.Match[str]) -> str:
        """
        Helper function to replace a matched ordinal number with its
        cardinal equivalent.

        Args:
            match: A match object representing an ordinal number found
                in the string.

        Returns:
            str: The cardinal version of the matched ordinal.
        """
        ordinal = match.group(0)
        return ordinal[:-2]

    return WarpingPatterns.ORDINAL.sub(_replace_ordinal, text)
