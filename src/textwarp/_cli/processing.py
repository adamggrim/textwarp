"""Execution modes for pipeline processing."""

import gettext
import mmap
import os
import sys
from collections.abc import Callable, Generator, Iterator
from contextlib import contextmanager
from typing import IO, Any, Final

import regex as re

from textwarp._cli.args import CommandType
from textwarp._cli.constants.messages import (
    BINARY_FILE_ERROR_MSG,
    FILE_ACCESS_ERROR_MSG,
    FILE_SIZE_LIMIT_ERROR_MSG,
    FILE_WRITE_ERROR_MSG,
    FILE_WRITE_SUCCESS_MSG,
    PIPED_INPUT_ERROR_MSG
)
from textwarp._cli.parsing import ParsedArgs
from textwarp._cli.pipeline import (
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
from textwarp._commands.replacement import _parse_cli_escapes
from textwarp._core.exceptions import TextwarpError

_ = gettext.gettext

MAX_MEMORY_MB: Final = 100
MAX_MEMORY_BYTES: Final = MAX_MEMORY_MB * 1024 * 1024


@contextmanager
def _managed_output_stream(
    output_file: str | None,
    mode: str = 'w'
) -> Generator[IO[Any], None, None]:
    """
    Manage an output stream, yielding either a file handle or stdout.

    Args:
        output_file: The path to the output file, or `None` for stdout.
        mode: The mode for opening the file (`w` or `ab`).

    Raises:
        TextwarpError: If there is an error opening the output file.
    """
    if output_file:
        try:
            kwargs = {'encoding': 'utf-8'} if 'b' not in mode else {}
            f = open(output_file, mode, **kwargs)
        except OSError as e:
            raise TextwarpError(
                _(FILE_WRITE_ERROR_MSG).format(error=e)
            ) from e
        try:
            yield f
        finally:
            f.close()
            if 'b' not in mode:
                print_wrapped(
                    _(FILE_WRITE_SUCCESS_MSG).format(output_file=output_file)
                )
    else:
        yield sys.stdout.buffer if 'b' in mode else sys.stdout


@contextmanager
def _file_open(
    file_path: str,
    mode: str = 'r'
) -> Generator[IO[Any], None, None]:
    """
    Open a file, wrapping standard exceptions in `TextwarpError`.

    Args:
        file_path: The path to the file.
        mode: The file mode (`r` or `rb`).

    Raises:
        TextwarpError: If the file is inaccessible or in binary.
    """
    try:
        kwargs = {'encoding': 'utf-8'} if 'b' not in mode else {}
        with open(file_path, mode, **kwargs) as f:
            yield f
    except UnicodeDecodeError as e:
        raise TextwarpError(
            _(BINARY_FILE_ERROR_MSG).format(input_file=file_path)
        ) from e
    except OSError as e:
        raise TextwarpError(
            _(FILE_ACCESS_ERROR_MSG).format(file_path=file_path, error=e)
        ) from e


def _read_and_strip_file(file_path: str) -> str:
    """
    Read a text file and strip its trailing newline.

    Args:
        file_path: The path to the input file.

    Returns:
        The file contents with the trailing newline removed.

    Raises:
        TextwarpError: If the file is inaccessible or binary.
    """
    with _file_open(file_path, 'r') as f:
        return f.read().removesuffix('\n')


def _iter_mmap_replacements(
    mm: mmap.mmap,
    pattern: re.Pattern,
    replacement: bytes
) -> Iterator[bytes]:
    """
    Yield chunks of a memory-mapped file with replacements applied.

    Args:
        mm: A memory-mapped file.
        pattern: A compiled regular expression pattern.
        replacement: A byte string replacement.

    Yields:
        Chunks of the updated byte stream.
    """
    last_end = 0
    for match in pattern.finditer(mm):
        yield mm[last_end:match.start()]
        yield match.expand(replacement)
        last_end = match.end()
    yield mm[last_end:]


def _process_file_stream(args: ParsedArgs) -> None:
    """
    Process files line-by-line to avoid loading oversized files into memory.

    Args:
        args: The parsed command-line arguments.

    Raises:
        SystemExit: If there is an error reading or writing files.
    """
    with _managed_output_stream(args.output_file, 'w') as output_stream:
        for file_path in args.input_files:
            with _file_open(file_path, 'r') as f:
                for line in f:
                    result = route_text(
                        line.removesuffix('\n'),
                        args.pipeline,
                        args.markdown,
                        args.find,
                        args.replace
                    )
                    if result is not None:
                        output_stream.write(result + '\n')


def _process_mmap_regex(file_path: str, args: ParsedArgs) -> None:
    """
    Perform a regex replacement on an oversized file using memory
    mapping.

    Preserves the entire context for multi-line regular expressions.

    Args:
        file_path: The path to the input file.
        args: The parsed command-line arguments.

    Raises:
        OSError: If there is an error mapping the file or writing the
            output.
    """
    pattern = re.compile(args.find.encode('utf-8'))
    replacement = _parse_cli_escapes(args.replace).encode('utf-8')

    with _managed_output_stream(args.output_file, 'ab') as output_stream:
        with _file_open(file_path, 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                for chunk in _iter_mmap_replacements(mm, pattern, replacement):
                    output_stream.write(chunk)

                if len(args.input_files) > 1:
                    output_stream.write(b'\n')


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

    is_analysis = is_analysis_pipeline(args.pipeline)

    is_regex_only_pipeline = (
        len(args.pipeline) == 1 and args.pipeline[0].name == 'replace-regex'
    )

    can_stream = not (
        is_analysis
        or args.markdown
        or args.copy_to_clipboard
        or is_regex_only_pipeline
        or any(cmd.requires_spacy for cmd in args.pipeline)
    )

    if can_stream:
        _process_file_stream(args)
        return

    combined_results: list[str] = []

    for file_path in args.input_files:
        if os.path.getsize(file_path) > MAX_MEMORY_BYTES:
            if (
                is_regex_only_pipeline
                and args.find is not None
                and args.replace is not None
            ):
                _process_mmap_regex(file_path, args)
                continue
            else:
                warning_msg = _(FILE_ACCESS_ERROR_MSG).format(
                    file_path=file_path,
                    error=_(
                        FILE_SIZE_LIMIT_ERROR_MSG
                    ).format(limit=MAX_MEMORY_MB)
                )
                print_wrapped(f"Warning: {warning_msg}")
                continue

        text = _read_and_strip_file(file_path)

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
            final_output,
            args.output_file,
            args.copy_to_clipboard
        )


def _interactive_pipeline_runner(text: str, args: ParsedArgs) -> str | None:
    """
    Route between the interactive clipboard loop and the core pipeline
    engine.

    Args:
        text: The text to process.
        args: The parsed command-line arguments.

    Returns:
        The processed text, or None if no output is produced.
    """
    return route_text(
        text, args.pipeline, args.markdown, args.find, args.replace
    )


def _unified_action_handler(
    func: Callable[[str], str | None],
    text: str,
    args: ParsedArgs,
    is_analysis: bool
) -> None:
    """
    Route the output from interactive mode to the destination.

    Args:
        func: The pipeline runner function to execute.
        text: The input text to process.
        args: The parsed command-line arguments.
        is_analysis: Whether the current pipeline performs text
            analysis.
    """
    result = func(text)
    if result is None:
        return

    if is_analysis:
        route_output(
            result,
            args.output_file,
            args.copy_to_clipboard
        )
    else:
        handle_output(
            result,
            args.output_file,
            default_action=lambda r: warp_and_copy(lambda _: r, text)
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
    first_cmd = args.pipeline[0]

    if (
        first_cmd.command_type == CommandType.REPLACEMENT
        and args.find is None
        and args.replace is None
    ):
        replace_text(first_cmd.name.replace('-', '_'))
        program_exit()

    is_analysis = is_analysis_pipeline(args.pipeline)

    run_command_loop(
        lambda text: _interactive_pipeline_runner(text, args),
        action_handler=lambda func, text: _unified_action_handler(
            func, text, args, is_analysis
        )
    )


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
        text = sys.stdin.read().removesuffix('\n')

        result = route_text(
            text,
            args.pipeline,
            args.markdown,
            args.find,
            args.replace
        )

        if result is not None:
            route_output(
                result,
                args.output_file,
                args.copy_to_clipboard
            )

    except (OSError, UnicodeDecodeError) as e:
        raise TextwarpError(_(PIPED_INPUT_ERROR_MSG).format(error=e)) from e
