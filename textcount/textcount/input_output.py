from typing import Callable

import pyperclip

from textcount.constants import (ANY_OTHER_TEXT_STR, ENTER_VALID_RESPONSE_STR, 
                                 EXIT_STR, NO_STRS, QUIT_STRS, YES_STRS)
from textcount.formatting import FormatPrinting


def program_exit() -> None:
    """
    Prints a message that the program is exiting, then exits the 
        program.
    """
    FormatPrinting.print_wrapped(EXIT_STR)
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
        clipboard = pyperclip.paste()
        processing_function(clipboard)
        FormatPrinting.print_wrapped(ANY_OTHER_TEXT_STR)
        response = input().strip()
        while True:
            if response.lower() in (NO_STRS | QUIT_STRS | YES_STRS):
                break
            else:
                FormatPrinting.print_wrapped(ENTER_VALID_RESPONSE_STR)
                response = input().strip()
                continue
        if response.lower() in (NO_STRS | QUIT_STRS):
            program_exit()
