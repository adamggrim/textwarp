"""
The main entry point for the package, containing the main loop and
associated functions.
"""

import gettext
import sys
from typing import Callable, Final

from textwarp._cli.parsing import ParsedArgs, parse_args
from textwarp._cli.runners import (
    clear_clipboard,
    replace_text,
    run_command_loop,
    warp_and_copy
)
from textwarp._cli.ui import print_padding, print_wrapped, program_exit
from textwarp._commands import replacement
from textwarp._core.types import Pipeline
from textwarp._core.context import ctx

_ = gettext.gettext

# Commands that print analysis and exit.
ANALYSIS_COMMANDS: Final[frozenset[str]] = frozenset({
    'char-count',
    'line-count',
    'mfws',
    'pos-counts',
    'sentence-count',
    'time-to-read',
    'word-count'
})

# All the function names for replacement commands.
_REPLACEMENT_FUNC_NAMES: Final[frozenset[str]] = frozenset(replacement.__all__)


def _apply_pipeline(
    text: str,
    pipeline: Pipeline,
    arg_to_replace: str | None = None,
    replacement_arg: str | None = None
) -> str | None:
    """
    Apply a sequence of pipeline functions to a given string.

    Args:
        text: The string to transform.
        pipeline: A list of tuples containing:
            - The command-line argument string (e.g., `word-count`).
            - The corresponding callable function (e.g., `word_count`).
        arg_to_replace: The case, regex or substring to replace, if
            provided. Defaults to `None`.
        replacement_arg: The replacement case, regex or substring, if
            provided. Defaults to `None`.

    Returns:
        str | None: The transformed string after applying all functions
            from the pipeline, or `None` if the pipeline executes an
            analysis command.
    """
    for cmd_name, func in pipeline:
        if cmd_name == 'clear':
            clear_clipboard()
        elif cmd_name in ANALYSIS_COMMANDS:
            func(text)
            return None
        else:
            normalized_name = cmd_name.replace('-', '_')
            if (
                normalized_name in _REPLACEMENT_FUNC_NAMES
                and arg_to_replace is not None
                and replacement_arg is not None
            ):
                text = func(
                    text,
                    arg_to_replace=arg_to_replace,
                    replacement_arg=replacement_arg
                )
            else:
                text = func(text)
    return text


def _handle_output(
    result: str | None,
    output_file: str | None,
    default_action: Callable[[str], None]
) -> None:
    """
    Route the transformed text to a file.

    Args:
        result: The transformed text to output, or `None` if the
            pipeline executed an analysis command.
        output_file: The optional path to an output file, or `None` to
            print to `stdout`.
        default_action: A callable that performs the default output
            action on the result string.

    Raises:
        SystemExit: If there is an error writing to the output file.
    """
    if result is None:
        return

    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print_wrapped(
                _(
                    "Modified text successfully written to '{output_file}'."
                ).format(output_file=output_file)
            )
        except Exception as e:
            print_wrapped(
                _('Error writing to output file: {error}').format(error=e)
            )
            sys.exit(1)
    else:
        default_action(result)


def _is_analysis_pipeline(pipeline: Pipeline) -> bool:
    """Check if any command in the pipeline is an analysis command."""
    return any(cmd in ANALYSIS_COMMANDS for cmd, _ in pipeline)


def _process_file_mode(args: ParsedArgs) -> None:
    """
    Handle file input and output mode.

    Args:
        args: The parsed command-line arguments.

    Raises:
        SystemExit: If the input file is unreadable or if there is an
            error writing to the output file.
    """
    _validate_piped_commands(args.pipeline, args.find, args.replace)

    combined_results: list[str] = []
    is_analysis = _is_analysis_pipeline(args.pipeline)

    for file_path in args.input_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
            print_wrapped(
            _(
                "Error: '{input_file}' appears to be a binary file. Please "
                'provide a valid text file.'
            ).format(input_file=file_path))
            sys.exit(1)
        except FileNotFoundError:
            print_wrapped(
                _("Error: File '{file_path}' not found.").format(
                    file_path=file_path
                ))
            sys.exit(1)

        if text.endswith('\n'):
            text = text[:-1]

        result = _route_text(
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
        _route_output(final_output, args.output_file, args.copy_to_clipboard)


def _process_interactive_mode(args: ParsedArgs) -> None:
    """
    Handle interactive user input.

    Args:
        args: The parsed command-line arguments.

    Raises:
        SystemExit: If a replacement command is in the pipeline or if
            the user exits the loop.
    """
    def pipeline_runner(text: str) -> str | None:
        """Run the pipeline on the given text."""
        return _route_text(
            text, args.pipeline, args.markdown, args.find, args.replace
        )

    first_cmd, _ = args.pipeline[0]
    normalized_cmd = first_cmd.replace('-', '_')

    if (
        normalized_cmd in _REPLACEMENT_FUNC_NAMES
        and args.find is None
        and args.replace is None
    ):
        replace_text(normalized_cmd)
        program_exit()

    if _is_analysis_pipeline(args.pipeline):
        run_command_loop(pipeline_runner, action_handler=None)
    else:
        def clipboard_action(func: Callable[[str], str], text: str) -> None:
            """Handle clipboard output for non-analysis pipelines."""
            result = func(text)
            _handle_output(
                result,
                args.output_file,
                default_action=lambda r: warp_and_copy(lambda _: r, text)
            )

        run_command_loop(pipeline_runner, action_handler=clipboard_action)


def _process_piped_mode(args: ParsedArgs) -> None:
    """
    Handle input when data is piped into the script.

    Args:
        args: The parsed command-line arguments.

    Raises:
        SystemExit: If there is an error processing the input.
    """
    _validate_piped_commands(args.pipeline, args.find, args.replace)

    try:
        text = sys.stdin.read()
        if text.endswith('\n'):
            text = text[:-1]

        result = _route_text(
            text,
            args.pipeline,
            args.markdown,
            args.find,
            args.replace
        )

        if result is not None:
            _route_output(result, args.output_file, args.copy_to_clipboard)

    except Exception as e:
        print_wrapped(
            _('Error processing input: {error}').format(error=e)
        )
        sys.exit(1)


def _route_output(
    result: str,
    output_file: str | None,
    copy_to_clipboard: bool
) -> None:
    """
    Route the transformed text to a file, the clipboard or the terminal.

    Args:
        result: The transformed text to output.
        output_file: The optional path to an output file, or `None` to
            print to `stdout`.
        copy_to_clipboard: Whether to copy the output to the clipboard
            instead of printing or writing to a file.

    Raises:
        SystemExit: If there is an error processing the input.
    """
    if output_file:
        _handle_output(result, output_file, default_action=lambda x: None)

    if copy_to_clipboard:
        import pyperclip
        from textwarp._cli.constants.messages import MODIFIED_TEXT_COPIED_MSG
        pyperclip.copy(result)
        print_wrapped(_(MODIFIED_TEXT_COPIED_MSG))
    elif not output_file:
        print(result)


def _route_text(
    text: str,
    pipeline: Pipeline,
    parse_markdown: bool,
    arg_to_replace: str | None = None,
    replacement_arg: str | None = None
) -> str | None:
    """
    Determine whether to process text as Markdown or a plain string.

    Args:
        text: The input text to process.
        pipeline: The pipeline list of command tuples.
        parse_markdown: Whether to parse text as Markdown.
        arg_to_replace: The case, regex or substring to replace.
        replacement_arg: The replacement case, regex or substring.

    Returns:
        str | None: The transformed text after processing, or `None` if
            the pipeline executed an analysis command.
    """
    if not parse_markdown:
        return _apply_pipeline(
            text, pipeline, arg_to_replace, replacement_arg
        )

    try:
        from textwarp._lib.markdown import process_markdown, strip_markdown
    except ImportError:
        print_wrapped(
            "Error: Markdown support requires the 'marko' package. Install it "
            'using: pip install textwarp[markdown]'
        )
        sys.exit(1)

    if _is_analysis_pipeline(pipeline):
        clean_text = strip_markdown(text)
        return _apply_pipeline(
            clean_text, pipeline, arg_to_replace, replacement_arg
        )
    else:
        def transform_chunk(chunk: str) -> str:
            """
            Transform a chunk of text from the Markdown Abstract Syntax
            Tree (AST).
            """
            res = _apply_pipeline(
                chunk, pipeline, arg_to_replace, replacement_arg
            )
            return res if res is not None else chunk

        return process_markdown(text, transform_chunk)


def _validate_piped_commands(
    pipeline: Pipeline,
    arg_to_replace: str | None,
    replacement_arg: str | None
) -> None:
    """
    Ensure that replacement commands are not used in pipeline mode.

    Args:
        pipeline: A list of tuples containing command names and their
            corresponding functions.
        arg_to_replace: The case, regex or substring to replace, if
            provided.
        replacement_arg: The replacement case, regex or substring, if
            provided.
    Raises:
        SystemExit: If a replacement command is in the pipeline.
    """
    for cmd_name, _ in pipeline:
        normalized_name = cmd_name.replace('-', '_')
        if normalized_name in _REPLACEMENT_FUNC_NAMES:
            if arg_to_replace is None or replacement_arg is None:
                print_wrapped(
                    _(
                        'Replacement commands require --find and '
                        '--replace arguments when used in file or piped '
                        'mode.'
                    )
                )
                sys.exit(1)


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
            _process_file_mode(parsed_args)
        elif not sys.stdin.isatty():
            _process_piped_mode(parsed_args)
        else:
            _process_interactive_mode(parsed_args)

    except KeyboardInterrupt:
        print_padding()
        program_exit()


if __name__ == '__main__':
    main()
