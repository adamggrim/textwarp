"""Main loop logic for executing commands."""

from typing import Callable, Final, TypeAlias

import pyperclip

from .args import ARGS_MAP
from .. import warping
from .._commands import analysis, replacement
from .._core.constants import (
    CLIPBOARD_ACCESS_ERROR_MESSAGE,
    CLIPBOARD_CLEARED_MESSAGE,
    MODIFIED_TEXT_COPIED_MESSAGE,
    TEXT_TO_REPLACE_NOT_FOUND_MESSAGE
)

from .ui import get_input, print_wrapped
from .validation import EmptyClipboardError, validate_clipboard

__all__ = [
    'analyze_text',
    'clear_clipboard',
    'replace_text',
    'run_command_loop',
    'warp_and_copy',
    'warp_text'
]

# Set of warping module command names.
_WARPING_MODULE_COMMANDS: Final[set[str]] = set(warping.__all__)

# Type alias for a function defining what to do with a command and
# clipboard text.
_ActionHandler: TypeAlias = Callable[[Callable[[str], str], str], None]


def _paste_and_validate() -> str | None:
    """
    Paste and validate clipboard text.

    Returns:
        clipboard | None: The validated clipboard text, or ``None`` if
            an error occurred.
    """
    try:
        clipboard = pyperclip.paste()
        validate_clipboard(clipboard)
        return clipboard
    except EmptyClipboardError as e:
        print_wrapped(str(e))
        return None
    except pyperclip.PyperclipException as e:
        msg = CLIPBOARD_ACCESS_ERROR_MESSAGE + str(e)
        if 'xclip' in str(e) or 'xsel' in str(e):
            msg += (
                "\nOn Linux, you may need to install 'xclip' or 'xsel' "
                "(e.g., sudo apt install xclip)."
            )
        print_wrapped(msg)
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


def analyze_text(command_name: str) -> None:
    """
    Print the given text analysis and prompt the user for any other
    clipboard input.

    Args:
        command_name: The name of the analysis function.
    """
    func_name = command_name.replace('-', '_')
    command_func: Callable[[str], str] = getattr(analysis, func_name)

    run_command_loop(command_func)


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
        replacement,
        command_name
    )

    run_command_loop(
        command_func,
        _replace_and_copy
    )


def run_command_loop(
    command_func: Callable[[str], str],
    action_handler: _ActionHandler | None = None
) -> None:
    """
    Run a module command to transform or analyze clipboard text.

    Args:
        command_func: The command function.
        action_handler | None: A function defining what to do with the
            command and clipboard text.
    """
    while True:
        clipboard = _paste_and_validate()

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


def warp_and_copy(
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


def warp_text(command_name: str) -> None:
    """
    Apply the selected warping function to the clipboard and prompt the
    user for any other clipboard input.

    Args:
        command_name: The name of the warping function.
    """
    if command_name in _WARPING_MODULE_COMMANDS:
        command_func: Callable[[str], str] = getattr(warping, command_name)
    else:
        func_name = command_name.replace('_', '-')
        command_func: Callable[[str], str] = ARGS_MAP[func_name][0]

    run_command_loop(
        command_func,
        warp_and_copy
    )
