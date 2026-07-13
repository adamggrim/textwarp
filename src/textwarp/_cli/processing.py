"""Execution modes for pipeline processing."""

import gettext
import sys
from typing import Callable

from textwarp._cli.parsing import ParsedArgs
from textwarp._cli.pipeline import (
    REPLACEMENT_FUNC_NAMES,
    handle_output,
    is_analysis_pipeline,
    route_output,
    route_text,
    validate_piped_commands
)
from textwarp._cli.runners import (
    replace_text,
    run_command_loop,
    warp_and_copy
)
from textwarp._cli.ui import print_wrapped, program_exit

_ = gettext.gettext


def process_file_mode(args: ParsedArgs) -> None:
    """
    Handle file input and output mode.

    Args:
        args: The parsed command-line arguments.

    Raises:
        SystemExit: If the input file is unreadable or if there is an
            error writing to the output file.
    """
    validate_piped_commands(args.pipeline, args.find, args.replace)

    combined_results: list[str] = []
    is_analysis = is_analysis_pipeline(args.pipeline)

    for file_path in args.input_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
            print_wrapped(
                _(
                    "Error: '{input_file}' appears to be a binary file. "
                    'Please provide a valid text file.'
                ).format(input_file=file_path)
            )
            sys.exit(1)
        except OSError as e:
            print_wrapped(
                _("Error accessing file '{file_path}': {error}").format(
                    file_path=file_path,
                    error=e
                ))
            sys.exit(1)

        if text.endswith('\n'):
            text = text[:-1]

        result = route_text(
            text,
            args.pipeline,
            args.markdown,
            args.find,
            args.replace
        )

        if result is not None:
            if is_analysis and len(args.input_files) > 1:
                result = f'\n--- {file_path} ---\n{result}'

            combined_results.append(result)

    if combined_results:
        final_output = '\n'.join(combined_results)
        route_output(
            final_output, args.output_file, args.copy_to_clipboard, args.debug
        )


def process_interactive_mode(args: ParsedArgs) -> None:
    """
    Handle the interactive CLI interface for user input without files or
    piping.

    This mode acts as a wrapper around the package's core pipeline engine.

    Args:
        args: The parsed command-line arguments.

    Raises:
        SystemExit: If the user exits the loop or a replacement command
            is in the pipeline.
    """
    def pipeline_runner(text: str) -> str | None:
        """
        Route between the interactive clipboard loop and the core pipeline
        engine.
        """
        return route_text(
            text, args.pipeline, args.markdown, args.find, args.replace
        )

    first_cmd, _ = args.pipeline[0]
    normalized_cmd = first_cmd.replace('-', '_')

    if (
        normalized_cmd in REPLACEMENT_FUNC_NAMES
        and args.find is None
        and args.replace is None
    ):
        replace_text(normalized_cmd)
        program_exit()

    if is_analysis_pipeline(args.pipeline):
        run_command_loop(pipeline_runner, action_handler=None)
    else:
        def clipboard_action(func: Callable[[str], str], text: str) -> None:
            """
            Output transformed clipboard output back to the clipbaord or
            to a default file.
            """
            result = func(text)
            handle_output(
                result,
                args.output_file,
                args.debug,
                default_action=lambda r: warp_and_copy(lambda _: r, text)
            )

        run_command_loop(pipeline_runner, action_handler=clipboard_action)


def process_piped_mode(args: ParsedArgs) -> None:
    """
    Handle input when data is piped into the script.

    Args:
        args: The parsed command-line arguments.

    Raises:
        SystemExit: If there is an error processing the input.
    """
    validate_piped_commands(args.pipeline, args.find, args.replace)

    try:
        text = sys.stdin.read()
        if text.endswith('\n'):
            text = text[:-1]

        result = route_text(
            text,
            args.pipeline,
            args.markdown,
            args.find,
            args.replace
        )

        if result is not None:
            route_output(
                result, args.output_file, args.copy_to_clipboard, args.debug
            )

    except Exception as e:
        if args.debug:
            raise
        print_wrapped(
            _('Error processing input: {error}').format(error=e)
        )
        sys.exit(1)
