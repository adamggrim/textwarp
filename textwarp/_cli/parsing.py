"""Command-line argument parsing using argparse."""

import argparse
import gettext
import sys
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version

from textwarp._cli.args import (
    ARGS_MAP,
    CASING_COMMANDS,
    MUTUALLY_EXCLUSIVE_COMMANDS,
    REPLACEMENT_COMMANDS,
    SEPARATOR_COMMANDS
)
from textwarp._cli.constants.messages import HELP_DESCRIPTION
from textwarp._core.types import Pipeline

_ = gettext.gettext

__all__ = ['parse_args', 'ParsedArgs']


@dataclass(frozen=True)
class ParsedArgs:
    """Data class containing parsed command-line arguments."""
    pipeline: Pipeline
    lang: str
    input_files: list[str]
    output_file: str | None
    markdown: bool
    find: str | None
    replace: str | None
    copy_to_clipboard: bool


def _validate_command_combinations(
    args: argparse.Namespace,
    parser: argparse.ArgumentParser
) -> None:
    """
    Validate that combined command-line arguments do not conflict.

    Args:
        args: The parsed command-line arguments.
        parser: The `ArgumentParser` instance used to display error
            messages.

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

    is_replacement_cmd = any(c in REPLACEMENT_COMMANDS for c in active_cmds)
    if (args.find or args.replace) and not is_replacement_cmd:
        parser.error(
            _(
                'The --find (-f) and --replace (-r) arguments can only '
                'be used with replacement commands (--replace, '
                '--replace-case, --replace-regex).'
            )
        )

    if args.markdown:
        if active_separators:
            parser.error(
                _(
                    'The --markdown flag cannot be combined with manual '
                    'separator commands: {styles}'
                ).format(styles=', '.join(active_separators))
            )


def parse_args() -> ParsedArgs:
    """
    Parse command-line arguments for a text warping or analysis
    function name and the language locale.

    Returns:
        ParsedArgs: A frozen dataclass containing the parsed arguments.
    """
    def formatter(prog: str) -> argparse.HelpFormatter:
        """
        A custom help formatter to align help messages neatly based on
        the maximum argument width.
        """
        # Use `RawTextHelpFormatter` to preserve consecutive spaces.
        return argparse.RawTextHelpFormatter(
            prog, max_help_position=79
        )

    try:
        __version__ = version('textwarp')
    except PackageNotFoundError:
        __version__ = 'unknown (not installed)'

    parser = argparse.ArgumentParser(
        prog='textwarp',
        formatter_class=formatter,
        description=_(HELP_DESCRIPTION),
        usage='%(prog)s [options] [input_files ...] [-o output_file]'
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
        help='set the language locale'
    )

    parser.add_argument(
        '-m', '--markdown',
        dest='markdown',
        action='store_true',
        help='parse text as Markdown and preserve formatting'
    )

    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        metavar='FILE',
        type=str,
        help='optional path to write the output file'
    )

    parser.add_argument(
        '-c', '--copy',
        dest='copy_to_clipboard',
        action='store_true',
        help='copy the output to the clipboard'
    )

    parser.add_argument(
        '-f', '--find',
        dest='find',
        type=str,
        help='text, case or regular expression to find'
    )

    parser.add_argument(
        '-r', '--replace',
        dest='replace',
        metavar='TEXT',
        type=str,
        help='replacement text'
    )

    for arg_key, (_func, help_msg) in ARGS_MAP.items():
        parser.add_argument(
            f'--{arg_key}',
            action='store_true',
            help=_(help_msg)
        )

    parser.add_argument(
        'input_files',
        nargs='*',
        type=str,
        help='optional path to one or more input text files'
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

    return ParsedArgs(
        pipeline=pipeline,
        lang=args.lang,
        input_files=args.input_files,
        output_file=args.output_file,
        markdown=args.markdown,
        find=args.find,
        replace=args.replace,
        copy_to_clipboard=args.copy_to_clipboard
    )
