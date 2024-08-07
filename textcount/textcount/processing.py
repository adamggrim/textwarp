from textcount.analyzing import (get_char_count, get_line_count, get_mfws, 
                                 get_pos_count, get_time_to_read, 
                                 get_word_count)
from textcount.constants import (FormatCountStrings, ENTER_MFW_COUNT_STR, ENTER_NUMBER_STR, 
                                 ENTER_WPM_STR)
from textcount.formatting import (FormatPrinting, format_count, 
                                  format_mfws, format_pos_count, 
                                  format_time_to_read)


def process_char_count(string: str) -> None:
    """
    Deploys functions to analyze, format and print character count 
        output.

    Args:
        string (str): The string to analyze.

    """
    char_count = get_char_count(string)
    char_count_str = format_count(FormatCountStrings.CHAR_STR, char_count)
    FormatPrinting.print_wrapped(char_count_str)


def process_line_count(string: str) -> None:
    """
    Deploys functions to analyze, format and print line count output.

    Args:
        string (str): The string to analyze.
    """
    line_count = get_line_count(string)
    line_count_str = format_count(FormatCountStrings.LINE_STR, line_count)
    FormatPrinting.print_wrapped(line_count_str)


def process_mfws(string: str) -> None:
    """
    Deploys functions to analyze, format and print most frequent words 
        output.

    Args:
        string (str): The string to analyze.
    """
    def get_mfw_count() -> int:
        """
        Prompts the user for the number of most frequent words to 
            display.

        Returns:
            int: The number of most frequent words to display.
        """
        FormatPrinting.print_wrapped(ENTER_MFW_COUNT_STR)
        mfw_count = input().strip()
        while True:
            if mfw_count.isdigit() == True:
                break
            else:
                print(ENTER_NUMBER_STR)
                mfw_count = input().strip()
                continue
        return int(mfw_count)
    mfw_count = get_mfw_count()
    mfws = get_mfws(string, mfw_count)
    mfws_str = format_mfws(mfws)
    FormatPrinting.print_wrapped(mfws_str)


def process_pos_count(string: str) -> None:
    """
    Deploys functions to analyze, format and print parts of speech 
        count output.

    Args:
        string (str): The string to analyze.
    """
    pos_count = get_pos_count(string)
    pos_count_str = format_pos_count(pos_count)
    FormatPrinting.print_wrapped(pos_count_str)


def process_time_to_read(string: str) -> None:
    """
    Deploys functions to analyze, format and print time to read output.

    Args:
        string (str): The string to analyze.
    """
    def get_wpm() -> int:
        """
        Prompts the user for the number of words per minute.

        Returns:
            int: The number of words per minute.
        """
        FormatPrinting.print_wrapped(ENTER_WPM_STR)
        wpm = input().strip()
        while True:
            if wpm.isdigit() == True:
                break
            else:
                print(ENTER_NUMBER_STR)
                wpm = input().strip()
                continue
        return int(wpm)
    wpm = get_wpm()
    time_to_read = get_time_to_read(string, wpm)
    time_to_read_str = format_time_to_read(time_to_read)
    FormatPrinting.print_wrapped(time_to_read_str)


def process_word_count(string: str) -> None:
    """
    Deploys functions to analyze, format and print word count output. 

    Args:
        string (str): The string to analyze.
    """
    word_count = get_word_count(string)
    word_count_str = format_count(FormatCountStrings.WORD_STR, word_count)
    FormatPrinting.print_wrapped(word_count_str)
