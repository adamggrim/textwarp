import os
import textwrap
from typing import Callable

import pyperclip

from .constants import (
    ANY_OTHER_TEXT_PROMPT,
    CLIPBOARD_ACCESS_ERROR_MESSAGE,
    ENTER_VALID_RESPONSE_PROMPT,
    EXIT_MESSAGE,
    MODIFIED_TEXT_COPIED,
    NO_INPUTS,
    EXIT_INPUTS,
    UNEXPECTED_ERROR_MESSAGE,
    YES_INPUTS
)
from .validation import EmptyClipboardError, _validate_clipboard


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


def warp_text(warping_function: Callable[[str], str]) -> None:
    """
    Apply the selected warping function within a loop and prompt the
    user for any other clipboard input.

    Args:
        warping_function (Callable[[str], str]): A function that
            takes a string as input and returns the converted string.
    """
    while True:
        _process_clipboard(warping_function)
        if not _get_input():
            break


def _get_input() -> bool:
    """
    Prompt the user whether to process the clipboard and return a
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


def _process_clipboard(warping_function: Callable[[str], str]) -> None:
    """
    Process the clipboard using a given text warping function.

    Args:
        warping_function (Callable[[str], str]): A function that
            takes a string as input and returns the converted string.
    """
    try:
        clipboard: str = pyperclip.paste()
        validate_clipboard(clipboard)
        converted_clipboard: str = warping_function(clipboard)
        pyperclip.copy(converted_clipboard)
        print_wrapped(MODIFIED_TEXT_COPIED)
    except EmptyClipboardError as e:
        print_wrapped(str(e))
    except pyperclip.PyperclipException as e:
        print_wrapped(CLIPBOARD_ACCESS_ERROR_MESSAGE + e)
    except Exception as e:
        print_wrapped(UNEXPECTED_ERROR_MESSAGE + e)
