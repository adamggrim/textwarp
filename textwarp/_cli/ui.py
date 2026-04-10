"""Functions for handling console input and output."""

import gettext
import shutil
import sys
import textwrap
from typing import NoReturn

from textwarp._cli.constants.inputs import (
    get_exit_inputs,
    get_no_inputs,
    get_yes_inputs
)
from textwarp._cli.constants.messages import (
    ANY_OTHER_TEXT_PROMPT,
    ENTER_VALID_RESPONSE_PROMPT,
    EXIT_MSG
)

_ = gettext.gettext

__all__ = [
    'get_input',
    'print_padding',
    'print_wrapped',
    'program_exit',
    'prompt_for_integer'
]


def get_input() -> bool:
    """
    Prompt the user on whether to process the clipboard and return a
    Boolean representing whether to continue.

    Returns:
        True: To continue processing the clipboard, otherwise `False`.
    """
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
    wrapped_text = textwrap.fill(text, width=print_size)
    print('\n' + wrapped_text)


def program_exit() -> NoReturn:
    """
    Print a message that the program is exiting, then exit the program.
    """
    print_wrapped(_(EXIT_MSG))
    print_padding()
    exit()


def prompt_for_integer(prompt_text: str, error_text: str) -> int:
    """
    Prompt the user for a valid positive integer.

    Args:
        prompt_text: The initial prompt to display.
        error_text: The error message displayed on invalid input.

    Returns:
        int: A valid integer provided by the user.
    """
    print_wrapped(prompt_text)
    user_input: str = input().strip()

    while True:
        if user_input.isdigit() and int(user_input) > 0:
            return int(user_input)
        else:
            print_wrapped(error_text)
            user_input = input().strip()
