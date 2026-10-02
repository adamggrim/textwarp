"""Pipeline output routing."""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
from collections.abc import Callable, Generator
from contextlib import contextmanager
from typing import IO, TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse

    from spacy.tokens import Doc

from textwarp._cli.args import ARGS_MAP, CommandType
from textwarp._cli.constants.messages import (
    FILE_WRITE_ERROR_MSG,
    FILE_WRITE_SUCCESS_MSG,
    INTERACTIVE_CMD_ERROR_MSG,
    MODIFIED_TEXT_COPIED_MSG,
    REPLACEMENT_CMD_ERROR_MSG
)
from textwarp._cli.runners import clear_clipboard
from textwarp._cli.spinner import run_with_spinner
from textwarp._cli.ui import print_wrapped
from textwarp._core.context import _
from textwarp._core.exceptions import (
    MissingDependencyError,
    TextwarpError,
    TextwarpValidationError
)
from textwarp._core.types import Pipeline
from textwarp._lib.nlp import process_as_doc

__all__ = [
    'apply_pipeline',
    'atomic_write',
    'build_pipeline',
    'handle_output',
    'is_analysis_pipeline',
    'requires_intermediate_input',
    'route_output',
    'route_text',
    'validate_piped_commands'
]


def _run_pipeline_segment(
    content: str | Doc,
    pipeline: Pipeline,
    arg_to_replace: str | None,
    replacement_arg: str | None,
    top: int | None = None,
    wpm: int | None = None
) -> str | None:
    """Helper to sequentially apply a list of commands to text."""
    analysis_results: list[str] = []

    for cmd in pipeline:
        if cmd.name == 'expand-contractions' and isinstance(content, str):
            content = cmd.func(content)
            continue

        if cmd.requires_spacy:
            if isinstance(content, str):
                content = process_as_doc(content)
        elif not isinstance(content, str):
            content = content.text

        if cmd.command_type == CommandType.ANALYSIS:
            if cmd.name in {'entity-counts', 'mfws'} and top is not None:
                analysis_results.append(cmd.func(content, top))
            elif cmd.name == 'time-to-read' and wpm is not None:
                analysis_results.append(cmd.func(content, wpm))
            else:
                analysis_results.append(cmd.func(content))
        elif (
            cmd.command_type == CommandType.REPLACEMENT
            and arg_to_replace is not None
            and replacement_arg is not None
        ):
            content = cmd.func(
                content,
                arg_to_replace=arg_to_replace,
                replacement_arg=replacement_arg
            )
        elif cmd.command_type == CommandType.STANDALONE:
            clear_clipboard()
            return None
        else:
            content = cmd.func(content)

    if analysis_results:
        return '\n'.join(analysis_results)

    return content if isinstance(content, str) else content.text


def _preload_spacy() -> None:
    """Helper to preload spaCy in the main process."""
    from textwarp._lib.nlp import get_nlp
    get_nlp()


def apply_pipeline(
    text: str | Doc,
    pipeline: Pipeline,
    arg_to_replace: str | None = None,
    replacement_arg: str | None = None,
    top: int | None = None,
    wpm: int | None = None
) -> str | None:
    """
    Apply a sequence of pipeline functions to a string.

    Args:
        text: The string or spaCy `Doc` to transform.
        pipeline: A list of tuples containing:
            - The command-line argument string (e.g., `word-count`).
            - The corresponding callable function (e.g., `word_count`).
        arg_to_replace: The case, regex or target substring, if
            provided. Defaults to `None`.
        replacement_arg: The replacement case, regex or substring, if
            provided. Defaults to `None`.
        top: The number of ranked items to display. Defaults to `None`.
        wpm: The words per minute. Defaults to `None`.

    Returns:
        str | None: The transformed string after applying all functions
            from the pipeline, or `None` if the pipeline executes an
            analysis command.
    """
    imports_spacy = any(cmd.requires_spacy for cmd in pipeline)
    requires_input = requires_intermediate_input(
        pipeline, arg_to_replace, replacement_arg, top=top, wpm=wpm
    )

    content = text

    if imports_spacy:
        if requires_input:
            run_with_spinner(_preload_spacy)
            return _run_pipeline_segment(
                content,
                pipeline,
                arg_to_replace,
                replacement_arg,
                top=top,
                wpm=wpm
            )
        else:
            return run_with_spinner(
                _run_pipeline_segment,
                content,
                pipeline,
                arg_to_replace,
                replacement_arg,
                top,
                wpm
            )
    else:
        return _run_pipeline_segment(
            content,
            pipeline,
            arg_to_replace,
            replacement_arg,
            top=top,
            wpm=wpm
        )


def build_pipeline(
    active_cmds: list[str], parser: argparse.ArgumentParser
) -> Pipeline:
    """
    Construct the execution pipeline from command-line arguments.

    Args:
        active_cmds: The ordered list of valid commands.
        parser: The `ArgumentParser` instance used to display error
            messages or help text.

    Returns:
        Pipeline: A list of command tuples.

    Raises:
        SystemExit: If the pipeline is empty.
    """
    pipeline: Pipeline = []

    for cmd_key in active_cmds:
        pipeline.append(ARGS_MAP[cmd_key])

    if not pipeline:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return pipeline


@contextmanager
def atomic_write(
    file_path: str,
    mode: str = 'w'
) -> Generator[IO[Any], None, None]:
    """
    Safely write to a file by staging writes to a temporary file
    and atomically swapping it upon completion.
    """
    dir_name = os.path.dirname(file_path) or '.'
    kwargs = {'encoding': 'utf-8'} if 'b' not in mode else {}

    try:
        temp_file = tempfile.NamedTemporaryFile(
            dir=dir_name,
            mode=mode,
            delete=False,
            **kwargs
        )
    except OSError as e:
        raise TextwarpError(
            _(FILE_WRITE_ERROR_MSG).format(error=e)
        ) from e

    temp_path = temp_file.name

    try:
        if 'a' in mode and os.path.exists(file_path):
            temp_file.close()
            shutil.copy2(file_path, temp_path)
            temp_file = open(temp_path, mode, **kwargs)
        yield temp_file
    except Exception as e:
        temp_file.close()
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        if isinstance(e, OSError) and not isinstance(e, TextwarpError):
            raise TextwarpError(
                _(FILE_WRITE_ERROR_MSG).format(error=e)
            ) from e
        raise
    else:
        temp_file.close()
        try:
            os.replace(temp_path, file_path)
        except OSError as e:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise TextwarpError(
                _(FILE_WRITE_ERROR_MSG).format(error=e)
            ) from e


def handle_output(
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
        TextwarpError: If there is an error writing to the output file.
    """
    if result is None:
        return

    if output_file:
        with atomic_write(output_file, 'w') as f:
            f.write(result)
        print_wrapped(
            _(FILE_WRITE_SUCCESS_MSG).format(output_file=output_file)
        )
    else:
        default_action(result)


def is_analysis_pipeline(pipeline: Pipeline) -> bool:
    """Check if any command in the pipeline is an analysis command."""
    return any(cmd.command_type == CommandType.ANALYSIS for cmd in pipeline)


def requires_intermediate_input(
    pipeline: Pipeline,
    arg_to_replace: str | None,
    replacement_arg: str | None,
    top: int | None = None,
    wpm: int | None = None
) -> bool:
    """
    Check whether the pipeline contains commands that prompt for input
    after the initial argument.
    """
    for cmd in pipeline:
        if cmd.requires_intermediate_input:
            if cmd.name in {'entity-counts', 'mfws'} and top is not None:
                continue
            if cmd.name == 'time-to-read' and wpm is not None:
                continue
            return True
        if (
            cmd.command_type == CommandType.REPLACEMENT
            and (arg_to_replace is None or replacement_arg is None)
        ):
            return True

    return False


def route_output(
    result: str,
    output_file: str | None,
    copy_to_clipboard: bool,
) -> None:
    """
    Route the transformed text to a file, the clipboard or the terminal.

    Args:
        result: The transformed text to output.
        output_file: The optional path to an output file, or `None` to
            print to `stdout`.
        copy_to_clipboard: Whether to copy the output to the clipboard
            instead of printing or writing to a file.
    """
    if output_file:
        handle_output(
            result, output_file, default_action=lambda x: None
        )

    if copy_to_clipboard:
        try:
            import pyperclip
        except ImportError as e:
            raise MissingDependencyError(
                'pyperclip',
                'Clipboard support',
                'clipboard'
            ) from e

        pyperclip.copy(result)
        print_wrapped(_(MODIFIED_TEXT_COPIED_MSG))
    elif not output_file:
        print('\n' + result)


def route_text(
    text: str,
    pipeline: Pipeline,
    parse_markdown: bool,
    arg_to_replace: str | None = None,
    replacement_arg: str | None = None,
    top: int | None = None,
    wpm: int | None = None
) -> str | None:
    """
    Determine whether to process text as Markdown or a plain string.

    Args:
        text: The input text to process.
        pipeline: The pipeline list of command tuples.
        parse_markdown: Whether to parse text as Markdown.
        arg_to_replace: The case, regex or target substring.
        replacement_arg: The replacement case, regex or substring.
        top: The number of ranked items to display. Defaults to `None`.
        wpm: The words per minute. Defaults to `None`.

    Returns:
        str | None: The transformed text after processing, or `None` if
            the pipeline executed an analysis command.
    """
    if not parse_markdown:
        return apply_pipeline(
            text,
            pipeline,
            arg_to_replace,
            replacement_arg,
            top=top,
            wpm=wpm
        )

    try:
        from textwarp._lib.markdown import process_markdown, strip_markdown
    except ImportError as e:
        raise MissingDependencyError(
            'marko', 'Markdown support', 'markdown'
        ) from e

    if is_analysis_pipeline(pipeline):
        stripped = strip_markdown(text)
        return apply_pipeline(
            stripped,
            pipeline,
            arg_to_replace,
            replacement_arg,
            top=top,
            wpm=wpm
        )
    else:
        def transform_chunk(chunk: str) -> str:
            """
            Transform a chunk of text from the Markdown Abstract Syntax
            Tree (AST).
            """
            res = apply_pipeline(
                chunk,
                pipeline,
                arg_to_replace,
                replacement_arg,
                top=top,
                wpm=wpm
            )
            return res if res is not None else chunk

        return process_markdown(text, transform_chunk)


def validate_piped_commands(
    pipeline: Pipeline,
    arg_to_replace: str | None,
    replacement_arg: str | None,
    top: int | None = None,
    wpm: int | None = None
) -> None:
    """
    Ensure that commands requiring intermediate input are not used in
    pipeline/file mode without the necessary arguments.

    Args:
        pipeline: A list of tuples containing command names and their
            corresponding functions.
        arg_to_replace: The case, regex or target substring, if
            provided.
        replacement_arg: The replacement case, regex or substring, if
            provided.

    Raises:
            TextwarpValidationError: For an intermediate input command
                used in pipeline mode.
    """
    for cmd in pipeline:
        if cmd.requires_intermediate_input:
            if cmd.name in {'entity-counts', 'mfws'} and top is not None:
                continue
            if cmd.name == 'time-to-read' and wpm is not None:
                continue
            raise TextwarpValidationError(
                _(INTERACTIVE_CMD_ERROR_MSG).format(cmd_name=cmd.name)
            )

        if (
            cmd.command_type == CommandType.REPLACEMENT
            and (arg_to_replace is None or replacement_arg is None)
        ):
            raise TextwarpValidationError(_(REPLACEMENT_CMD_ERROR_MSG))
