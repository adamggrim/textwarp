"""Command-line argument parsing using argparse."""

import argparse
import sys
from typing import (
    Any,
    Callable
)

from .._core.constants import HELP_DESCRIPTION
from .args import ARGS_MAP

__all__ = [
    'parse_args'
]


def _calculate_max_arg_width(commands: dict[str, Any]) -> int:
    """
    Calculate the length of the longest command string.

    Args:
        commands (dict): A dictionary mapping command names to their
            corresponding functions and help messages.

    Returns:
        int: The length of the longest command string, adjusted for
            formatting.
    """
    adjustment = 6 # Account for both the '--' prefix and whitespace.
    return max(len(key) + adjustment for key in commands.keys())


def parse_args() -> tuple[str, str]:
    """
    Parse command-line arguments for a text warping or analysis
    function name.

    Returns:
        tuple[str, str]: A tuple containing:
            - The command-line argument string (e.g., 'word-count').
            - The corresponding function name (e.g., 'word_count').
    """
    max_arg_width = _calculate_max_arg_width(ARGS_MAP)

    # A custom help formatter to align help messages neatly based on
    # the maximum argument length.
    formatter: Callable[[str], argparse.HelpFormatter] = (
        # Use RawTextHelpFormatter to preserve consecutive spaces.
        lambda prog: argparse.RawTextHelpFormatter(
            prog, max_help_position=max_arg_width
        )
    )

    parser = argparse.ArgumentParser(
        prog='textwarp',
        formatter_class=formatter,
        description=HELP_DESCRIPTION,
        usage='%(prog)s [command]'
    )

    group = (parser.add_mutually_exclusive_group(required=True))

    for arg_key, (_, help_message) in ARGS_MAP.items():
        group.add_argument(
            f'--{arg_key}',
            action='store_true',
            help=help_message
        )

    # If the user enters the command with no arguments, print the help
    # messages and exit.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args: argparse.Namespace = parser.parse_args()

    for arg_key, _ in ARGS_MAP.items():
        if getattr(args, arg_key.replace('-', '_')):
            command_name: str = arg_key
            func_name: str = command_name.replace('-', '_')
            return command_name, func_name
