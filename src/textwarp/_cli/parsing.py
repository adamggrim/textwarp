"""Command-line argument parsing using argparse."""

import argparse
import gettext
import sys
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version

from textwarp._cli.args import ARGS_MAP
from textwarp._cli.constants.messages import HELP_DESCRIPTION
from textwarp._cli.pipeline import build_pipeline
from textwarp._core.types import Pipeline
from textwarp._cli.validation import validate_command_combinations

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
    debug: bool


def parse_args() -> ParsedArgs:
    """
    Parse command-line arguments for a text warping or analysis
    function name and the language locale.

    Returns:
        ParsedArgs: A frozen dataclass containing the parsed arguments.

    Raises:
        SystemExit: If arguments are invalid or help or version flags
        are present.
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
        __version__ = _('unknown (not installed)')

    parser = argparse.ArgumentParser(
        prog='textwarp',
        formatter_class=formatter,
        description=_(HELP_DESCRIPTION),
        usage=_('%(prog)s [options] [input_files ...] [-o output_file]')
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}',
        help=_('show version number and exit')
    )

    parser.add_argument(
        '-l', '--lang',
        type=str,
        default='en',
        help=_('set the language locale')
    )

    parser.add_argument(
        '-m', '--markdown',
        dest='markdown',
        action='store_true',
        help=_('parse text as Markdown and preserve formatting')
    )

    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        metavar='FILE',
        type=str,
        help=_('optional path to write the output file')
    )

    parser.add_argument(
        '-c', '--copy',
        dest='copy_to_clipboard',
        action='store_true',
        help=_('copy the output to the clipboard')
    )

    parser.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        help=_('enable debug mode to show full error tracebacks')
    )

    parser.add_argument(
        '-f', '--find',
        dest='find',
        type=str,
        help=_('text, case or regular expression to find')
    )

    parser.add_argument(
        '-r', '--replace',
        dest='replace',
        metavar='TEXT',
        type=str,
        help=_('replacement text')
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
        help=_('optional path to one or more input text files')
    )

    # If there are no arguments or piped input, print the help messages
    # and exit.
    if len(sys.argv) == 1 and sys.stdin.isatty():
        parser.print_help(sys.stderr)
        sys.exit(1)

    args: argparse.Namespace = parser.parse_args()

    validate_command_combinations(args, parser)
    pipeline = build_pipeline(sys.argv, parser)

    return ParsedArgs(
        pipeline=pipeline,
        lang=args.lang,
        input_files=args.input_files,
        output_file=args.output_file,
        markdown=args.markdown,
        find=args.find,
        replace=args.replace,
        copy_to_clipboard=args.copy_to_clipboard,
        debug=args.debug
    )
