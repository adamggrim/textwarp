import argparse
import sys
from typing import Callable

from textcount.constants import HelpMessages
from textcount.processing import (
    process_char_count,
    process_line_count,
    process_mfws,
    process_pos_count,
    process_time_to_read,
    process_word_count
)


def parse_args() -> Callable[[str], str]:
    """
    Parse command-line arguments for a text analysis function.

    Returns:
        Callable[[str], str]: The text analysis function corresponding
            to the specified command-line argument.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='textcount',
        description=HelpMessages.DESCRIPTION,
        usage='%(prog)s [command]'
    )
    group: argparse._MutuallyExclusiveGroup = (
        parser.add_mutually_exclusive_group(required=True)
    )
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

    # If the user enters the command name with no arguments, print help
    # messages and exit.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args: argparse.Namespace = parser.parse_args()

    # Dictionary mapping argument names to text counting functions
    arg_func_map: dict[str, Callable[[str], None]] = {
        'char_count': process_char_count,
        'line_count': process_line_count,
        'mfws': process_mfws,
        'pos_count': process_pos_count,
        'time_to_read': process_time_to_read,
        'word_count': process_word_count
    }

    for arg_label, func in arg_func_map.items():
        if getattr(args, arg_label):
            return func
