"""Runners for analysis commands."""

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
    format_pos_count,
    format_time_to_read
)
from textwarp._cli.ui import print_wrapped, prompt_for_integer

__all__ = [
    'char_count',
    'line_count',
    'mfws',
    'pos_count',
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
    char_count: int = count_chars(text)
    formatted_char_count: str = format_count(
        CountLabels.CHAR.value, char_count
    )
    print_wrapped(formatted_char_count)


def line_count(text: str) -> None:
    """
    Analyze, format and print line count output.

    Args:
        text: The string to process.
    """
    line_count: int = count_lines(text)
    formatted_line_count: str = format_count(
        CountLabels.LINE.value, line_count
    )
    print_wrapped(formatted_line_count)


def mfws(text: str) -> None:
    """
    Analyze, format and print most frequent words output.

    Args:
        text: The string to process.
    """
    num_mfws: int = prompt_for_integer(
        ENTER_MFW_COUNT_PROMPT,
        ENTER_VALID_NUMBER_PROMPT
    )

    mfws: list[WordCount] = count_mfws(text, num_mfws)
    formatted_mfws: str = format_mfws(mfws)
    print('\n' + formatted_mfws)


def pos_count(text: str) -> None:
    """
    Analyze, format and print parts of speech count output.

    Args:
        text: The string to process.
    """
    pos_count: POSCounts = count_pos(text)
    formatted_pos_count: str = format_pos_count(pos_count)
    print('\n' + formatted_pos_count)


def sentence_count(text: str) -> None:
    """
    Analyze, format and print sentence count output.

    Args:
        text: The string to process.
    """
    sent_count: int = count_sents(text)
    formatted_sent_count: str = format_count(
        CountLabels.SENTENCE.value, sent_count
    )
    print_wrapped(formatted_sent_count)


def time_to_read(text: str) -> None:
    """
    Analyze, format and print time-to-read output.

    Args:
        text: The string to process.
    """
    wpm: int = prompt_for_integer(
        ENTER_WPM_PROMPT,
        ENTER_VALID_NUMBER_PROMPT
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
    word_count: int = count_words(text)
    formatted_word_count: str = format_count(
        CountLabels.WORD.value, word_count
    )
    print_wrapped(formatted_word_count)
