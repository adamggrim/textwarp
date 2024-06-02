import argparse
from typing import Callable

from textcount.constants import HelpMessages
from textcount.analysis import (get_char_count, get_mfws, get_pos_count, 
                                get_time_to_read)


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
    group.add_argument('--mfws', action='store_true', 
                       help=HelpMessages.MFWS)
    group.add_argument('--pos-count', action='store_true', 
                       help=HelpMessages.POS_COUNT)
    group.add_argument('--time-to-read', action='store_true', 
                       help=HelpMessages.TIME_TO_READ)
    args = parser.parse_args()

    # Dictionary mapping argument names to text analysis functions
    arg_func_dict = {
        'char_count': get_char_count,
        'mfws': get_mfws,
        'pos_count': get_pos_count,
        'time_to_read': get_time_to_read,
    }

    for arg_str, func in arg_func_dict.items():
        if getattr(args, arg_str):
            return func