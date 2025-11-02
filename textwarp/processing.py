from .analysis import (
    calculate_time_to_read,
    count_chars,
    count_lines,
    count_mfws,
    count_pos,
    count_sents,
    count_words
)
from ._constants import (
    ENTER_MFWS_PROMPT,
    ENTER_NUMBER_PROMPT,
    ENTER_WPM_PROMPT
)
from _enums import CountLabels
from _input_output import print_wrapped
from ._pos_counts import POSCounts
from ._formatting import (
    format_count,
    format_mfws,
    format_pos_count,
    format_time_to_read
)


def char_count(text: str) -> None:
    """
    Deploy functions to analyze, format and print character count
        output.

    Args:
        text: The string to process.
    """
    char_count: int = count_chars(text)
    formatted_char_count: str = format_count(FormatCountLabels.CHAR, char_count)
    print_wrapped(formatted_char_count)


def line_count(text: str) -> None:
    """
    Deploy functions to analyze, format and print line count output.

    Args:
        text: The string to process.
    """
    line_count: int = count_lines(text)
    formatted_line_count: str = format_count(FormatCountLabels.LINE, line_count)
    print_wrapped(formatted_line_count)


def mfws(text: str) -> None:
    """
    Deploy functions to analyze, format and print most frequent words
    output.

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
        mfw_count_input: str = input().strip()
        while True:
            if mfw_count_input.isdigit() == True:
                break
            else:
                print(ENTER_NUMBER_PROMPT)
                mfw_count_input = input().strip()
                continue
        return int(mfw_count_input)
    mfw_count: int = prompt_for_mfw_count()
    mfws: list[tuple] = count_mfws(text, mfw_count)
    formatted_mfws: str = format_mfws(mfws)
    print_wrapped(formatted_mfws)


def pos_count(text: str) -> None:
    """
    Deploy functions to analyze, format and print parts of speech count
    output.

    Args:
        text: The string to process.
    """
    pos_count: POSCounts = count_pos(text)
    formatted_pos_count: str = format_pos_count(pos_count)
    print_wrapped(formatted_pos_count)


def time_to_read(text: str) -> None:
    """
    Deploy functions to analyze, format and print time to read output.

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
    Deploy functions to analyze, format and print word count output.

    Args:
        text: The string to process.
    """
    word_count: int = count_words(text)
    formatted_word_count: str = format_count(FormatCountLabels.WORD, word_count)
    print_wrapped(formatted_word_count)
