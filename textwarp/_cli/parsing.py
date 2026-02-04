"""Command-line argument parsing using argparse."""

import argparse
import sys
from typing import Any, Callable

from .._core.constants import HELP_DESCRIPTION
from .args import (
    ARGS_MAP,
    CASING_COMMANDS,
    MUTUALLY_EXCLUSIVE_COMMANDS,
    SEPARATOR_COMMANDS
)

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


def parse_args() -> list[tuple[str, Callable[[str], str]]]:
    """
    Parse command-line arguments for a text warping or analysis
    function name.

    Returns:
        list[tuple[str, Callable[[str], str]]]: A list of tuples
            containing:
            - The command-line argument string (e.g., 'word-count').
            - The corresponding callable function (e.g., 'word_count').
    """
    max_arg_width = _calculate_max_arg_width(ARGS_MAP)

    def formatter(prog: str) -> argparse.HelpFormatter:
        """
        A custom help formatter to align help messages neatly based on
        the maximum argument width.
        """
        # Use RawTextHelpFormatter to preserve consecutive spaces.
        return argparse.RawTextHelpFormatter(
            prog, max_help_position=max_arg_width
        )

    parser = argparse.ArgumentParser(
        prog='textwarp',
        formatter_class=formatter,
        description=HELP_DESCRIPTION,
        usage='%(prog)s [command]'
    )

    for arg_key, (_, help_message) in ARGS_MAP.items():
        parser.add_argument(
            f'--{arg_key}',
            action='store_true',
            help=help_message
        )

    # If there are no arguments or piped input, print the help messages
    # and exit.
    if len(sys.argv) == 1 and sys.stdin.isatty():
        parser.print_help(sys.stderr)
        sys.exit(1)

    args: argparse.Namespace = parser.parse_args()

    active_cmds = [
        key for key in ARGS_MAP
        if getattr(args, key.replace('-', '_'), False)
    ]

    active_separators = [c for c in active_cmds if c in SEPARATOR_COMMANDS]
    active_casings = [c for c in active_cmds if c in CASING_COMMANDS]
    active_mutually_exclusives = [
        c for c in active_cmds if c in MUTUALLY_EXCLUSIVE_COMMANDS
    ]

    if len(active_separators) > 1:
        parser.error(
            f'Cannot combine multiple separator styles: '
            f"{', '.join(active_separators)}"
        )
    if len(active_casings) > 1:
        parser.error(
            f'Cannot combine multiple casing styles: '
            f"{', '.join(active_casings)}"
        )
    if len(active_mutually_exclusives) > 1:
        parser.error(
            f'Cannot combine multiple exclusive commands: '
            f"{', '.join(active_mutually_exclusives)}"
        )
    if active_mutually_exclusives and (active_separators or active_casings):
        cmd = active_mutually_exclusives[0]
        parser.error(
            f"Command '{cmd}' cannot be combined with casing or separator "
            f'commands.'
        )

    pipeline: list[tuple[str, Callable[[str], str]]] = []

    for arg in sys.argv[1:]:
        if not arg.startswith('-'):
            continue

        cmd_key = arg.lstrip('-')

        if cmd_key in ARGS_MAP:
            func = ARGS_MAP[cmd_key][0]
            pipeline.append((cmd_key, func))

    if not pipeline:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return pipeline
