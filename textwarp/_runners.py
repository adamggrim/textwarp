from types import ModuleType
from typing import Callable

import pyperclip

from ._commands import _analysis as analysis_mod
from ._commands import _replacement as replacement_mod
from ._constants import (
    CLIPBOARD_ACCESS_ERROR_MESSAGE,
    CLIPBOARD_CLEARED_MESSAGE,
    MODIFIED_TEXT_COPIED_MESSAGE,
    REPLACEMENT_NOT_FOUND_MESSAGE
)
from . import warping as warping_mod
from ._ui import (
    get_input,
    print_wrapped
)
from ._validation import (
    EmptyClipboardError,
    validate_clipboard
)


def _paste_and_validate() -> str | None:
    """
    Paste and validate clipboard text.

    Returns:
        clipboard: The validated clipboard text, or ``None`` if an error
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
        print_wrapped(str(e))
        return None


def _replace_and_copy(
    command: Callable[[str], str],
    clipboard: str
) -> None:
    """
    Transform text using a replacement command and copy the result.
    Print if the replacement was not found.

    Args:
        command: The replacement function.
        clipboard: The clipboard text to transform.
    """
    transformation: str = command(clipboard)

    if transformation == clipboard:
        print_wrapped(REPLACEMENT_NOT_FOUND_MESSAGE)
    else:
        pyperclip.copy(transformation)
        print_wrapped(MODIFIED_TEXT_COPIED_MESSAGE)


def _warp_and_copy(
    command: Callable[[str], str],
    clipboard: str
) -> None:
    """
    Transform text using a given command and copy the result back to the
    clipboard.

    Args:
        command: The transformation function.
        clipboard: The clipboard text to transform.
    """
    transformation: str = command(clipboard)
    pyperclip.copy(transformation)
    print_wrapped(MODIFIED_TEXT_COPIED_MESSAGE)


def _run_command_loop(
    command_name: str,
    module: ModuleType,
    action_handler: Callable[[Callable[[str], str], str], None] | None = None
) -> None:
    """
    Run a module command to transform or analyze clipboard text.

    Args:
        command_name: The command name.
        module: The module containing the command.
        action_handler: A function defining what to do with the
            command and clipboard text.
    """
    command: Callable[[str], str] = getattr(module, command_name)

    while True:
        clipboard: str | None = _paste_and_validate()

        if clipboard is None:
            if not get_input():
                break
            continue

        if action_handler:
            action_handler(command, clipboard)
        else:
            command(clipboard)

        if not get_input():
            break


def analyze_text(command_name: str) -> None:
    """
    Print the given text analysis and prompt the user for any other
    clipboard input.

    Args:
        command_name: The name of the analysis function.
    """
    _run_command_loop(
        command_name,
        analysis_mod
    )


def replace_text(command_name: str) -> None:
    """
    Apply the selected replacement function to the clipboard and prompt
    the user for any other clipboard input.

    Args:
        command_name: The name of the replacement function.
    """
    _run_command_loop(
        command_name,
        replacement_mod,
        _replace_and_copy
    )


def warp_text(command_name: str) -> None:
    """
    Apply the selected warping function to the clipboard and prompt the
    user for any other clipboard input.

    Args:
        command_name: The name of the warping function.
    """
    _run_command_loop(
        command_name,
        warping_mod,
        _warp_and_copy
    )
