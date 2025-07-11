import os
import textwrap
from typing import Callable

import pyperclip

from textwarp.constants import (
    ANY_OTHER_TEXT_PROMPT,
    ENTER_VALID_RESPONSE_PROMPT,
    EXIT_MESSAGE,
    MODIFIED_TEXT_COPIED,
    NO_INPUTS,
    EXIT_INPUTS,
    YES_INPUTS
)


def print_padding() -> None:
    """Prints a blank line for padding."""
    print('')


def print_wrapped(text: str) -> None:
    """
    Wraps printing based on the width of the terminal and adds a
    newline character to the start of the string.

    Args:
        text: The string to print.
    """
    terminal_size: int = os.get_terminal_size()[0]
    print_size: int = terminal_size - 1
    wrapped_text: str = textwrap.fill(text, width=print_size)
    print('\n' + wrapped_text)


def program_exit() -> None:
    """
    Prints a message that the program is exiting, then exits the
    program.
    """
    print_wrapped(EXIT_MESSAGE)
    print_padding()
    exit()


def convert_text(conversion_function: Callable[[str], str]) -> None:
    """
    Applies the selected conversion function and prompts the user for
    any other clipboard input.

    Args:
        conversion_function (Callable[[str], str]): A function that
            takes a string as input and returns the transformed string.
    """
    while True:
        clipboard: str = pyperclip.paste()
        converted_clipboard: str = conversion_function(clipboard)
        pyperclip.copy(converted_clipboard)
        print_wrapped(MODIFED_TEXT_MESSAGE)
        print_wrapped(ANY_OTHER_TEXT_PROMPT)
        response: str = input().strip()
        while True:
            if response.lower() in (NO_INPUTS | EXIT_INPUTS | YES_INPUTS):
                break
            else:
                print_wrapped(ENTER_VALID_RESPONSE_PROMPT)
                response = input().strip()
                continue
        if response.lower() in (NO_INPUTS | EXIT_INPUTS):
            program_exit()
