from ..analysis import (
    calculate_time_to_read,
    count_chars,
    count_lines,
    count_mfws,
    count_pos,
    count_sents,
    count_words
)
from .._constants import (
    ENTER_MFW_COUNT_PROMPT,
    ENTER_NUMBER_PROMPT,
    ENTER_WPM_PROMPT
)
from .._enums import CountLabels
from .._models import (
    POSCounts,
    WordCount
)
from .._formatting import (
    format_count,
    format_mfws,
    format_pos_count,
    format_time_to_read
)
from .._ui import print_wrapped

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
    def prompt_for_mfws() -> int:
        """
        Prompt the user for the number of most frequent words to
        display.

        Returns:
            int: The number of most frequent words to display.
        """
        print_wrapped(ENTER_MFW_COUNT_PROMPT)
        num_mfws_input: str = input().strip()
        while True:
            if num_mfws_input.isdigit() == True:
                return int(num_mfws_input)
            else:
                print(ENTER_NUMBER_PROMPT)
                num_mfws_input = input().strip()
                continue

    num_mfws: int = prompt_for_mfws()
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
    Analyze, format and print line count output.

    Args:
        text: The string to process.
    """
    sent_count: int = count_sents(text)
    formatted_sent_count: str = format_count(
        CountLabels.SENT.value, sent_count
    )
    print_wrapped(formatted_sent_count)


def time_to_read(text: str) -> None:
    """
    Analyze, format and print time-to-read output.

    Args:
        text: The string to process.
    """
    def prompt_for_wpm() -> int:
        """
        Prompts the user for the number of words per minute.

        Returns:
            int: The number of words per minute.
        """
        print_wrapped(ENTER_WPM_PROMPT)
        wpm_input: str = input().strip()
        while True:
            if wpm_input.isdigit() == True:
                break
            else:
                print(ENTER_NUMBER_PROMPT)
                wpm_input = input().strip()
                continue
        return int(wpm_input)
    wpm: int = prompt_for_wpm()
    time_to_read: int = calculate_time_to_read(text, wpm)
    formatted_time_to_read: str = format_time_to_read(time_to_read)
    print_wrapped(formatted_time_to_read)


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
