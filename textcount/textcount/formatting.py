import os
import textwrap

from textcount.constants import POS_TAGS, MAX_POS_LENGTH
from textcount.data_structures import POSCounts


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
        lines = string.splitlines()
        wrapped_lines = [textwrap.fill(line, width=print_size) for line in 
                         lines]
        wrapped_str = '\n'.join(wrapped_lines)
        print('\n' + wrapped_str)


def format_char_count(char_count: int) -> str:
    """
    Returns a string indicating the number of characters in a given 
        string.

    Args:
        char_count (int): The string to analyze.

    Returns:
        str: A formatted string indicating character count.
    """
    return f'Character count: {char_count}'


def format_line_count(line_count: int) -> str:
    """
    Returns a string indicating the number of lines in a given string.

    Args:
        line_count (int): The string to analyze.

    Returns:
        str: A formatted string indicating character count.
    """
    return f'Line count: {line_count}'


def format_mfws(mfws: list[tuple]) -> str:
    """
    Returns a string indicating the most frequent words in a given 
        string.

    Args:
        mfws (list[tuple]): A list of tuples with each tuple containing 
            a word (str) and its count (int)

    Returns:
        str: A formatted string indicating most frequent words.
    """
    word_count_strs = [f'{word}: {count}' for word, count in mfws]
    return '\n'.join(word_count_strs)


def format_pos_count(pos_counts: POSCounts) -> str:
    """
    Returns a dynamically formatted string indicating parts of speech 
        counts for a given POSCounts object.

    Args:
        pos_counts (POSCounts): The parts of speech counts.

    Returns:
        str: A formatted string indicating parts of speech counts.
    """
    pos_tuples = []
    for tag_pair in POS_TAGS:
        pos = tag_pair[1]
        count = getattr(pos_counts, f'{tag_pair[0].lower()}_count')
        ratio = getattr(pos_counts, f'{tag_pair[0].lower()}_ratio')
        pos_tuples.append((pos, count, ratio))
    max_count_length = max(len(f'{count}') for _, count, _ in pos_tuples)
    max_ratio_length = max(len(f'({ratio:.2f}%)') for _, _, ratio in 
                           pos_tuples)
    padding = 2
    results = []
    for pos, count, ratio in pos_tuples:
        formatted_ratio = f'({ratio:.2f}%)'
        # Dynamic spacing based on POS, count and ratio length
        results.append(f'{pos:{MAX_POS_LENGTH + padding}}'
                       f'{count:<{max_count_length + padding}}'
                       f'{formatted_ratio:>{max_ratio_length}}')
    return '\n'.join(results)


def format_time_to_read(minutes_to_read: int) -> str:
    """
    Returns a string indicating the time to read a given string.

    Args:
        string (str): The string to analyze.
        wpm (int): The number of words per minute.

    Returns:
        str: The formatted string indicating time to read.
    """
    hours, minutes = divmod(minutes_to_read, 60)
    if hours >= 1:
        hours_str = f'{hours} hours' if hours != 1 else '1 hour'
        if minutes == 0:
            return hours_str
        minutes_str = f'{minutes} minutes' if minutes != 1 else '1 minute'
        return f'{hours_str}, {minutes_str}'
    elif minutes >= 1:
        return f'{minutes} minutes' if minutes != 1 else '1 minute'
    else:
        return 'Less than 1 minute'


def format_word_count(word_count: int) -> str:
    """
    Returns a string indicating the number of words in a given string.

    Args:
        string (str): The string to analyze.

    Returns:
        str: The formatted string indicating word count.
    """
    return f'Word count: {word_count}'
