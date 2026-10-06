"""Execution modes for pipeline processing."""

import codecs
import mmap
import os
import sys
from collections.abc import Callable, Generator, Iterator
from contextlib import contextmanager
from typing import IO, Any

import regex as re

from textwarp._cli.args import CommandType
from textwarp._cli.constants.messages import (
    BINARY_FILE_ERROR_MSG,
    FILE_ACCESS_ERROR_MSG,
    FILE_SIZE_LIMIT_ERROR_MSG,
    FILE_WRITE_SUCCESS_MSG,
    PIPED_INPUT_ERROR_MSG
)
from textwarp._cli.parsing import BYTES_PER_MB, ParsedArgs
from textwarp._cli.pipeline import (
    atomic_write,
    bind_pipeline,
    handle_output,
    is_analysis_pipeline,
    route_output,
    route_text
)
from textwarp._cli.runners import (
    NOT_FOUND_MSG_MAP,
    replace_and_copy,
    run_command_loop,
    warp_and_copy
)
from textwarp._cli.ui import print_wrapped
from textwarp._cli.validation import validate_regex
from textwarp._commands.replacement import parse_cli_escapes
from textwarp._core.context import _
from textwarp._core.exceptions import TextwarpError

__all__ = [
    'process_file_mode',
    'process_interactive_mode',
    'process_piped_mode'
]


@contextmanager
def _open_output_stream(
    output_file: str | None,
    mode: str = 'w'
) -> Generator[IO[Any], None, None]:
    """
    Open an output stream, yielding either a file handle or stdout.
    """
    if output_file:
        with atomic_write(output_file, mode) as f:
            yield f

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
        encoding = None if 'b' in mode else 'utf-8'
        with open(file_path, mode, encoding=encoding) as f:
            yield f
    except UnicodeDecodeError as e:
        raise TextwarpError(
            _(BINARY_FILE_ERROR_MSG).format(input_file=file_path)
        ) from e
    except OSError as e:
        raise TextwarpError(
            _(FILE_ACCESS_ERROR_MSG).format(file_path=file_path, error=e)
        ) from e


def _strip_line_ending(text: str) -> str:
    """Strip a single line ending."""
    return text.removesuffix('\n').removesuffix('\r')


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
        content: str = f.read()
        return _strip_line_ending(content)


def _iter_mmap_replacements(
    mm: mmap.mmap,
    pattern: re.Pattern[str],
    replacement: str
) -> Iterator[bytes]:
    """
    Yield UTF-8 encoded chunks of a memory-mapped file with Unicode
    regex replacements applied safely across multi-byte boundaries.

    Args:
        mm: A memory-mapped file.
        pattern: A compiled regular expression pattern.
        replacement: A string replacement.

    Yields:
        Chunks of the updated UTF-8 byte stream.
    """
    decoder = codecs.getincrementaldecoder('utf-8')(errors='strict')
    mm_len = len(mm)
    buffer = ''

    for offset in range(0, mm_len, BYTES_PER_MB):
        raw_chunk = mm[offset : min(offset + BYTES_PER_MB, mm_len)]
        is_eof = (offset + BYTES_PER_MB >= mm_len)
        buffer += decoder.decode(raw_chunk, final=is_eof)

        if not is_eof:
            split_idx = buffer.rfind('\n')
            if split_idx == -1 and len(buffer) >= BYTES_PER_MB * 4:
                split_idx = max(buffer.rfind(' '), buffer.rfind('\t'))
                if split_idx == -1:
                    split_idx = len(buffer) - 1024

            if split_idx == -1:
                continue

            processable, buffer = (
                buffer[: split_idx + 1],
                buffer[split_idx + 1 :]
            )
        else:
            processable, buffer = buffer, ''

        if processable:
            yield pattern.sub(replacement, processable).encode('utf-8')


def _write_mmap_regex_to_stream(
    file_path: str,
    args: ParsedArgs,
    output_stream: IO[bytes]
) -> None:
    """
    Write memory-mapped regex replacements for a single file to a
    stream.

    Args:
        file_path: The path to the input file.
        args: The parsed CLI arguments.
        output_stream: An open binary stream to write to.
    """
    assert args.find is not None
    assert args.replace is not None

    validate_regex(args.find)

    if os.path.getsize(file_path) == 0:
        if len(args.input_files) > 1:
            output_stream.write(b'\n')
        return

    pattern = re.compile(args.find)
    replacement = parse_cli_escapes(args.replace)

    with (
        _file_open(file_path, 'rb') as f,
        mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm
    ):
        try:
            for chunk in _iter_mmap_replacements(mm, pattern, replacement):
                output_stream.write(chunk)
        except UnicodeDecodeError as e:
            raise TextwarpError(
                _(BINARY_FILE_ERROR_MSG).format(input_file=file_path)
            ) from e

        if len(args.input_files) > 1:
            output_stream.write(b'\n')


def _process_mmap_regex(
    file_path: str,
    args: ParsedArgs,
    output_stream: IO[bytes] | None = None
) -> None:
    """
    Perform a regex replacement on an oversized file using memory
    mapping.

    Preserves the entire context for multi-line regular expressions.

    Args:
        file_path: The path to the input file.
        args: The parsed CLI arguments.
        output_stream: An optional open binary stream to write to.

    Raises:
        OSError: If there is an error mapping the file or writing the
            output.
    """
    if output_stream is not None:
        _write_mmap_regex_to_stream(file_path, args, output_stream)
        return

    with _open_output_stream(args.output_file, 'wb') as stream:
        _write_mmap_regex_to_stream(file_path, args, stream)


def _process_file_stream(args: ParsedArgs) -> None:
    """
    Process files line-by-line to avoid loading oversized files into
    memory.

    Args:
        args: The parsed CLI arguments.

    Raises:
        SystemExit: If there is an error reading or writing files.
    """
    with _open_output_stream(args.output_file, 'w') as output_stream:
        for file_path in args.input_files:
            with _file_open(file_path, 'r') as f:
                for line in f:
                    result = route_text(
                        _strip_line_ending(line),
                        args.pipeline,
                        args.markdown
                    )
                    if result is not None:
                        output_stream.write(result + '\n')


def _process_mixed_mmap_files(
    args: ParsedArgs,
    max_memory_bytes: int
) -> None:
    """
    Process regex replacements across oversized and standard files.
    """
    with _open_output_stream(args.output_file, 'wb') as output_stream:
        for file_path in args.input_files:
            if (
                os.path.exists(file_path)
                and os.path.getsize(file_path) > max_memory_bytes
            ):
                _process_mmap_regex(file_path, args, output_stream)
            else:
                text = _read_and_strip_file(file_path)
                result = route_text(
                    text,
                    args.pipeline,
                    args.markdown
                )
                if result is not None:
                    output_stream.write(result.encode('utf-8'))
                    if len(args.input_files) > 1:
                        output_stream.write(b'\n')


def _process_in_memory_files(
    args: ParsedArgs,
    max_memory_bytes: int,
    is_analysis: bool
) -> None:
    """Process files in memory and route the combined output."""
    combined_results: list[str] = []

    for file_path in args.input_files:
        if (
            os.path.exists(file_path)
            and os.path.getsize(file_path) > max_memory_bytes
        ):
            warning_msg = _(FILE_ACCESS_ERROR_MSG).format(
                file_path=file_path,
                error=_(
                    FILE_SIZE_LIMIT_ERROR_MSG
                ).format(limit=args.max_file_mb)
            )
            print_wrapped(f'Warning: {warning_msg}')
            continue

        text = _read_and_strip_file(file_path)
        result = route_text(
            text,
            args.pipeline,
            args.markdown
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


def process_file_mode(args: ParsedArgs) -> None:
    """
    Handle file input and output mode.

    Args:
        args: The parsed CLI arguments.

    Raises:
        SystemExit: If the input file is unreadable or if there is an
            error writing to the output file.
    """
    args = bind_pipeline(args, interactive=False)

    is_analysis = is_analysis_pipeline(args.pipeline)
    is_regex_only_pipeline = (
        len(args.pipeline) == 1 and args.pipeline[0].name == 'replace-regex'
    )
    max_memory_bytes = args.max_file_mb * BYTES_PER_MB
    has_oversized_file = any(
        os.path.exists(fp) and os.path.getsize(fp) > max_memory_bytes
        for fp in args.input_files
    )

    can_stream = has_oversized_file and not (
        is_analysis
        or args.markdown
        or args.copy_to_clipboard
        or is_regex_only_pipeline
        or any(cmd.requires_spacy for cmd in args.pipeline)
    )
    if can_stream:
        _process_file_stream(args)
        return

    can_mmap_regex = (
        has_oversized_file
        and is_regex_only_pipeline
        and args.find is not None
        and args.replace is not None
        and not args.markdown
        and not args.copy_to_clipboard
    )
    if can_mmap_regex:
        _process_mixed_mmap_files(args, max_memory_bytes)
        return

    _process_in_memory_files(args, max_memory_bytes, is_analysis)


def _interactive_pipeline_runner(text: str, args: ParsedArgs) -> str | None:
    """
    Route between the interactive clipboard loop and the core pipeline
    engine.

    Args:
        text: The text to process.
        args: The parsed CLI arguments.

    Returns:
        The processed text, or None if no output is produced.
    """
    return route_text(
        text,
        args.pipeline,
        args.markdown
    )


def _unified_action_handler(
    func: Callable[[str], str | None],
    text: str,
    args: ParsedArgs,
    is_analysis: bool,
    not_found_msg: str | None = None
) -> None:
    """
    Route the output from interactive mode to the destination.

    Args:
        func: The pipeline runner function to execute.
        text: The input text to process.
        args: The parsed CLI arguments.
        is_analysis: Whether the current pipeline performs text
            analysis.
        not_found_msg: Optional message to display when a replacement
            target is not found.
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
    elif not_found_msg is not None:
        handle_output(
            result,
            args.output_file,
            default_action=lambda r: replace_and_copy(
                lambda _: r, text, not_found_msg
            )
        )
    else:
        handle_output(
            result,
            args.output_file,
            default_action=lambda r: warp_and_copy(lambda _: r, text)
        )


def process_interactive_mode(args: ParsedArgs) -> None:
    """
    Handle the interactive CLI for user input without files or piping.

    This mode acts as a wrapper around the package's core pipeline engine.

    Args:
        args: The parsed CLI arguments.
    """
    args = bind_pipeline(args, interactive=True)

    replacement_cmd = next(
        (
            cmd for cmd in args.pipeline
            if cmd.command_type == CommandType.REPLACEMENT
        ),
        None
    )
    not_found_msg = (
        NOT_FOUND_MSG_MAP.get(replacement_cmd.name)
        if replacement_cmd is not None
        else None
    )
    is_analysis = is_analysis_pipeline(args.pipeline)

    run_command_loop(
        lambda text: _interactive_pipeline_runner(text, args),
        action_handler=lambda func, text: _unified_action_handler(
            func, text, args, is_analysis, not_found_msg
        )
    )


def process_piped_mode(args: ParsedArgs) -> None:
    """
    Handle input when data is piped into the script.

    Args:
        args: The parsed CLI arguments.

    Raises:
        SystemExit: If there is an error processing the input.
    """
    args = bind_pipeline(args, interactive=False)

    try:
        text = _strip_line_ending(sys.stdin.read())

        result = route_text(
            text,
            args.pipeline,
            args.markdown
        )

        if result is not None:
            route_output(
                result,
                args.output_file,
                args.copy_to_clipboard
            )

    except (OSError, UnicodeDecodeError) as e:
        raise TextwarpError(_(PIPED_INPUT_ERROR_MSG).format(error=e)) from e