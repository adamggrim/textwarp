"""Runners for analysis commands."""

import gettext

from textwarp._cli.spinner import AcceleratingSpinner
from textwarp.analysis import (
    calculate_time_to_read,
    calculate_ttr,
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
    format_time_to_read,
    format_ttr
)
from textwarp._cli.ui import prompt_for_integer

_ = gettext.gettext

__all__ = [
    'char_count',
    'line_count',
    'mfws',
    'pos_counts',
    'sentence_count',
    'time_to_read',
    'ttr',
    'word_count'
]


def char_count(text: str) -> str:
    """
    Analyze, format and print character count output.

    Args:
        text: The string to process.
    """
    count: int = count_chars(text)
    return format_count(CountLabels.CHAR.value, count)


def line_count(text: str) -> str:
    """
    Analyze, format and print line count output.

    Args:
        text: The string to process.
    """
    count: int = count_lines(text)
    return format_count(CountLabels.LINE.value, count)



def mfws(text: str) -> str:
    """
    Analyze, format and print most frequent words output.

    Args:
        text: The string to process.
    """
    count_limit: int = prompt_for_integer(
        _(ENTER_MFW_COUNT_PROMPT),
        _(ENTER_VALID_NUMBER_PROMPT),
        allow_early_exit=True
    )

    with AcceleratingSpinner():
        data: list[WordCount] = count_mfws(text, count_limit)

    return format_mfws(data)


def pos_counts(text: str) -> str:
    """
    Analyze, format and print parts of speech count output.

    Args:
        text: The string to process.
    """
    counts: POSCounts = count_pos(text)
    return format_pos_counts(counts)


def sentence_count(text: str) -> str:
    """
    Analyze, format and print sentence count output.

    Args:
        text: The string to process.
    """
    count: int = count_sents(text)
    return format_count(CountLabels.SENTENCE.value, count)


def time_to_read(text: str) -> str:
    """
    Analyze, format and print time-to-read output.

    Args:
        text: The string to process.
    """
    wpm: int = prompt_for_integer(
        _(ENTER_WPM_PROMPT),
        _(ENTER_VALID_NUMBER_PROMPT),
        allow_early_exit=True
    )

    with AcceleratingSpinner():
        minutes: int = calculate_time_to_read(text, wpm)

    return format_time_to_read(minutes)


def ttr(text: str) -> str:
    """
    Analyze, format and print type-token ratio output.

    Args:
        text: The string to process.
    """
    ttr: float = calculate_ttr(text)
    return format_ttr(ttr)


def word_count(text: str) -> str:
    """
    Analyze, format and print word count output.

    Args:
        text: The string to process.
    """
    count: int = count_words(text)
    return format_count(CountLabels.WORD.value, count)
