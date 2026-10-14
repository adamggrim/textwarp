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
    'count_sentences',
    'count_words',
    'time_to_read',
    'ttr'
]


def calculate_time_to_read(content: str | Doc, wpm: int) -> str:
    """
    Analyze, format and print time-to-read output.

    Args:
        content: The string or spaCy `Doc` to process.
        wpm: The reading speed in words per minute.
    """
    text = content if isinstance(content, str) else content.text
    minutes: int = lib_analysis.calculate_time_to_read(text, wpm)

    return format_time_to_read(minutes)


def calculate_ttr(text: str) -> str:
    """
    Analyze, format and print type-token ratio output.

    Args:
        text: The string to process.
    """
    ratio: float = lib_analysis.calculate_ttr(text)
    return format_ttr(ratio)


def count_chars(text: str) -> str:
    """
    Analyze, format and print character count output.

    Args:
        text: The string to process.
    """
    count: int = lib_analysis.count_chars(text)
    return format_count(CountLabels.CHAR.value, count)


def count_entities(content: str | Doc, number: int) -> str:
    """
    Analyze, format and print most frequent entities output.

    Args:
        content: The string or spaCy `Doc` to process.
        number: The number of entities to return.
    """
    data: list[WordCount] = lib_analysis.count_entities(content, number)

    if not data:
        return _(NO_ENTITIES_FOUND_MSG)
    return format_entity_counts(data)


def count_lines(text: str) -> str:
    """
    Analyze, format and print line count output.

    Args:
        text: The string to process.
    """
    count: int = lib_analysis.count_lines(text)
    return format_count(CountLabels.LINE.value, count)


def count_mfws(content: str | Doc, number: int) -> str:
    """
    Analyze, format and print most frequent words output.

    Args:
        content: The string or spaCy `Doc` to process.
        number: The number of most frequent words to return.
    """
    data: list[WordCount] = lib_analysis.count_mfws(content, number)

    return format_mfws(data)


def count_pos(content: str | Doc) -> str:
    """
    Analyze, format and print parts of speech count output.

    Args:
        content: The string or spaCy `Doc` to process.
    """
    counts: POSCounts = lib_analysis.count_pos(content)
    return format_pos_counts(counts)


def count_sentences(content: str | Doc) -> str:
    """
    Analyze, format and print sentence count output.

    Args:
        content: The string or spaCy `Doc` to process.
    """
    count: int = lib_analysis.count_sents(content)
    return format_count(CountLabels.SENTENCE.value, count)


def count_words(text: str) -> str:
    """
    Analyze, format and print word count output.

    Args:
        text: The string to process.
    """
    count: int = lib_analysis.count_words(text)
    return format_count(CountLabels.WORD.value, count)
