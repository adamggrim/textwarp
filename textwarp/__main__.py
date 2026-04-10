"""
The main entry point for the package, containing the main loop and
associated functions.
"""

import gettext
import sys
from typing import Final

from textwarp._cli.parsing import parse_args
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
    'pos-count',
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
    default_action
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


def _process_file_mode(
    pipeline: Pipeline,
    input_files: list[str],
    output_file: str | None,
    arg_to_replace: str | None,
    replacement_arg: str | None
) -> None:
    """
    Handle file input and output mode.

    Args:
        pipeline: The list of command tuples to apply to the input.
        input_files: A list of paths to the input files.
        output_file: The optional path to the output file. If `None`,
            the result prints to `stdout`.
        arg_to_replace: The case, regex or substring to replace, if
            provided.
        replacement_arg: The replacement case, regex or substring, if
            provided.

    Raises:
        SystemExit: If the input file is unreadable or if there is an
            error writing to the output file.
    """
    _validate_piped_commands(pipeline, arg_to_replace, replacement_arg)

    combined_results: list[str] = []
    is_analysis = _is_analysis_pipeline(pipeline)

    for file_path in input_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
            print_wrapped(
            _(
                "Error: '{input_file}' appears to be a binary file. Please "
                'provide a valid text file.'
            ).format(file_path=file_path))
            sys.exit(1)
        except FileNotFoundError:
            print_wrapped(
                _("Error: File '{file_path}' not found.").format(
                    file_path=file_path
                ))
            sys.exit(1)

        if text.endswith('\n'):
            text = text[:-1]

        if is_analysis and len(input_files) > 1:
            print(f"\n--- {file_path} ---")

        result = _apply_pipeline(
            text,
            pipeline,
            arg_to_replace,
            replacement_arg
        )
        if result is not None:
            combined_results.append(result)

    if combined_results:
        final_output = '\n'.join(combined_results)
        _handle_output(final_output, output_file, default_action=print)


def _process_interactive_mode(
    pipeline: Pipeline,
    output_file: str | None,
    arg_to_replace: str | None,
    replacement_arg: str | None
) -> None:
    """
    Handle interactive user input.

    Args:
        pipeline: The list of command tuples to apply to the input.
        output_file: The optional path to the output file. If `None`,
            the result prints to `stdout`.
        arg_to_replace: The case, regex or substring to replace, if
            provided.
        replacement_arg: The replacement case, regex or substring, if
            provided.

    Raises:
        SystemExit: If a replacement command is in the pipeline or if
            the user exits the loop.
    """
    def pipeline_runner(text: str) -> str | None:
        """Run the pipeline on the given text."""
        return _apply_pipeline(text, pipeline, arg_to_replace, replacement_arg)

    first_cmd, _ = pipeline[0]
    normalized_cmd = first_cmd.replace('-', '_')

    if (
        normalized_cmd in _REPLACEMENT_FUNC_NAMES
        and arg_to_replace is None
        and replacement_arg is None
    ):
        replace_text(normalized_cmd)
        program_exit()

    if _is_analysis_pipeline(pipeline):
        run_command_loop(pipeline_runner, action_handler=None)
    else:
        def clipboard_action(func, text):
            result = func(text)
            _handle_output(
                result,
                output_file,
                default_action=lambda r: warp_and_copy(lambda _: r, text)
            )

        run_command_loop(pipeline_runner, action_handler=clipboard_action)


def _process_piped_mode(
    pipeline: Pipeline,
    output_file: str | None,
    arg_to_replace: str | None,
    replacement_arg: str | None
) -> None:
    """
    Handle input when data is piped into the script.

    Args:
        pipeline: The list of command tuples to apply to the input.
        output_file: The optional path to the output file. If `None`,
            the result prints to `stdout`.
        arg_to_replace: The case, regex or substring to replace, if
            provided.
        replacement_arg: The replacement case, regex or substring, if
            provided.
    """
    _validate_piped_commands(pipeline, arg_to_replace, replacement_arg)

    try:
        text = sys.stdin.read()
        if text.endswith('\n'):
            text = text[:-1]

        if _is_analysis_pipeline(pipeline):
            _apply_pipeline(text, pipeline, arg_to_replace, replacement_arg)
        else:
            result = _apply_pipeline(
                text,
                pipeline,
                arg_to_replace,
                replacement_arg
            )
            _handle_output(result, output_file, default_action=print)

    except Exception as e:
        print_wrapped(
            _('Error processing input: {error}').format(error=e),
            file=sys.stderr
        )
        sys.exit(1)


def _validate_piped_commands(pipeline: Pipeline) -> None:
    """
    Ensure that replacement commands are not used in pipeline mode.

    Args:
        pipeline: A list of tuples containing command names and their
            corresponding functions.
    Raises:
        SystemExit: If a replacement command is in the pipeline.
    """
    for cmd_name, _ in pipeline:
        normalized_name = cmd_name.replace('-', '_')
        if normalized_name in _REPLACEMENT_FUNC_NAMES:
            print_wrapped(
                _(
                    'Replacement commands require interactive user input and '
                    'cannot be used with pipelines.'
                ),
                file=sys.stderr
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
        pipeline_data = parse_args()
        if not pipeline_data:
            return None

        pipeline, lang_code, input_file, output_file = pipeline_data

        ctx.set_locale(lang_code)

        if input_file:
            _process_file_mode(pipeline, input_file, output_file)
        elif not sys.stdin.isatty():
            _process_piped_mode(pipeline, output_file)
        else:
            _process_interactive_mode(pipeline, output_file)

    except KeyboardInterrupt:
        print_padding()
        program_exit()


if __name__ == '__main__':
    main()
