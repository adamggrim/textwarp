from textcount.analyzing import (get_char_count, get_mfws, get_pos_count, 
                                 get_time_to_read, get_word_count)
from textcount.formatting import (FormatPrinting, format_char_count, 
                                  format_mfws, format_pos_count, 
                                  format_time_to_read, format_word_count)


def print_char_count(string) -> None:
    """
    Deploys functions to analyze, format and print character count 
        output.

    Args:
        string (str): The string to analyze.

    """
    char_count = get_char_count(string)
    char_count_str = format_char_count(char_count)
    FormatPrinting.print_wrapped(char_count_str)


def print_mfws(string, mfw_count) -> None:
    """
    Deploys functions to analyze, format and print most frequent words 
        output.

    Args:
        string (str): The string to analyze.
        mfw_count (int): The number of most frequent words to print.
    """
    mfws = get_mfws(string, mfw_count)
    mfws_str = format_mfws(mfws)
    FormatPrinting.print_wrapped(mfws_str)


def print_pos_count(string) -> None:
    """
    Deploys functions to analyze, format and print parts of speech 
        count output.

    Args:
        string (str): The string to analyze.
    """
    pos_count = get_pos_count(string)
    pos_count_str = format_pos_count(pos_count)
    FormatPrinting.print_wrapped(pos_count_str)


def print_time_to_read(string, wpm) -> None:
    """
    Deploys functions to analyze, format and print time to read output.

    Args:
        string (str): The string to analyze.
        wpm (int): The number of words per minute to print.
    """
    time_to_read = get_time_to_read(string, wpm)
    time_to_read_str = format_time_to_read(time_to_read)
    FormatPrinting.print_wrapped(time_to_read_str)


def print_word_count(string) -> None:
    """
    Deploys functions to analyze, format and print word count output. 

    Args:
        string (str): The string to analyze.
    """
    word_count = get_word_count(string)
    word_count_str = format_word_count(word_count)
    FormatPrinting.print_wrapped(word_count_str)