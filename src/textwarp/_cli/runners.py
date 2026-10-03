"""Main loop logic for executing commands."""

import logging
from collections.abc import Callable
from types import ModuleType
from typing import Final, TypeAlias

from textwarp._cli.constants.messages import (
    CASE_TO_REPLACE_NOT_FOUND_MSG,
    CLIPBOARD_ACCESS_ERROR_MSG,
    CLIPBOARD_CLEARED_MSG,
    LINUX_XCLIP_WARNING_MSG,
    MODIFIED_TEXT_COPIED_MSG,
    REGEX_TO_REPLACE_NOT_FOUND_MSG,
    TEXT_TO_REPLACE_NOT_FOUND_MSG,
    UNEXPECTED_CLIPBOARD_ERROR_MSG
)
from textwarp._cli.ui import get_input, print_wrapped
from textwarp._cli.validation import (
    EmptyClipboardError,
    WhitespaceClipboardError,
    validate_clipboard
)
from textwarp._core.context import _
from textwarp._core.exceptions import MissingDependencyError

__all__ = [
    'NOT_FOUND_MSG_MAP',
    'clear_clipboard',
    'replace_and_copy',
    'run_command_loop',
    'warp_and_copy'
]

_ActionHandler: TypeAlias = Callable[[Callable[[str], str | None], str], None]

NOT_FOUND_MSG_MAP: Final[dict[str, str]] = {
    'replace-case': CASE_TO_REPLACE_NOT_FOUND_MSG,
    'replace-regex': REGEX_TO_REPLACE_NOT_FOUND_MSG,
    'replace-text': TEXT_TO_REPLACE_NOT_FOUND_MSG
}

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
        msg = _(CLIPBOARD_ACCESS_ERROR_MSG) + str(e)
        if 'xclip' in str(e) or 'xsel' in str(e):
            msg += _(LINUX_XCLIP_WARNING_MSG)
        print_wrapped(msg)
        return None
    except OSError:
        _logger.exception('Unexpected clipboard error.')
        print_wrapped(_(UNEXPECTED_CLIPBOARD_ERROR_MSG))
        return None


def clear_clipboard() -> None:
    """Clear clipboard text."""
    pyperclip = _get_pyperclip()
    pyperclip.copy('')
    print_wrapped(_(CLIPBOARD_CLEARED_MSG))


def replace_and_copy(
    command_func: Callable[[str], str],
    clipboard: str,
    not_found_msg: str = TEXT_TO_REPLACE_NOT_FOUND_MSG
) -> None:
    """
    Transform text using a replacement command and copy the result.
    Print if the target text was not found.
    """
    pyperclip = _get_pyperclip()
    transformation: str = command_func(clipboard)
    if transformation == clipboard:
        print_wrapped(_(not_found_msg))
        return
    pyperclip.copy(transformation)
    print_wrapped(_(MODIFIED_TEXT_COPIED_MSG))


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
