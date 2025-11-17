from typing import Callable

import pyperclip

from ._args import ARGS_MAP
from ._commands import (
    _analysis,
    _replacement
)
from ._constants import (
    CLIPBOARD_ACCESS_ERROR_MESSAGE,
    CLIPBOARD_CLEARED_MESSAGE,
    MODIFIED_TEXT_COPIED_MESSAGE,
    TEXT_TO_REPLACE_NOT_FOUND_MESSAGE
)
from ._ui import (
    get_input,
    print_wrapped
)
from ._validation import (
    EmptyClipboardError,
    validate_clipboard
)
from . import warping

WARPING_MODULE_COMMANDS: set[str] = set(warping.__all__)


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
    command_func: Callable[[str], str],
    clipboard: str
) -> None:
    """
    Transform text using a replacement command and copy the result.
    Print if the replacement was not found.

    Args:
        command: The replacement function.
        clipboard: The clipboard text to transform.
    """
    transformation: str = command_func(clipboard)

    if transformation == clipboard:
        print_wrapped(TEXT_TO_REPLACE_NOT_FOUND_MESSAGE)
    else:
        pyperclip.copy(transformation)
        print_wrapped(MODIFIED_TEXT_COPIED_MESSAGE)


def _warp_and_copy(
    command_func: Callable[[str], str],
    clipboard: str
) -> None:
    """
    Transform text using a given command and copy the result back to the
    clipboard.

    Args:
        command: The transformation function.
        clipboard: The clipboard text to transform.
    """
    transformation: str = command_func(clipboard)
    pyperclip.copy(transformation)
    print_wrapped(MODIFIED_TEXT_COPIED_MESSAGE)


def _run_command_loop(
    command_func: Callable[[str], str],
    action_handler: Callable[[Callable[[str], str], str], None] | None = None
) -> None:
    """
    Run a module command to transform or analyze clipboard text.

    Args:
        command_func: The command function.
        action_handler: A function defining what to do with the
            command and clipboard text.
    """
    while True:
        clipboard: str | None = _paste_and_validate()

        if clipboard is None:
            if not get_input():
                break
            continue

        if action_handler:
            action_handler(command_func, clipboard)
        else:
            command_func(clipboard)

        if not get_input():
            break


def analyze_text(command_name: str) -> None:
    """
    Print the given text analysis and prompt the user for any other
    clipboard input.

    Args:
        command_name: The name of the analysis function.
    """
    func_name: str = command_name.replace('-', '_')
    command_func: Callable[[str], str] = getattr(_analysis, func_name)

    _run_command_loop(command_func)


def clear_clipboard() -> None:
    """Clear clipboard text."""
    pyperclip.copy('')
    print_wrapped(CLIPBOARD_CLEARED_MESSAGE)


def replace_text(command_name: str) -> None:
    """
    Apply the selected replacement function to the clipboard and prompt
    the user for any other clipboard input.

    Args:
        command_name: The name of the replacement function.
    """
    command_func: Callable[[str], str] = getattr(
        _replacement,
        command_name
    )

    _run_command_loop(
        command_func,
        _replace_and_copy
    )


def warp_text(command_name: str) -> None:
    """
    Apply the selected warping function to the clipboard and prompt the
    user for any other clipboard input.

    Args:
        command_name: The name of the warping function.
    """
    if command_name in WARPING_MODULE_COMMANDS:
        command_func = getattr(warping, command_name)
    else:
        func_name = command_name.replace('_', '-')
        command_func = ARGS_MAP[func_name][0]

    _run_command_loop(
        command_func,
        _warp_and_copy
    )
