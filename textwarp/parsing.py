import argparse
import sys
from typing import Callable

from textwarp.args import ARGS_MAP
from textwarp.constants import HELP_DESCRIPTION


def parse_args() -> Callable[[str], str]:
    """
    Parse command-line arguments for a text warping function.

    Returns:
        Callable[[str], str]: The text warping function corresponding
            to the specified command-line argument.
    """
    max_arg_width = _calculate_max_arg_width(ARGS_MAP)

    # A custom help formatter to align help messages neatly based on
    # the maximum argument length.
    formatter: Callable[[str], argparse.HelpFormatter] = (
        lambda prog: argparse.HelpFormatter(
            prog, max_help_position=max_arg_width
        )
    )

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='textwarp',
        formatter_class=formatter,
        description=HELP_DESCRIPTION,
        usage='%(prog)s [command]'
    )

    group: argparse._MutuallyExclusiveGroup = (
        parser.add_mutually_exclusive_group(required=True)
    )

    for arg_key, (_, help_message) in ARGS_MAP.items():
        group.add_argument(
            f'--{arg_key}',
            action='store_true',
            help=help_message
        )

    # If the user enters the command name with no arguments, print the
    # help messages and exit.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args: argparse.Namespace = parser.parse_args()

    for arg_key, (func, _) in ARGS_MAP.items():
        if getattr(args, arg_key.replace('-', '_')):
            return func


def _calculate_max_arg_width(commands: dict) -> int:
    """
    Calculate the length of the longest command string.

    Args:
        commands (dict): A dictionary mapping command names to their
            corresponding functions and help messages.

    Returns:
        int: The length of the longest command string, adjusted for
            formatting.
    """
    adjustment: int = 6 # Account for the '--' prefix and whitespace.
    return max(len(key) + adjustment for key in commands.keys())
