"""Command-line argument parsing using argparse."""

import argparse
import gettext
import sys
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Callable

from textwarp._cli.args import (
    ARGS_MAP,
    CASING_COMMANDS,
    MUTUALLY_EXCLUSIVE_COMMANDS,
    SEPARATOR_COMMANDS
)
from textwarp._cli.constants.messages import HELP_DESCRIPTION
from textwarp._core.types import Pipeline

_ = gettext.gettext

__all__ = ['parse_args']


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
    adjustment = 6 # Account for both the "--" prefix and whitespace.
    return max(len(key) + adjustment for key in commands.keys())


def _validate_command_combinations(
    args: argparse.Namespace,
    parser: argparse.ArgumentParser
) -> None:
    """
    Validate that combined command-line arguments do not conflict.

    Args:
        args: The parsed command-line arguments.
        parser: The `ArgumentParser` instance used to display error messages.

    Raises:
        SystemExit: If there is any invalid combination of arguments.
    """
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
            _('Cannot combine multiple separator styles: {styles}').format(
                styles=', '.join(active_separators)
            )
        )
    if len(active_casings) > 1:
        parser.error(
            _('Cannot combine multiple casing styles: {styles}').format(
                styles=', '.join(active_casings)
            )
        )
    if len(active_mutually_exclusives) > 1:
        parser.error(
            _('Cannot combine multiple exclusive commands: {commands}').format(
                commands=', '.join(active_mutually_exclusives)
            )
        )
    if active_mutually_exclusives and (active_separators or active_casings):
        cmd = active_mutually_exclusives[0]
        msg = _(
            "Command '{cmd}' cannot be combined with casing or separator "
            'commands.'
        )
        parser.error(msg.format(cmd=cmd))


def parse_args() -> tuple[
    list[tuple[str, Callable[..., str]]],
    str,
    list[str],
    str | None,
    str | None,
    str | None
]:
    """
    Parse command-line arguments for a text warping or analysis
    function name and the language locale.

    Returns:
        tuple: A six-element tuple containing:
            1. list[tuple[str, Callable[..., str]]]: The pipeline list
               of command tuples.
            2. str: The language locale string (e.g., "en").
            3. list[str]: A list of optional paths to one or more input
               text files.
            4. str | None: An optional path to write the output file.
            5. str | None: The optional text, case, or regex to find.
            6. str | None: The replacement text for replacement
               commands.
    """
    max_arg_width = _calculate_max_arg_width(ARGS_MAP)

    def formatter(prog: str) -> argparse.HelpFormatter:
        """
        A custom help formatter to align help messages neatly based on
        the maximum argument width.
        """
        # Use `RawTextHelpFormatter` to preserve consecutive spaces.
        return argparse.RawTextHelpFormatter(
            prog, max_help_position=max_arg_width
        )

    try:
        __version__ = version('textwarp')
    except PackageNotFoundError:
        __version__ = 'unknown (not installed)'

    parser = argparse.ArgumentParser(
        prog='textwarp',
        formatter_class=formatter,
        description=HELP_DESCRIPTION,
        usage='%(prog)s [command]'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}',
        help='show version number and exit'
    )

    parser.add_argument(
        '-l', '--lang',
        type=str,
        default='en',
        help='set the language locale ("en" by default)'
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

    _validate_command_combinations(args, parser)

    pipeline: Pipeline = []

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

    return pipeline, args.lang
