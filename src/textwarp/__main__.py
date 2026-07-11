"""The entry point of the package, containing the main loop."""

from __future__ import annotations

import sys

from textwarp._cli.parsing import parse_args
from textwarp._cli.processing import (
    process_file_mode,
    process_interactive_mode,
    process_piped_mode
)
from textwarp._cli.ui import print_padding, program_exit
from textwarp._core.context import ctx


def main() -> None:
    """
    Run the main loop for text transformation or analysis.

    Raises:
        SystemExit: If there is an error with the input file, output file,
            or if the command combinations are invalid.
    """
    try:
        parsed_args = parse_args()

        if not parsed_args.pipeline:
            return None

        ctx.set_locale(parsed_args.lang)

        if parsed_args.input_files:
            process_file_mode(parsed_args)
        elif not sys.stdin.isatty():
            process_piped_mode(parsed_args)
        else:
            process_interactive_mode(parsed_args)

    except KeyboardInterrupt:
        print_padding()
        program_exit()


if __name__ == '__main__':
    main()
