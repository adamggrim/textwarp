from typing import Callable

import pyperclip

from textcount.constants import (
    ANY_OTHER_TEXT_PROMPT,
    ENTER_VALID_RESPONSE_PROMPT,
    EXIT_MESSAGE,
    NO_INPUTS,
    EXIT_INPUTS,
    YES_INPUTS
)
from textcount.formatting import FormatPrinting


def program_exit() -> None:
    """
    Prints a message that the program is exiting, then exits the
        program.
    """
    FormatPrinting.print_wrapped(EXIT_MESSAGE)
    FormatPrinting.print_padding()
    exit()


def process_analysis(processing_function: Callable[[str], str]) -> None:
    """
    Prints the text analysis and prompts the user for any other
        clipboard input.

    Args:
        processing_function (Callable[[str], str]): A function that
            takes a string as input and deploys functions to print
            the selected analysis.
    """
    while True:
        clipboard: str = pyperclip.paste()
        processing_function(clipboard)
        FormatPrinting.print_wrapped(ANY_OTHER_TEXT_PROMPT)
        response: str = input().strip()
        while True:
            if response.lower() in (NO_INPUTS | EXIT_INPUTS | YES_INPUTS):
                break
            else:
                FormatPrinting.print_wrapped(ENTER_VALID_RESPONSE_PROMPT)
                response = input().strip()
                continue
        if response.lower() in (NO_INPUTS | EXIT_INPUTS):
            program_exit()
