from typing import Callable

import pyperclip

import textwarp._analysis_commands as analysis_mod
import textwarp.warping as warping_mod

from ._constants import (
    CLIPBOARD_ACCESS_ERROR_MESSAGE,
    MODIFIED_TEXT_COPIED,
    UNEXPECTED_ERROR_MESSAGE
)
from ._ui import (
    get_input,
    print_wrapped
)
from ._validation import (
    EmptyClipboardError,
    validate_clipboard
)


def _process_clipboard(warping_function: Callable[[str], str]) -> None:
    """
    Process the clipboard for use in a text warping or analysis
    function.

    Returns:
        clipboard (str): The validated clipboard text, or ``None`` if an error
            occurred.
    """
    try:
        clipboard: str = pyperclip.paste()
        validate_clipboard(clipboard)
        return clipboard
    except EmptyClipboardError as e:
        print_wrapped(str(e))
        return None
    except pyperclip.PyperclipException as e:
        print_wrapped(CLIPBOARD_ACCESS_ERROR_MESSAGE + str(e))
        return None
    except Exception as e:
        print_wrapped(UNEXPECTED_ERROR_MESSAGE + str(e))
        return None


def analyze_text(analysis_function: Callable[[str], str]) -> None:
    """
    Prints the text analysis and prompts the user for any other
    clipboard input.

    Args:
        analysis_function (Callable[[str], str]): A function that takes
            a string as input and prints the selected analysis.
    """
    while True:
        clipboard: str = pyperclip.paste()
        analysis_function(clipboard)

        if not get_input():
            program_exit()


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
        if not get_input():
            break
