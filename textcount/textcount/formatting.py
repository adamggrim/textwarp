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


    def print_wrapped(text: str) -> None:
        """
        Wraps printing based on the width of the terminal and adds a 
            newline character to the start of the string.
        
        Args:
            text: The string to print.
        """
        terminal_size: int = os.get_terminal_size()[0]
        print_size: int = terminal_size - 1
        wrapped_text: str = textwrap.fill(text, width=print_size)
        print('\n' + wrapped_text)


def format_count(name: str, count: int) -> str:
    """
    Returns a string indicating the count of a specific analysis.

    Args:
        name: The name of the count.
        count: The count to display.

    Returns:
        str: A formatted string indicating the name and count.
    """
    return f'{name} count: {count}'


def format_mfws(mfws: list[tuple]) -> str:
    """
    Returns a string indicating the most frequent words in a given 
        string.

    Args:
        mfws: A list of tuples with each tuple containing a word and its 
            count.

    Returns:
        str: A formatted string indicating most frequent words.
    """
    formatted_word_counts: list[str] = [f'{word}: {count}' for word, count in mfws]
    return '\n'.join(formatted_word_counts)


def format_pos_count(pos_counts: POSCounts) -> str:
    """
    Returns a dynamically formatted string indicating parts of speech 
        counts for a given POSCounts object.

    Args:
        pos_counts: The parts of speech counts.

    Returns:
        str: A formatted string indicating parts of speech counts.
    """
    pos_tuples: list[tuple[str, int, float]] = []
    for tag_pair in POS_TAGS:
        pos: str = tag_pair[1]
        count: int = getattr(pos_counts, f'{tag_pair[0].lower()}_count')
        ratio: float = getattr(pos_counts, f'{tag_pair[0].lower()}_ratio')
        pos_tuples.append((pos, count, ratio))
    max_count_length: int = max(len(f'{count}') for _, count, _ in pos_tuples)
    max_ratio_length: int = max(len(f'({ratio:.2f}%)') for _, _, ratio in 
                           pos_tuples)
    padding: int = 2
    results: list[str] = []
    for pos, count, ratio in pos_tuples:
        formatted_ratio: str = f'({ratio:.2f}%)'
        # Dynamic spacing based on POS, count and ratio length
        results.append(f'{pos:{MAX_POS_LENGTH + padding}}'
                       f'{count:<{max_count_length + padding}}'
                       f'{formatted_ratio:>{max_ratio_length}}')
    return '\n'.join(results)


def format_time_to_read(minutes_to_read: int) -> str:
    """
    Returns a string indicating the time to read a given string.

    Args:
        minutes_to_read (int): The number of minutes.

    Returns:
        str: The formatted string indicating time to read.
    """
    hours: int
    minutes: int
    hours, minutes = divmod(minutes_to_read, 60)
    if hours >= 1:
        formatted_hours = f'{hours} hours' if hours != 1 else '1 hour'
        if minutes == 0:
            return formatted_hours
        formatted_minutes = f'{minutes} minutes' if minutes != 1 else '1 minute'
        return f'{formatted_hours}, {formatted_minutes}'
    elif minutes >= 1:
        return f'{minutes} minutes' if minutes != 1 else '1 minute'
    else:
        return 'Less than 1 minute'
