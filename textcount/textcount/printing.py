import os
import textwrap

from textcount.analyzing import (get_char_count, get_mfws, get_pos_count, 
                                 get_time_to_read, get_word_count)
from textcount.formatting import (format_char_count, format_mfws, 
                                  format_pos_count, format_time_to_read, 
                                  format_word_count)



class FormatPrinting:
    """
    Class for formatting and printing text.
    """
    def print_padding() -> None:
        """Prints a blank line for padding."""
        print('')

    def print_wrapped(string: str) -> None:
        """
        Wraps printing based on the width of the terminal and adds a 
            newline character to the start of the string.

        Args:
            text (str): The string to print.
        """
        terminal_size = os.get_terminal_size()[0]
        print_size = terminal_size - 1
        wrapped_str = textwrap.fill(string, width=print_size)
        print('\n' + wrapped_str)


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