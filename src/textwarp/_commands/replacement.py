"""Runners for find-and-replace commands."""

import gettext
from collections.abc import Callable

import regex as re

from textwarp._cli.spinner import run_with_spinner
from textwarp._cli.constants.messages import (
    CASE_TO_REPLACE_NOT_FOUND_MSG,
    ENTER_CASE_TO_REPLACE_PROMPT,
    ENTER_REGEX_PROMPT,
    ENTER_REPLACEMENT_CASE_PROMPT,
    ENTER_REPLACEMENT_TEXT_PROMPT,
    ENTER_TEXT_TO_REPLACE_PROMPT,
    ENTER_VALID_CASE_PROMPT,
    ENTER_VALID_REGEX_PROMPT,
    ENTER_VALID_TEXT_PROMPT,
    REGEX_TO_REPLACE_NOT_FOUND_MSG,
    TEXT_TO_REPLACE_NOT_FOUND_MSG
)
from textwarp._cli.constants.inputs import get_exit_inputs, get_no_inputs
from textwarp._cli.dispatch import CASE_NAMES_FUNC_MAP
from textwarp._core.constants.maps import get_case_names_regex_map
from textwarp._core.exceptions import TextwarpValidationError
from textwarp._cli.ui import print_wrapped, program_exit
from textwarp._cli.validation import (
    validate_case_name,
    validate_regex,
    validate_text
)
from textwarp._lib import replacement as lib_replacement

_ = gettext.gettext

__all__ = [
    'prompt_for_replacement_case',
    'prompt_for_replacement_regex',
    'prompt_for_replacement_text',
    'replace_case',
    'replace_regex',
    'replace_text'
]

_ESCAPE_PATTERN = re.compile(r'\\[nrt\\]')
_ESCAPE_MAP = {
    r'\n': '\n',
    r'\r': '\r',
    r'\t': '\t',
    r'\\': '\\'
}


def _parse_cli_escapes(text: str) -> str:
    """
    Convert CLI escape strings into their corresponding whitespace
    characters.
    """
    def _replace_escape(match: re.Match[str]) -> str:
        return _ESCAPE_MAP[match.group(0)]

    # Match a backslash followed by "n", "r", "t" or another backslash.
    return re.sub(_ESCAPE_PATTERN, _replace_escape, text)


def _prompt_for_valid_input(
    enter_text_prompt: str,
    validation_func: Callable[[str], None],
    enter_valid_text_prompt: str,
    allow_early_exit: bool = False
) -> str:
    """
    Prompt the user for input until the input is valid.

    Args:
        enter_text_prompt: The prompt to display to the user.
        validation_func: A function that accepts a string as input and
            returns `None` if the string is valid or raises an
            exception if the string is invalid.
        enter_valid_text_prompt: The prompt to display when the input is
            invalid.
        allow_early_exit: Whether to allow the user to exit early by
            entering an exit input.
    """
    current_prompt = enter_text_prompt

    while True:
        print_wrapped(current_prompt)
        user_input = input().rstrip('\n')

        exit_commands: set[str] = set(get_exit_inputs() | get_no_inputs())
        is_exiting = user_input.strip().lower() in exit_commands

        if allow_early_exit and is_exiting:
            program_exit()

        try:
            validation_func(user_input)
            return user_input
        except TextwarpValidationError as e:
            print_wrapped(str(e))
            current_prompt = enter_valid_text_prompt


def prompt_for_replacement_case() -> tuple[str, str]:
    """
    Prompt the user for a case to replace and a replacement case.

    Returns:
        tuple[str, str]: A tuple containing:
            1. The original case name to search for.
            2. The new case name to apply as a replacement.
    """
    arg_to_replace = _prompt_for_valid_input(
        ENTER_CASE_TO_REPLACE_PROMPT,
        validate_case_name,
        ENTER_VALID_CASE_PROMPT,
        allow_early_exit=True
    ).lower()

    replacement_arg = _prompt_for_valid_input(
        ENTER_REPLACEMENT_CASE_PROMPT,
        validate_case_name,
        ENTER_VALID_CASE_PROMPT,
        allow_early_exit=True
    ).lower()

    return arg_to_replace, replacement_arg


def prompt_for_replacement_regex() -> tuple[str, str]:
    """
    Prompt the user for a regular expression to find and a string
    to replace it.

    Returns:
        tuple[str, str]: A tuple containing:
            1. The regular expression pattern to search for.
            2. The replacement text.
    """
    arg_to_replace = _prompt_for_valid_input(
        ENTER_REGEX_PROMPT,
        validate_regex,
        ENTER_VALID_REGEX_PROMPT
    )
    replacement_arg = _prompt_for_valid_input(
        ENTER_REPLACEMENT_TEXT_PROMPT,
        # Accept any text (including empty text) for replacement.
        lambda x: None,
        ENTER_VALID_TEXT_PROMPT
    )
    return arg_to_replace, replacement_arg


def prompt_for_replacement_text() -> tuple[str, str]:
    """
    Prompt the user for a string to find and a string to replace it with.

    Returns:
        tuple[str, str]: A tuple containing:
            1. The exact string to search for.
            2. The replacement string.
    """
    arg_to_replace = _prompt_for_valid_input(
        ENTER_TEXT_TO_REPLACE_PROMPT,
        validate_text,
        ENTER_VALID_TEXT_PROMPT
    )
    replacement_arg = _prompt_for_valid_input(
        ENTER_REPLACEMENT_TEXT_PROMPT,
        # Accept any text (including empty text) for replacement.
        lambda x: None,
        ENTER_VALID_TEXT_PROMPT
    )
    return arg_to_replace, replacement_arg


def replace_case(text: str, arg_to_replace: str, replacement_arg: str) -> str:
    """
    Extract arguments for a case to replace and a replacement case,
    and return the transformed text.

    Args:
        text: The string to transform.
        arg_to_replace: The case to replace.
        replacement_arg: The replacement case name.

    Returns:
        str: The transformed text.
    """
    validate_case_name(arg_to_replace)
    case_to_replace_name = arg_to_replace.lower()
    search_pattern = get_case_names_regex_map().get(case_to_replace_name)

    if search_pattern and not search_pattern.search(text):
        print_wrapped(_(CASE_TO_REPLACE_NOT_FOUND_MSG))
        return text

    validate_case_name(replacement_arg)
    replacement_case_name = replacement_arg.lower()

    search_pattern = get_case_names_regex_map()[case_to_replace_name]
    conversion_func = CASE_NAMES_FUNC_MAP[replacement_case_name]

    return run_with_spinner(
        lib_replacement.replace_case, text, search_pattern, conversion_func
    )


def replace_regex(text: str, arg_to_replace: str, replacement_arg: str) -> str:
    """
    Extract arguments for a regular expression to find and a string
    to replace it, and return the transformed text.

    Args:
        text: The string to transform.
        arg_to_replace: The regular expression to search for.
        replacement_arg: The replacement string.

    Returns:
        str: The transformed text.
    """
    validate_regex(arg_to_replace)
    if not re.search(arg_to_replace, text):
        print_wrapped(_(REGEX_TO_REPLACE_NOT_FOUND_MSG))
        return text

    parsed_replacement = _parse_cli_escapes(replacement_arg)

    return run_with_spinner(
        lib_replacement.replace_regex, text, arg_to_replace, parsed_replacement
    )


def replace_text(text: str, arg_to_replace: str, replacement_arg: str) -> str:
    """
    Extract arguments for a string to replace and a string to replace it,
    and return the transformed text.

    Args:
        text: The string to transform.
        arg_to_replace: The specific string to find and replace.
        replacement_arg: The string to replace the match with.

    Returns:
        str: The transformed text.
    """
    validate_text(arg_to_replace)
    if arg_to_replace not in text:
        print_wrapped(_(TEXT_TO_REPLACE_NOT_FOUND_MSG))
        return text

    parsed_replacement = _parse_cli_escapes(replacement_arg)

    return run_with_spinner(
        lib_replacement.replace_text, text, arg_to_replace, parsed_replacement
    )
