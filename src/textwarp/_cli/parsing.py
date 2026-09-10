"""Command-line argument parsing using argparse."""

import argparse
import gettext
import sys
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from typing_extensions import Final

from textwarp._cli.args import ARGS_MAP
from textwarp._cli.constants.messages import HELP_DESCRIPTION
from textwarp._cli.pipeline import build_pipeline
from textwarp._cli.ui import get_terminal_width, wrap_text
from textwarp._core.types import Pipeline
from textwarp._cli.validation import validate_command_combinations

_ = gettext.gettext

__all__ = ['parse_args', 'ParsedArgs']

DEFAULT_MAX_FILE_MB: Final = 100

_INDENT: Final = 2
_CMD_WIDTH: Final = 20
_SEPARATOR: Final = 1
_LEFT_MARGIN: Final = (
    _INDENT + _CMD_WIDTH + _SEPARATOR
)


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
    max_file_mb: int


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
        # Use `RawDescriptionHelpFormatter` to preserve command
        # formatting.
        return argparse.RawDescriptionHelpFormatter(
            prog, max_help_position=79
        )

    try:
        __version__ = version('textwarp')
    except PackageNotFoundError:
        __version__ = _('unknown (not installed)')

    terminal_width = get_terminal_width()
    text_width = max(terminal_width - (_LEFT_MARGIN + 2), 10)

    epilog_lines = [_('commands:')]
    for arg_key, cmd in sorted(ARGS_MAP.items()):
        help_text = _(cmd.help_text)
        wrapped_help = wrap_text(help_text, text_width)

        if wrapped_help:
            epilog_lines.append(
                f"{' ' * _INDENT}"
                f'{arg_key:<{_CMD_WIDTH}}'
                f"{' ' * _SEPARATOR}"
                f'{wrapped_help[0]}'
            )
            for line in wrapped_help[1:]:
                epilog_lines.append(f"{' ' * _LEFT_MARGIN}{line}")
        else:
            epilog_lines.append(f"{' ' * _INDENT}{arg_key:<{_CMD_WIDTH}}")

    parser = argparse.ArgumentParser(
        prog='textwarp',
        formatter_class=formatter,
        description=_(HELP_DESCRIPTION),
        usage=_(
            '%(prog)s [options] [commands ...] [input_files ...] '
            '[-o output_file]'
        ),
        epilog='\n'.join(epilog_lines)
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

    parser.add_argument(
        '--max-file-mb',
        dest='max_file_mb',
        metavar='MB',
        type=int,
        default=DEFAULT_MAX_FILE_MB,
        help=_('maximum file size for in-memory processing')
    )

    parser.add_argument(
        'commands',
        nargs='*',
        type=str,
        help=argparse.SUPPRESS
    )

    # If there are no arguments or piped input, print the help messages
    # and exit.
    if len(sys.argv) == 1 and sys.stdin.isatty():
        parser.print_help(sys.stderr)
        sys.exit(1)

    args: argparse.Namespace = parser.parse_args()

    active_cmds = [p for p in args.commands if p in ARGS_MAP]
    input_files = [p for p in args.commands if p not in ARGS_MAP]

    validate_command_combinations(active_cmds, args, parser)
    pipeline = build_pipeline(active_cmds, parser)

    return ParsedArgs(
        pipeline=pipeline,
        lang=args.lang,
        input_files=input_files,
        output_file=args.output_file,
        markdown=args.markdown,
        find=args.find,
        replace=args.replace,
        copy_to_clipboard=args.copy_to_clipboard,
        debug=args.debug,
        max_file_mb=args.max_file_mb
    )
