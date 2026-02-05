"""
The main entry point for the package, containing the main loop and
associated functions.
"""

import sys
from collections.abc import Callable
from typing import TypeAlias

from textwarp._cli.parsing import parse_args
from textwarp._cli.runners import (
    clear_clipboard,
    replace_text,
    run_command_loop,
    warp_and_copy
)
from textwarp._cli.ui import print_padding, print_wrapped, program_exit
from textwarp._commands import replacement

PipelineItem: TypeAlias = tuple[str, Callable[[str], str]]
Pipeline: TypeAlias = list[PipelineItem]

# Commands that print analysis and exit (cannot be looped easily or piped further)
ANALYSIS_COMMANDS = {
    'char-count',
    'line-count',
    'mfws',
    'pos-count',
    'sentence-count',
    'time-to-read',
    'word-count'
}

# All function names for replacement commands.
_REPLACEMENT_FUNC_NAMES: set[str] = set(replacement.__all__)


def _apply_pipeline(text: str, pipeline: list) -> str | None:
    """
    Apply a list of pipeline functions to a given string.

    Args:
        text: The string to transform.
        pipeline: A list of tuples containing:
            - The command-line argument string (e.g., "word-count").
            - The corresponding callable function (e.g., "word_count").

    Returns:
        str | None: The string after applying all functions from the
            pipeline, or ``None`` if the pipeline executes an analysis
            command.
    """
    for cmd_name, func in pipeline:
        if cmd_name == 'clear':
            clear_clipboard()
        elif cmd_name in ANALYSIS_COMMANDS:
            func(text)
            return None # Stop the pipeline.
        else:
            text = func(text)
    return text


def _is_analysis_pipeline(pipeline: Pipeline) -> bool:
    """Check if any command in the pipeline is an analysis command."""
    return any(cmd in ANALYSIS_COMMANDS for cmd, _ in pipeline)


def _process_interactive_mode(pipeline: Pipeline) -> None:
    """Handle interactive user input mode."""
    def pipeline_runner(text: str) -> str | None:
        """Run the pipeline on the given text."""
        return _apply_pipeline(text, pipeline)

    first_cmd, _ = pipeline[0]
    normalized_cmd = first_cmd.replace('-', '_')

    if normalized_cmd in _REPLACEMENT_FUNC_NAMES:
        replace_text(normalized_cmd)
        program_exit()

    if _is_analysis_pipeline(pipeline):
        run_command_loop(pipeline_runner, action_handler=None)
    else:
        run_command_loop(pipeline_runner, action_handler=warp_and_copy)


def _process_piped_mode(pipeline: Pipeline) -> None:
    """Handle input when data is piped into the script (stdin)."""
    _validate_piped_commands(pipeline)

    try:
        text = sys.stdin.read()
        if text.endswith('\n'):
            text = text[:-1]

        if _is_analysis_pipeline(pipeline):
            _apply_pipeline(text, pipeline)
        else:
            warp_and_copy(lambda t: _apply_pipeline(t, pipeline), text)

    except Exception as e:
        print_wrapped(f'Error processing input: {e}', file=sys.stderr)
        sys.exit(1)


def _validate_piped_commands(pipeline: Pipeline) -> None:
    """Ensure replacement commands are not used in pipeline mode."""
    for cmd_name, _ in pipeline:
        normalized_name = cmd_name.replace('-', '_')
        if normalized_name in _REPLACEMENT_FUNC_NAMES:
            print_wrapped(
                'Replacement commands require interactive user input and '
                'cannot be used with pipelines.',
                file=sys.stderr
            )
            sys.exit(1)


def main() -> None:
    """Run the main loop for text transformation or analysis."""
    try:
        pipeline = parse_args()
        if not pipeline:
            return

        if sys.stdin.isatty():
            _process_interactive_mode(pipeline)
        else:
            _process_piped_mode(pipeline)

    except KeyboardInterrupt:
        print_padding()
        program_exit()


if __name__ == "__main__":
    main()
