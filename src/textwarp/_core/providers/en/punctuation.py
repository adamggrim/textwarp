"""English-specific functions handling punctuation."""

import regex as re

from textwarp._core.providers import en
from textwarp._core.providers.en.constants import CURLY_TO_STRAIGHT_TABLE

__all__ = [
    'curly_to_straight',
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
    return text.translate(CURLY_TO_STRAIGHT_TABLE)


def punct_to_inside(text: str) -> str:
    """
    Move periods and commas at the end of quotes inside quotation marks.
    """
    def _repl(match: re.Match[str]) -> str:
        quote, punct = match.groups()
        return f'{punct}{quote}'

    return en.patterns.get_punct_outside().sub(_repl, text)


def punct_to_outside(text: str) -> str:
    """
    Move periods and commas at the end of quotes outside quotation
    marks.
    """
    def _repl(match: re.Match[str]) -> str:
        punct, quote = match.groups()
        return f'{quote}{punct}'

    return en.patterns.get_punct_inside().sub(_repl, text)


def remove_apostrophes(text: str) -> str:
    """
    Remove apostrophes from a string without removing single quotes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return en.patterns.get_apostrophe_in_word().sub('', text)


def straight_to_curly(text: str) -> str:
    """
    Convert straight quotes in a string to curly quotes.

    Args:
        text: The string to convert.

    Returns:
        curly_text: The converted string.
    """
    # Convert any straight apostrophes first (contractions, decades or
    # elisions).
    text = en.patterns.get_apostrophe_in_word().sub('’', text)

    chars = list(text)

    for i, char in enumerate(chars):
        if char not in "'\"":
            continue

        prev_char = chars[i - 1] if i else None
        prev_prev_char = chars[i - 2] if i > 1 else None

        is_opening_context = (
            prev_char is None or prev_char in ' \t\n\r([{—–"\u201c\u2018\''
        )
        is_preceded_by_whitespace = (
            prev_char is not None and prev_char in ' \t\n\r'
        )

        if char == "'":
            is_opener = (
                is_opening_context
                or (is_preceded_by_whitespace and prev_prev_char in ('"', '“'))
            )
            chars[i] = '‘' if is_opener else '’'

        elif char == '"':
            # Exception for double quotes preceded by a space and single
            # quote.
            is_opener = (
                is_opening_context
                and not (
                    is_preceded_by_whitespace
                    and prev_prev_char in ("'", '’', '‘')
                )
            )
            chars[i] = '“' if is_opener else '”'

    return ''.join(chars)
