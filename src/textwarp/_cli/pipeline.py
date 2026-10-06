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

from dataclasses import replace as dc_replace
from functools import partial

from seawhirl import Spinner

if TYPE_CHECKING:
    from textwarp._cli.parsing import ParsedArgs

from textwarp._cli.args import ARGS_MAP, CommandType
from textwarp._cli.constants.messages import (
    ENTER_VALID_NUMBER_PROMPT,
    FILE_WRITE_ERROR_MSG,
    FILE_WRITE_SUCCESS_MSG,
    INTERACTIVE_CMD_ERROR_MSG,
    MODIFIED_TEXT_COPIED_MSG,
    REPLACEMENT_CMD_ERROR_MSG
)
from textwarp._cli.runners import clear_clipboard
from textwarp._cli.ui import print_wrapped, prompt_for_integer
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
    'bind_pipeline',
    'build_pipeline',
    'handle_output',
    'is_analysis_pipeline',
    'route_output',
    'route_text',
    'validate_piped_commands'
]


def _run_pipeline_segment(
    content: str | Doc,
    pipeline: Pipeline
) -> str | None:
    """Sequentially apply a list of pre-bound commands to text."""
    analysis_results: list[str] = []

    for cmd in pipeline:
        if cmd.requires_spacy:
            if isinstance(content, str):
                content = process_as_doc(content)
        elif not isinstance(content, str):
            content = content.text

        if cmd.command_type == CommandType.ANALYSIS:
            analysis_results.append(cmd.func(content))
        elif cmd.command_type == CommandType.STANDALONE:
            clear_clipboard()
            return None
        else:
            content = cmd.func(content)

    if analysis_results:
        return '\n'.join(analysis_results)

    return content if isinstance(content, str) else content.text


def apply_pipeline(
    text: str | Doc,
    pipeline: Pipeline
) -> str | None:
    """
    Apply a sequence of pre-bound pipeline functions to a string.

    Args:
        text: The string or spaCy `Doc` to transform.
        pipeline: A list of `CLICommand` objects with bound parameters.

    Returns:
        str | None: The transformed string after applying all functions
            from the pipeline, or `None` if the pipeline executes a
            standalone command.
    """
    imports_spacy = any(cmd.requires_spacy for cmd in pipeline)

    if imports_spacy:
        with Spinner():
            return _run_pipeline_segment(text, pipeline)
    return _run_pipeline_segment(text, pipeline)


def bind_pipeline(
    args: ParsedArgs,
    interactive: bool = False
) -> ParsedArgs:
    """
    Parse command parameters from CLI flags or interactive prompts and
    bind them to the pipeline's command functions.

    Args:
        args: The parsed CLI arguments.
        interactive: Whether to prompt the user for missing arguments.
            Raises `TextwarpValidationError` if `False`.

    Returns:
        ParsedArgs: Updated arguments containing the pre-bound pipeline.
    """
    if not interactive:
        validate_piped_commands(
            args.pipeline,
            args.find,
            args.replace,
            top=args.top,
            wpm=args.wpm
        )

    bound_pipeline: Pipeline = []

    for cmd in args.pipeline:
        if cmd.command_type == CommandType.REPLACEMENT:
            find_val, replace_val = args.find, args.replace
            if (find_val is None or replace_val is None) and interactive:
                assert cmd.replacement_prompt is not None
                find_val, replace_val = cmd.replacement_prompt()
                args = dc_replace(args, find=find_val, replace=replace_val)

            if find_val is not None and replace_val is not None:
                cmd = dc_replace(
                    cmd,
                    func=partial(
                        cmd.func,
                        arg_to_replace=find_val,
                        replacement_arg=replace_val
                    )
                )

        elif cmd.arg_field is not None:
            val = getattr(args, cmd.arg_field, None)
            if val is None and interactive and cmd.prompt_msg is not None:
                val = prompt_for_integer(
                    _(cmd.prompt_msg),
                    _(ENTER_VALID_NUMBER_PROMPT),
                    allow_early_exit=True
                )
                args = dc_replace(args, **{cmd.arg_field: val})

            if val is not None:
                cmd = dc_replace(
                    cmd,
                    func=partial(cmd.func, count_limit=val)
                    if cmd.arg_field == 'top'
                    else partial(cmd.func, wpm=val)
                )

        bound_pipeline.append(cmd)

    return dc_replace(args, pipeline=bound_pipeline)


def build_pipeline(
    active_cmds: list[str], parser: argparse.ArgumentParser
) -> Pipeline:
    """
    Construct the execution pipeline from CLI arguments.

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
    encoding = None if 'b' in mode else 'utf-8'

    try:
        temp_file: IO[Any] = tempfile.NamedTemporaryFile(
            dir=dir_name,
            mode=mode,
            delete=False,
            encoding=encoding
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
            temp_file = open(temp_path, mode, encoding=encoding)
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
    parse_markdown: bool
) -> str | None:
    """
    Determine whether to process text as Markdown or a plain string.

    Args:
        text: The input text to process.
        pipeline: The pipeline list of pre-bound `CLICommand` objects.
        parse_markdown: Whether to parse text as Markdown.

    Returns:
        str | None: The transformed text after processing, or `None` if
            the pipeline executed a standalone command.
    """
    if not parse_markdown:
        return apply_pipeline(text, pipeline)

    try:
        from textwarp._lib.markdown import process_markdown, strip_markdown
    except ImportError as e:
        raise MissingDependencyError(
            'marko', 'Markdown support', 'markdown'
        ) from e

    if is_analysis_pipeline(pipeline):
        stripped = strip_markdown(text)
        return apply_pipeline(stripped, pipeline)
    else:
        def transform_chunk(chunk: str) -> str:
            """
            Transform a chunk of text from the Markdown Abstract Syntax
            Tree (AST).
            """
            res = apply_pipeline(chunk, pipeline)
            return res if res is not None else chunk

        return process_markdown(text, transform_chunk)


def validate_piped_commands(
    pipeline: Pipeline,
    arg_to_replace: str | None,
    replacement_arg: str | None,
    **kwargs: Any
) -> None:
    """
    Ensure that commands requiring intermediate input are not used in
    pipeline/file mode without the necessary arguments.

    Args:
        pipeline: A list of `CLICommand` objects.
        arg_to_replace: The case, regex or target substring, if
            provided.
        replacement_arg: The replacement case, regex or substring, if
            provided.
        **kwargs: Optional command parameter values keyed by `arg_field`
            (e.g., `top`, `wpm`).

    Raises:
        TextwarpValidationError: For an intermediate input command
            used in pipeline mode without its required flag.
    """
    for cmd in pipeline:
        if cmd.arg_field is not None and kwargs.get(cmd.arg_field) is None:
            raise TextwarpValidationError(
                _(INTERACTIVE_CMD_ERROR_MSG).format(cmd_name=cmd.name)
            )

        if (
            cmd.command_type == CommandType.REPLACEMENT
            and (arg_to_replace is None or replacement_arg is None)
        ):
            raise TextwarpValidationError(_(REPLACEMENT_CMD_ERROR_MSG))
