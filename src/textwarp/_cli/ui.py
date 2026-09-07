"""Functions for handling console input and output."""

import gettext
import shutil
import sys
import time
from typing import NoReturn

from wcwidth import wcswidth

from textwarp._cli.constants.inputs import (
    get_exit_inputs,
    get_no_inputs,
    get_yes_inputs
)
from collections.abc import Callable

from textwarp._cli.constants.messages import (
    ANY_OTHER_TEXT_PROMPT,
    ENTER_CASE_TO_REPLACE_PROMPT,
    ENTER_REGEX_PROMPT,
    ENTER_REPLACEMENT_CASE_PROMPT,
    ENTER_REPLACEMENT_TEXT_PROMPT,
    ENTER_TEXT_TO_REPLACE_PROMPT,
    ENTER_VALID_CASE_PROMPT,
    ENTER_VALID_REGEX_PROMPT,
    ENTER_VALID_RESPONSE_PROMPT,
    ENTER_VALID_TEXT_PROMPT,
    EXIT_MSG
)
from textwarp._core.exceptions import TextwarpValidationError
from textwarp._cli.validation import (
    validate_case_name,
    validate_regex,
    validate_text
)

_ = gettext.gettext

__all__ = [
    'get_input',
    'print_padding',
    'print_wrapped',
    'program_exit',
    'prompt_for_integer',
    'prompt_for_replacement_case',
    'prompt_for_replacement_regex',
    'prompt_for_replacement_text'
]


def _prompt_for_valid_input(
    enter_text_prompt: str,
    validation_func: Callable[[str], None],
    enter_valid_text_prompt: str,
    allow_early_exit: bool = False
) -> str:
    """Prompt the user for input until the input is valid."""
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


def _prompt_for_valid_replacement_pair(
    target_config: tuple[str, Callable[[str], None] | None, str],
    replacement_config: tuple[str, Callable[[str], None] | None, str],
    allow_early_exit: bool = False,
    transform: Callable[[str], str] | None = None
) -> tuple[str, str]:
    """
    Prompt the user for a target string and its replacement.

    Args:
        target_config: A tuple containing the target prompt message, a
            validation function and an invalid replacement error
            message.
        replacement_config: A tuple containing the replacement prompt, a
            validation function and an error message for invalid
            replacements.
        allow_early_exit: Whether to allow early program exit using
            standard commands. Defaults to `False`.
        transform: An optional validation function to apply to both
            strings before returning.

    Returns:
        tuple[str, str]: The validated and optionally transformed target
            and replacement strings.
    """

    target = _prompt_for_valid_input(
        *target_config, allow_early_exit=allow_early_exit
    )
    replacement = _prompt_for_valid_input(
        *replacement_config, allow_early_exit=allow_early_exit
    )

    if transform:
        return transform(target), transform(replacement)

    return target, replacement


def get_input(prompt_delay: float = 0.5) -> bool:
    """
    Prompt the user on whether to process the clipboard and return a
    Boolean representing whether to continue.

    Returns:
        True: To continue processing the clipboard, otherwise `False`.
    """
    time.sleep(prompt_delay)

    print_wrapped(_(ANY_OTHER_TEXT_PROMPT))
    while True:
        response = input().strip().lower()
        if response in get_yes_inputs():
            return True
        if response in (get_no_inputs() | get_exit_inputs()):
            return False
        print_wrapped(_(ENTER_VALID_RESPONSE_PROMPT))


def print_padding() -> None:
    """Print a blank line for padding."""
    print('')


def print_wrapped(text: str) -> None:
    """
    Wrap printing based on the width of the terminal and add a newline
    character to the start of the string.

    Args:
        text: The string to print.
    """
    terminal_size = shutil.get_terminal_size(fallback=(80, 24)).columns
    print_size = terminal_size - 1

    words = text.split()
    lines: list[str] = []
    current_line: list[str] = []
    current_width = 0

    for word in words:
        word_width = max(0, wcswidth(word))

        if current_line and current_width + 1 + word_width > print_size:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width
        else:
            current_line.append(word)
            current_width += word_width + (1 if len(current_line) > 1 else 0)

    if current_line:
        lines.append(' '.join(current_line))

    wrapped_text = '\n'.join(lines)
    print('\n' + wrapped_text)


def program_exit() -> NoReturn:
    """
    Print a message that the program is exiting, then exit the program.

    Raises:
        SystemExit: Raised to terminate the application.
    """
    print_wrapped(_(EXIT_MSG))
    print_padding()
    sys.exit(0)


def prompt_for_integer(
    prompt_text: str,
    error_text: str,
    allow_early_exit: bool = False
) -> int:
    """
    Prompt the user for a valid positive integer.

    Args:
        prompt_text: The initial prompt to display.
        error_text: The error message displayed on invalid input.
        allow_early_exit: Whether to allow the user to exit early by
            entering an exit input.

    Returns:
        int: A valid integer provided by the user.
    """
    print_wrapped(prompt_text)
    user_input: str = input().strip()

    while True:
        exit_commands: set[str] = set(get_exit_inputs() | get_no_inputs())
        is_exiting = user_input.lower() in exit_commands

        if allow_early_exit and is_exiting:
            program_exit()

        if user_input.isdigit() and int(user_input) > 0:
            return int(user_input)
        else:
            print_wrapped(error_text)
            user_input = input().strip()


def prompt_for_replacement_case() -> tuple[str, str]:
    """
    Prompt for a target case and replacement case.

    Returns:
        tuple[str, str]: A tuple containing:
            1. The target case name.
            2. The replacement case name.
    """
    return _prompt_for_valid_replacement_pair(
        target_config=(
            ENTER_CASE_TO_REPLACE_PROMPT,
            validate_case_name,
            ENTER_VALID_CASE_PROMPT
        ),
        replacement_config=(
            ENTER_REPLACEMENT_CASE_PROMPT,
            validate_case_name,
            ENTER_VALID_CASE_PROMPT
        ),
        allow_early_exit=True,
        transform=str.lower
    )


def prompt_for_replacement_regex() -> tuple[str, str]:
    """
    Prompt for a target regular expression and replacement text.

    Returns:
        tuple[str, str]: A tuple containing:
            1. The target regular expression pattern.
            2. The replacement text.
    """
    return _prompt_for_valid_replacement_pair(
        target_config=(
            ENTER_REGEX_PROMPT,
            validate_regex,
            ENTER_VALID_REGEX_PROMPT
        ),
        replacement_config=(
            ENTER_REPLACEMENT_TEXT_PROMPT,
            lambda x: None,
            ENTER_VALID_TEXT_PROMPT
        )
    )


def prompt_for_replacement_text() -> tuple[str, str]:
    """
    Prompt for target text and replacement text.

    Returns:
        tuple[str, str]: A tuple containing:
            1. The target text.
            2. The replacement text.
    """
    return _prompt_for_valid_replacement_pair(
        target_config=(
            ENTER_TEXT_TO_REPLACE_PROMPT,
            validate_text,
            ENTER_VALID_TEXT_PROMPT
        ),
        replacement_config=(
            ENTER_REPLACEMENT_TEXT_PROMPT,
            # Accept any text (including empty text) for replacement.
            lambda x: None,
            ENTER_VALID_TEXT_PROMPT
        )
    )
