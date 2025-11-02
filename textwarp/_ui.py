import os
import textwrap

from ._constants import (
    ANY_OTHER_TEXT_PROMPT,
    ENTER_VALID_RESPONSE_PROMPT,
    EXIT_MESSAGE,
    NO_INPUTS,
    EXIT_INPUTS,
    YES_INPUTS
)


def get_input() -> bool:
    """
    Prompt the user on whether to process the clipboard and return a
    Boolean representing whether to continue.

    Returns:
        True: To continue processing the clipboard, otherwise ``False``.
    """
    print_wrapped(ANY_OTHER_TEXT_PROMPT)
    while True:
        response: str = input().strip().lower()
        if response in (YES_INPUTS):
            return True
        if response in (NO_INPUTS | EXIT_INPUTS):
            return False
        print_wrapped(ENTER_VALID_RESPONSE_PROMPT)


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
    terminal_size: int = os.get_terminal_size()[0]
    print_size: int = terminal_size - 1
    wrapped_text: str = textwrap.fill(text, width=print_size)
    print('\n' + wrapped_text)


def program_exit() -> None:
    """Print a message that the program is exiting, then exit the
    program."""
    print_wrapped(EXIT_MESSAGE)
    print_padding()
    exit()
