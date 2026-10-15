"""Runners for analysis commands."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Doc

from textwarp._cli.constants.messages import NO_ENTITIES_FOUND_MSG
from textwarp._cli.formatting import (
    format_count,
    format_entity_counts,
    format_mfws,
    format_pos_counts,
    format_time_to_read,
    format_ttr
)
from textwarp._core.context import _
from textwarp._core.enums import CountLabels
from textwarp._core.models import POSCounts, WordCount
from textwarp._lib import analysis as lib_analysis

__all__ = [
    'count_chars',
    'count_entities',
    'count_lines',
    'count_mfws',
    'count_pos',
    'count_sents',
    'count_words'
]


def calculate_time_to_read(content: str | Doc, wpm: int) -> str:
    """Analyze and format time-to-read output.

    Args:
        content: The string or spaCy `Doc` to process.
        wpm: The reading speed in words per minute.

    Returns:
        str: The formatted time-to-read string.
    """
    text = content if isinstance(content, str) else content.text
    minutes: int = lib_analysis.calculate_time_to_read(text, wpm)

    return format_time_to_read(minutes)


def calculate_ttr(text: str) -> str:
    """Analyze and format type-token ratio output."""
    ratio: float = lib_analysis.calculate_ttr(text)
    return format_ttr(ratio)


def count_chars(text: str) -> str:
    """Analyze and format character count output."""
    count: int = lib_analysis.count_chars(text)
    return format_count(CountLabels.CHAR.value, count)


def count_entities(content: str | Doc, number: int) -> str:
    """Analyze and format entity counts output.

    Args:
        content: The string or spaCy `Doc` to process.
        number: The number of entities to return.

    Returns:
        str: The formatted entity counts table, or a message if none are
            found.
    """
    data: list[WordCount] = lib_analysis.count_entities(content, number)

    if not data:
        return _(NO_ENTITIES_FOUND_MSG)
    return format_entity_counts(data)


def count_lines(text: str) -> str:
    """Analyze and format line count output."""
    count: int = lib_analysis.count_lines(text)
    return format_count(CountLabels.LINE.value, count)


def count_mfws(content: str | Doc, number: int) -> str:
    """Analyze and format most frequent words output.

    Args:
        content: The string or spaCy `Doc` to process.
        number: The number of most frequent words to return.

    Returns:
        str: The formatted most frequent words table.
    """
    data: list[WordCount] = lib_analysis.count_mfws(content, number)

    return format_mfws(data)


def count_pos(content: str | Doc) -> str:
    """Analyze and format parts-of-speech count output.

    Args:
        content: The string or spaCy `Doc` to process.

    Returns:
        str: The formatted parts-of-speech counts table.
    """
    counts: POSCounts = lib_analysis.count_pos(content)
    return format_pos_counts(counts)


def count_sents(content: str | Doc) -> str:
    """Analyze and format sentence count output."""
    count: int = lib_analysis.count_sents(content)
    return format_count(CountLabels.SENTENCE.value, count)


def count_words(text: str) -> str:
    """Analyze and format word count output."""
    count: int = lib_analysis.count_words(text)
    return format_count(CountLabels.WORD.value, count)
