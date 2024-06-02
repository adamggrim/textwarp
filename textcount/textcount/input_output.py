import os
import textwrap
from typing import Callable

import pyperclip

from textcount.constants import (ANY_OTHER_TEXT_STR, ENTER_VALID_RESPONSE_STR, 
                                EXIT_STR, NO_STRS, QUIT_STRS, YES_STRS)


def print_padding() -> None:
    """Prints a blank line for padding."""
    print('')


def print_wrapped(string: str) -> None:
    """
    Wraps printing based on the width of the terminal and adds a 
        newline character to the start of the string.

    Args:
        text (str): The string to print.
    """
    terminal_size = os.get_terminal_size()[0]
    print_size = terminal_size - 1
    wrapped_str = textwrap.fill(string, width=print_size)
    print('\n' + wrapped_str)


def program_exit() -> None:
    """
    Prints a message that the program is exiting, then exits the 
        program.
    """
    print_wrapped(EXIT_STR)
    print_padding()
    exit()


def analyze_text(analysis_function: Callable[[str], str]) -> None:
    """
    Applies the selected analysis function and prompts the user for 
        other clipboard input.

    Args:
        analysis_function (Callable[[str], str]): A function that 
            takes a string as input and prints the selected analysis.
    """
    while True:
        clipboard = pyperclip.paste()
        analysis_function(clipboard)
        print_wrapped(ANY_OTHER_TEXT_STR)
        response = input().strip()
        while True:
            if response.lower() in (NO_STRS | QUIT_STRS | YES_STRS):
                break
            else:
                print_wrapped(ENTER_VALID_RESPONSE_STR)
                response = input().strip()
                continue
        if response.lower() in (NO_STRS | QUIT_STRS):
            program_exit()