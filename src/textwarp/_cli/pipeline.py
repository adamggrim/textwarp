"""Pipeline output routing."""

from __future__ import annotations

import gettext
import sys
from typing import Callable, Final, TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Doc

from textwarp._cli.args import (
    ANALYSIS_COMMANDS,
    ARGS_MAP,
    SPACY_COMMANDS
)
from textwarp._cli.runners import clear_clipboard
from textwarp._cli.ui import print_wrapped
from textwarp._commands import replacement
from textwarp._core.types import Pipeline

_ = gettext.gettext

REPLACEMENT_FUNC_NAMES: Final[frozenset[str]] = frozenset(replacement.__all__)

INTEGER_PROMPT_FUNC_NAMES: Final[frozenset[str]] = frozenset({
    'mfws', 'time_to_read'
})


def apply_pipeline(
    text: str | Doc,
    pipeline: Pipeline,
    arg_to_replace: str | None = None,
    replacement_arg: str | None = None
) -> str | None:
    """
    Apply a sequence of pipeline functions to a string.

    Args:
        text: The string or spaCy Doc to transform.
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
    imports_spacy = any(cmd in SPACY_COMMANDS for cmd, _ in pipeline)

    if imports_spacy:
        from textwarp._cli.spinner import AcceleratingSpinner
        from textwarp._lib.nlp import _get_nlp
        active_context = AcceleratingSpinner()
    else:
        import contextlib
        active_context = contextlib.nullcontext()

    requires_input = requires_intermediate_input(
        pipeline, arg_to_replace, replacement_arg
    )

    with active_context:
        if imports_spacy:
            _get_nlp()
            if requires_input:
                active_context.stop()

        content = text

        for cmd_name, func in pipeline:
            if cmd_name == 'clear':
                if imports_spacy:
                    active_context.stop()
                clear_clipboard()
            elif cmd_name in ANALYSIS_COMMANDS:
                if imports_spacy:
                    active_context.stop()
                func(content)
                return None
            else:
                func_name = cmd_name.replace('-', '_')
                if (
                    func_name in REPLACEMENT_FUNC_NAMES
                    and arg_to_replace is not None
                    and replacement_arg is not None
                ):
                    content = func(
                        content,
                        arg_to_replace=arg_to_replace,
                        replacement_arg=replacement_arg
                    )
                else:
                    content = func(content)

        return content if isinstance(content, str) else content.text


def build_pipeline(argv: list[str], parser: argparse.ArgumentParser) -> Pipeline:
    """
    Construct the execution pipeline from command-line arguments.

    Args:
        argv: The list of command-line arguments.
        parser: The `ArgumentParser` instance used to display error
            messages or help text.

    Returns:
        Pipeline: A list of command tuples.

    Raises:
        SystemExit: If the pipeline is empty.
    """
    pipeline: Pipeline = []

    for arg in argv[1:]:
        if not arg.startswith('-'):
            continue

        cmd_key = arg.lstrip('-')

        if cmd_key in ARGS_MAP:
            func = ARGS_MAP[cmd_key][0]
            pipeline.append((cmd_key, func))

    if not pipeline:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return pipeline


def handle_output(
    result: str | None,
    output_file: str | None,
    debug: bool,
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
            if debug:
                raise
            print_wrapped(
                _('Error writing to output file: {error}').format(error=e)
            )
            sys.exit(1)
    else:
        default_action(result)


def is_analysis_pipeline(pipeline: Pipeline) -> bool:
    """Check if any command in the pipeline is an analysis command."""
    return any(cmd in ANALYSIS_COMMANDS for cmd, _ in pipeline)


def requires_intermediate_input(
    pipeline: Pipeline,
    arg_to_replace: str | None,
    replacement_arg: str | None
) -> bool:
    """
    Check whether the pipeline contains commands that prompt for input
    after the initial argument.
    """
    for cmd_name, _ in pipeline:
        normalized_name = cmd_name.replace('-', '_')

        if normalized_name in INTEGER_PROMPT_FUNC_NAMES:
            return True
        if (
            normalized_name in REPLACEMENT_FUNC_NAMES
            and (arg_to_replace is None or replacement_arg is None)
        ):
            return True

    return False


def route_output(
    result: str,
    output_file: str | None,
    copy_to_clipboard: bool,
    debug: bool
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
        handle_output(
            result, output_file, debug, default_action=lambda x: None
        )

    if copy_to_clipboard:
        import pyperclip
        from textwarp._cli.constants.messages import MODIFIED_TEXT_COPIED_MSG
        pyperclip.copy(result)
        print_wrapped(_(MODIFIED_TEXT_COPIED_MSG))
    elif not output_file:
        print(result)


def route_text(
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
        return apply_pipeline(
            text, pipeline, arg_to_replace, replacement_arg
        )

    try:
        from textwarp._lib.markdown import process_markdown, strip_markdown
    except ImportError:
        print_wrapped(
            _(
                "Error: Markdown support requires 'marko'. Install it "
                'using: pip install textwarp[markdown]'
            )
        )
        sys.exit(1)

    if is_analysis_pipeline(pipeline):
        clean_text = strip_markdown(text)
        return apply_pipeline(
            clean_text, pipeline, arg_to_replace, replacement_arg
        )
    else:
        def transform_chunk(chunk: str) -> str:
            """
            Transform a chunk of text from the Markdown Abstract Syntax
            Tree (AST).
            """
            res = apply_pipeline(
                chunk, pipeline, arg_to_replace, replacement_arg
            )
            return res if res is not None else chunk

        return process_markdown(text, transform_chunk)


def validate_piped_commands(
    pipeline: Pipeline,
    arg_to_replace: str | None,
    replacement_arg: str | None
) -> None:
    """
    Ensure that commands requiring intermediate input are not used in
    pipeline/file mode without the necessary arguments.

    Args:
        pipeline: A list of tuples containing command names and their
            corresponding functions.
        arg_to_replace: The case, regex or substring to replace, if
            provided.
        replacement_arg: The replacement case, regex or substring, if
            provided.
    Raises:
        SystemExit: If an intermediate input command is used in pipeline mode.
    """
    for cmd_name, func in pipeline:
        func_name = cmd_name.replace('-', '_')

        if func_name in INTEGER_PROMPT_FUNC_NAMES:
            print_wrapped(
                _(
                    "The '--{cmd_name}' command requires interactive input "
                    "and cannot be used in file or piped mode."
                ).format(cmd_name=cmd_name)
            )
            sys.exit(1)

        if func_name in REPLACEMENT_FUNC_NAMES:
            if arg_to_replace is None or replacement_arg is None:
                print_wrapped(
                    _(
                        'Replacement commands require --find and '
                        '--replace arguments when used in file or piped '
                        'mode.'
                    )
                )
                sys.exit(1)
