"""Main loop logic for executing commands."""

import gettext
from typing import Callable, TypeAlias

from textwarp._cli.constants.messages import (
    CLIPBOARD_ACCESS_ERROR_MSG,
    CLIPBOARD_CLEARED_MSG,
    MODIFIED_TEXT_COPIED_MSG
)
from textwarp._cli.ui import get_input, print_wrapped
from textwarp._cli.validation import EmptyClipboardError, validate_clipboard
from textwarp._commands import replacement

_ = gettext.gettext

__all__ = [
    'clear_clipboard',
    'replace_text',
    'run_command_loop',
    'warp_and_copy'
]

# Type alias for a function defining what to do with a command and
# clipboard text.
_ActionHandler: TypeAlias = Callable[[Callable[[str], str], str], None]


def _paste_and_validate() -> str | None:
    """
    Paste and validate clipboard text.

    Returns:
        clipboard | None: The validated clipboard text, or `None` if
            an error occurred.
    """
    import pyperclip
    try:
        clipboard = pyperclip.paste()
        validate_clipboard(clipboard)
        return clipboard
    except EmptyClipboardError as e:
        print_wrapped(str(e))
        return None
    except pyperclip.PyperclipException as e:
        msg = CLIPBOARD_ACCESS_ERROR_MSG + str(e)
        if 'xclip' in str(e) or 'xsel' in str(e):
            msg += _(
                "\nOn Linux, you may need to install 'xclip' or 'xsel' "
                '(e.g., sudo apt install xclip).'
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
        command_func: The replacement function.
        clipboard: The clipboard text to transform.
    """
    import pyperclip
    transformation: str = command_func(clipboard)
    pyperclip.copy(transformation)
    print_wrapped(_(MODIFIED_TEXT_COPIED_MSG))


def clear_clipboard() -> None:
    """Clear clipboard text."""
    import pyperclip
    pyperclip.copy('')
    print_wrapped(_(CLIPBOARD_CLEARED_MSG))


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
        command_func: The transformation function.
        clipboard: The clipboard text to transform.
    """
    import pyperclip
    transformation: str = command_func(clipboard)
    pyperclip.copy(transformation)
    print_wrapped(MODIFIED_TEXT_COPIED_MSG)
