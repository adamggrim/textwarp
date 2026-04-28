"""Universal regular expressions for text warping."""

from functools import lru_cache
from typing import Iterable

import regex as re

from textwarp._core.enums import RegexBoundary

__all__ = [
    'create_words_regex',
    'get_dash',
    'get_em_dash_stand_in',
    'get_multiple_spaces'
]


def create_words_regex(
    words: str | Iterable[str],
    boundary: RegexBoundary = RegexBoundary.WORD_BOUNDARY
) -> re.Pattern[str]:
    """
    Create a regular expression that matches any word in the given list.

    Args:
        words: A string or iterable of strings to match.
        boundary: The boundary to use around the word.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    def _add_escaped_apostrophes(word: str) -> str:
        """Add escaped straight and curly apostrophes to a word."""
        return re.escape(word).replace("'", "['’‘]")

    if isinstance(words, str):
        pattern_string = _add_escaped_apostrophes(words)
    else:
        # Sort words by length in descending order, so that longer
        # words containing other words from the set are matched first
        # (e.g., "can't've" before "can't").
        sorted_words: list[str] = sorted(
            words,
            key=len,
            reverse=True
        )
        escaped_patterns: list[str] = [
            _add_escaped_apostrophes(w) for w in sorted_words
        ]
        pattern_string = '|'.join(escaped_patterns)

    match boundary:
        case RegexBoundary.WORD_BOUNDARY:
            final_pattern = rf'(?<!\w)(?:{pattern_string})(?!\w)'
        case RegexBoundary.START_ANCHOR:
            final_pattern = rf'(?<!\w)(?:{pattern_string})'
        case RegexBoundary.END_ANCHOR:
            final_pattern = rf'(?:{pattern_string})$'

    return re.compile(final_pattern, re.IGNORECASE)


@lru_cache(maxsize=1)
def get_dash() -> re.Pattern[str]:
    """
    Get a regular expression matching an en (–) or em (—) dash.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'[–—]')


@lru_cache(maxsize=1)
def get_em_dash_stand_in() -> re.Pattern[str]:
    """
    Get a regular expression matching characters that function as an em
    dash.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'\s?--?\s?')


@lru_cache(maxsize=1)
def get_multiple_spaces() -> re.Pattern[str]:
    """
    Get a regular expression matching two or more consecutive spaces.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'(?<=\S) {2,}')


@lru_cache(maxsize=1)
def get_period_separated_initialism() -> re.Pattern[str]:
    """
    Get a regular expression matching a period-separated initialism.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'\b(?:\p{L}+\.){2,}')


@lru_cache(maxsize=1)
def get_word_character() -> re.Pattern[str]:
    """
    Get a regular expression matching any word character.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'\w')
