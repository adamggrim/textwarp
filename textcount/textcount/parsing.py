import argparse
from typing import Callable

from textcount.constants import HelpMessages
from textcount.processing import (process_char_count, process_line_count, 
                                  process_mfws, process_pos_count, 
                                  process_time_to_read, process_word_count)


def parse_args() -> Callable[[str], str]:
    """
    Parses command-line arguments for a text analysis function 
        specification.

    Returns:
        Callable[[str], str]: The text analysis function corresponding 
            to the specified command-line argument.
    """
    parser = argparse.ArgumentParser(description=HelpMessages.DESCRIPTION)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--char-count', action='store_true', 
                       help=HelpMessages.CHAR_COUNT)
    group.add_argument('--line-count', action='store_true', 
                       help=HelpMessages.LINE_COUNT)
    group.add_argument('--mfws', action='store_true', 
                       help=HelpMessages.MFWS)
    group.add_argument('--pos-count', action='store_true', 
                       help=HelpMessages.POS_COUNT)
    group.add_argument('--time-to-read', action='store_true', 
                       help=HelpMessages.TIME_TO_READ)
    group.add_argument('--word-count', action='store_true', 
                       help=HelpMessages.WORD_COUNT)
    args = parser.parse_args()

    # Dictionary mapping argument names to text counting functions
    arg_func_dict = {
        'char_count': process_char_count,
        'line_count': process_line_count,
        'mfws': process_mfws,
        'pos_count': process_pos_count,
        'time_to_read': process_time_to_read,
        'word_count': process_word_count
    }

    for arg_str, func in arg_func_dict.items():
        if getattr(args, arg_str):
            return func
