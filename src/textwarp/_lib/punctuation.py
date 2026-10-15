"""Functions handling punctuation."""

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
    """Convert curly quotes to straight quotes."""
    return ctx.provider.curly_to_straight(text)


def hyphens_to_em(text: str) -> str:
    """Convert em dash stand-ins to em dashes."""
    return patterns.warping.get_em_dash_stand_in().sub('—', text)


def hyphens_to_en(text: str) -> str:
    """Convert hyphens to en dashes."""
    return text.replace('-', '–')


def punct_to_inside(text: str) -> str:
    """Move periods and commas at the end of quotes inside quotation
    marks.
    """
    return ctx.provider.punct_to_inside(text)


def punct_to_outside(text: str) -> str:
    """Move periods and commas at the end of quotes outside quotation
    marks.
    """
    return ctx.provider.punct_to_outside(text)


def remove_apostrophes(text: str) -> str:
    """Remove apostrophes without removing single quotes."""
    return ctx.provider.remove_apostrophes(text)


def straight_to_curly(text: str) -> str:
    """Convert straight quotes to curly quotes."""
    return ctx.provider.straight_to_curly(text)
