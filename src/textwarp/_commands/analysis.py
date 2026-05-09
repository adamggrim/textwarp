"""Runners for analysis commands."""

import gettext

from textwarp.analysis import (
    calculate_time_to_read,
    count_chars,
    count_lines,
    count_mfws,
    count_pos,
    count_sents,
    count_words
)
from textwarp._cli.constants.messages import (
    ENTER_MFW_COUNT_PROMPT,
    ENTER_VALID_NUMBER_PROMPT,
    ENTER_WPM_PROMPT
)
from textwarp._core.enums import CountLabels
from textwarp._core.models import POSCounts, WordCount
from textwarp._cli.formatting import (
    format_count,
    format_mfws,
    format_pos_counts,
    format_time_to_read
)
from textwarp._cli.ui import print_wrapped, prompt_for_integer

_ = gettext.gettext

__all__ = [
    'char_count',
    'line_count',
    'mfws',
    'pos_counts',
    'sentence_count',
    'time_to_read',
    'word_count'
]


def char_count(text: str) -> None:
    """
    Analyze, format and print character count output.

    Args:
        text: The string to process.
    """
    count: int = count_chars(text)
    formatted_count: str = format_count(CountLabels.CHAR.value, count)
    print_wrapped(formatted_count)


def line_count(text: str) -> None:
    """
    Analyze, format and print line count output.

    Args:
        text: The string to process.
    """
    count: int = count_lines(text)
    formatted_count: str = format_count(CountLabels.LINE.value, count)
    print_wrapped(formatted_count)


def mfws(text: str) -> None:
    """
    Analyze, format and print most frequent words output.

    Args:
        text: The string to process.
    """
    count_limit: int = prompt_for_integer(
        _(ENTER_MFW_COUNT_PROMPT),
        _(ENTER_VALID_NUMBER_PROMPT)
    )

    data: list[WordCount] = count_mfws(text, count_limit)
    formatted_data: str = format_mfws(data)
    print('\n' + formatted_data)


def pos_counts(text: str) -> None:
    """
    Analyze, format and print parts of speech count output.

    Args:
        text: The string to process.
    """
    counts: POSCounts = count_pos(text)
    formatted_count: str = format_pos_counts(counts)
    print('\n' + formatted_count)


def sentence_count(text: str) -> None:
    """
    Analyze, format and print sentence count output.

    Args:
        text: The string to process.
    """
    count: int = count_sents(text)
    formatted_count: str = format_count(
        CountLabels.SENTENCE.value, count
    )
    print_wrapped(formatted_count)


def time_to_read(text: str) -> None:
    """
    Analyze, format and print time-to-read output.

    Args:
        text: The string to process.
    """
    wpm: int = prompt_for_integer(
        _(ENTER_WPM_PROMPT),
        _(ENTER_VALID_NUMBER_PROMPT)
    )

    minutes: int = calculate_time_to_read(text, wpm)
    formatted_minutes: str = format_time_to_read(minutes)
    print_wrapped(formatted_minutes)


def word_count(text: str) -> None:
    """
    Analyze, format and print word count output.

    Args:
        text: The string to process.
    """
    count: int = count_words(text)
    formatted_count: str = format_count(
        CountLabels.WORD.value, count
    )
    print_wrapped(formatted_count)
