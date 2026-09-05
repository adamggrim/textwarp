"""Functions handling punctuation."""

import regex as re

from textwarp._core.constants import patterns
from textwarp._core.context import ctx

__all__ = [
    'curly_to_straight',
    'hyphens_to_em',
    'hyphens_to_en',
    'punct_to_inside',
    'punct_to_outside',
    'remove_apostrophes',
    'straight_to_curly'
]


def curly_to_straight(text: str) -> str:
    """
    Convert curly quotes in a string to straight quotes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return ctx.provider.curly_to_straight(text)


def hyphens_to_em(text: str) -> str:
    """Convert em dash stand-ins in a string to em dashes."""
    return patterns.warping.get_em_dash_stand_in().sub('—', text)


def hyphens_to_en(text: str) -> str:
    """Convert hyphens in a string to en dashes."""
    return text.replace('-', '–')


def punct_to_inside(text: str) -> str:
    """
    Move periods and commas at the end of quotes inside quotation marks.
    """
    pattern = ctx.provider.punct_outside_pattern
    if not pattern:
        return text

    def _repl(match: re.Match[str]) -> str:
        quote, punct = match.groups()
        return punct + quote

    return pattern.sub(_repl, text)


def punct_to_outside(text: str) -> str:
    """
    Move periods and commas at the end of quotes to outside quotation
    marks.
    """
    pattern = ctx.provider.punct_inside_pattern
    if not pattern:
        return text

    def _repl(match: re.Match[str]) -> str:
        """
        Reorder periods and commas to move them outside quotation
        marks.
        """
        punct, quote = match.groups()
        return quote + punct

    return pattern.sub(_repl, text)


def remove_apostrophes(text: str) -> str:
    """
    Remove apostrophes from a string without removing single quotes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return ctx.provider.remove_apostrophes(text)


def straight_to_curly(text: str) -> str:
    """
    Convert straight quotes in a string to curly quotes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return ctx.provider.straight_to_curly(text)
