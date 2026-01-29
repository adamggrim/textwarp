"""The main entry point for the package, containing the main loop."""

import sys

from ._cli.parsing import parse_args
from ._cli.runners import (
    clear_clipboard,
    replace_text,
    run_command_loop,
    warp_and_copy
)
from ._cli.ui import (
    print_padding,
    program_exit
)
from ._commands import analysis
from ._commands import replacement

# Commands that print analysis and exit (cannot be looped easily or piped further)
ANALYSIS_COMMANDS = {
    'char-count', 'line-count', 'mfws', 'pos-count',
    'sentence-count', 'time-to-read', 'word-count'
}

# All function names for replacement commands.
_REPLACEMENT_FUNC_NAMES: set[str] = set(replacement.__all__)


def apply_pipeline(text: str, pipeline: list) -> str | None:
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
        if cmd_name in ANALYSIS_COMMANDS:
            func(text)
            return None # Stop the pipeline.
        else:
            text = func(text)
    return text


def main() -> None:
    """Run the main loop for text transformation or analysis."""
    pipeline = parse_args()
    if not pipeline:
        return

    if not sys.stdin.isatty():
        try:
            text = sys.stdin.read()
            if text.endswith('\n'):
                text = text[:-1]

            result = apply_pipeline(text, pipeline)
            if result is not None:
                sys.stdout.write(result)
        except Exception:
            pass
        return

    try:
        first_cmd, _ = pipeline[0]

        if first_cmd == 'clear':
            clear_clipboard()
            program_exit()

        if first_cmd.replace('-', '_') in _REPLACEMENT_FUNC_NAMES:
            replace_text(first_cmd.replace('-', '_'))
            program_exit()

        def pipeline_runner(text: str) -> str | None:
            """Apply the pipeline function to the given text."""
            return apply_pipeline(text, pipeline)

        is_analysis = any(cmd in ANALYSIS_COMMANDS for cmd, _ in pipeline)

        if is_analysis:
            run_command_loop(pipeline_runner, action_handler=None)
        else:
            # Run and copy result to clipboard
            run_command_loop(pipeline_runner, action_handler=warp_and_copy)

    except KeyboardInterrupt:
        print_padding()
        program_exit()
