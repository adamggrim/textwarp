"""Validators for text, clipboard and regular expression content."""

import gettext
import regex as re

from textwarp._cli.dispatch import CASE_NAMES_FUNC_MAP
from textwarp._core.exceptions import (
    EmptyClipboardError,
    InvalidCaseNameError,
    InvalidRegexError,
    NoCaseNameError,
    NoRegexError,
    NoTextError,
    WhitespaceCaseNameError,
    WhitespaceClipboardError
)

_ = gettext.gettext

__all__ = [
    'validate_case_name',
    'validate_clipboard',
    'validate_regex',
    'validate_text'
]


def validate_case_name(case_name: str) -> None:
    """
    Validate a case name string.

    This function checks whether the string is a valid case name (i.e.,
    camel case, dot case, lowercase, kebab case, Pascal case, snake case
    or uppercase).

    Args:
        case_name: A string representing a case name.

    Raises:
        NoCaseNameError: If the input string is empty.
        WhitespaceCaseNameError: If the input string contains only
            whitespace.
        InvalidCaseNameError: If the input is not a valid case name.
    """
    if case_name == '':
        raise NoCaseNameError(_('Case input is empty.'))
    elif case_name.strip() == '':
        raise WhitespaceCaseNameError(_('Case contains only whitespace.'))
    elif case_name.lower() not in CASE_NAMES_FUNC_MAP:
        raise InvalidCaseNameError(_('Invalid case.'))


def validate_clipboard(clipboard: str) -> None:
    """
    Validate the clipboard input.

    This function checks if the clipboard content is an empty string or
    contains only whitespace.

    Args:
        clipboard: A string representing the content of the clipboard.

    Raises:
        EmptyClipboardError: If the clipboard string is empty.
        WhitespaceClipboardError: If the clipboard string contains only
            whitespace.
    """
    if clipboard == '':
        raise EmptyClipboardError(_('Clipboard is empty.'))
    elif clipboard.strip() == '':
        raise WhitespaceClipboardError(_('Clipboard contains only whitespace.'))


def validate_regex(regex: str) -> None:
    """
    Validate a regular expression string.

    This function checks whether the string is a valid regular
    expression.

    Args:
        regex: A string representing a regular expression.

    Raises:
        NoRegexError: If the input string is empty.
        InvalidRegexError: If the input string is not a valid regular
            expression.
    """
    if regex == '':
        raise NoRegexError(_('Regex input is empty.'))

    try:
        re.compile(regex)
    except re.error as e:
        raise InvalidRegexError(str(e))


def validate_text(text: str) -> None:
    """
    Validate a text string, excluding empty text.

    Args:
        text: A string of text.

    Raises:
        NoTextError: If the text string is empty.
    """
    if text == '':
        raise NoTextError(_('Text input is empty.'))
