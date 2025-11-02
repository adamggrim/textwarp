from typing import Callable

import pyperclip

from ._constants import (
    CLIPBOARD_ACCESS_ERROR_MESSAGE,
    MODIFIED_TEXT_COPIED,
    UNEXPECTED_ERROR_MESSAGE
)
from ._ui import (
    get_input,
    print_wrapped,
    program_exit
)
from ._validation import (
    EmptyClipboardError,
    validate_clipboard
)


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
        print_wrapped(CLIPBOARD_ACCESS_ERROR_MESSAGE + str(e))
    except Exception as e:
        print_wrapped(UNEXPECTED_ERROR_MESSAGE + str(e))


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
