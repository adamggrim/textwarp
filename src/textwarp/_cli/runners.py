"""Main loop logic for executing commands."""

import gettext
import logging
from collections.abc import Callable
from typing import TypeAlias
from types import ModuleType

from textwarp._cli.constants.messages import (
    CLIPBOARD_ACCESS_ERROR_MSG,
    CLIPBOARD_CLEARED_MSG,
    LINUX_XCLIP_WARNING_MSG,
    MODIFIED_TEXT_COPIED_MSG,
    UNEXPECTED_CLIPBOARD_ERROR_MSG
)
from textwarp._cli.ui import get_input, print_wrapped
from textwarp._cli.validation import (
    EmptyClipboardError,
    WhitespaceClipboardError,
    validate_clipboard
)
from textwarp._commands import replacement
from textwarp._core.exceptions import MissingDependencyError

_ = gettext.gettext

__all__ = [
    'clear_clipboard',
    'replace_text',
    'run_command_loop',
    'warp_and_copy'
]

_ActionHandler: TypeAlias = Callable[[Callable[[str], str | None], str], None]

_logger = logging.getLogger(__name__)


def _get_pyperclip() -> ModuleType:
    """Helper to safely import pyperclip or exit with an error."""
    try:
        import pyperclip
        return pyperclip
    except ImportError as e:
        raise MissingDependencyError(
            'pyperclip',
            'Clipboard support',
            'clipboard'
        ) from e


def _paste_and_validate() -> str | None:
    """Paste and validate clipboard text."""
    pyperclip = _get_pyperclip()
    try:
        clipboard = pyperclip.paste()
        validate_clipboard(clipboard)
        return clipboard
    except (EmptyClipboardError, WhitespaceClipboardError) as e:
        print_wrapped(str(e))
        return None
    except pyperclip.PyperclipException as e:
        msg = CLIPBOARD_ACCESS_ERROR_MSG + str(e)
        if 'xclip' in str(e) or 'xsel' in str(e):
            msg += LINUX_XCLIP_WARNING_MSG
        print_wrapped(msg)
        return None
    except OSError:
        _logger.exception('Unexpected clipboard error.')
        print_wrapped(UNEXPECTED_CLIPBOARD_ERROR_MSG)
        return None


def _replace_and_copy(
    command_func: Callable[[str], str],
    clipboard: str
) -> None:
    """
    Transform text using a replacement command and copy the result.
    Print if the target text was not found.
    """
    pyperclip = _get_pyperclip()
    transformation: str = command_func(clipboard)
    pyperclip.copy(transformation)
    print_wrapped(_(MODIFIED_TEXT_COPIED_MSG))


def clear_clipboard() -> None:
    """Clear clipboard text."""
    pyperclip = _get_pyperclip()
    pyperclip.copy('')
    print_wrapped(_(CLIPBOARD_CLEARED_MSG))


def replace_text(command_name: str) -> None:
    """
    Apply the selected replacement function to the clipboard and prompt
    the user for any other clipboard input.
    """
    prompt_name = (
        f"prompt_for_{command_name.replace('replace_', 'replacement_')}"
    )

    prompt_func = getattr(replacement, prompt_name)
    exec_func = getattr(replacement, command_name)

    arg_to_replace, replacement_arg = prompt_func()

    def configured_func(text: str) -> str:
        return exec_func(text, arg_to_replace, replacement_arg)

    run_command_loop(
        configured_func,
        _replace_and_copy
    )


def run_command_loop(
    command_func: Callable[[str], str | None],
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
    """
    pyperclip = _get_pyperclip()
    transformation: str = command_func(clipboard)
    pyperclip.copy(transformation)
    print_wrapped(_(MODIFIED_TEXT_COPIED_MSG))
