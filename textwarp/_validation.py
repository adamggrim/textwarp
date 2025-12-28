import regex as re

from ._dispatch import CASE_NAMES_FUNC_MAP
from ._exceptions import (
    EmptyClipboardError,
    InvalidCaseNameError,
    NoCaseNameError,
    NoRegexError,
    NoTextError,
    WhitespaceCaseNameError,
    WhitespaceClipboardError
)


def validate_any_text(text: str) -> None:
    """
    Validate and accept any text string, including empty text.

    Args:
        text: A string of any text.
    """
    pass


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
        raise EmptyClipboardError('Clipboard is empty.')
    elif clipboard.strip() == '':
        raise WhitespaceClipboardError('Clipboard contains only whitespace.')


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
        raise NoCaseNameError('Case string is empty.')
    elif case_name.strip() == '':
        raise WhitespaceCaseNameError('Case contains only whitespace.')
    elif case_name.lower() not in CASE_NAMES_FUNC_MAP:
        raise InvalidCaseNameError('Invalid case.')


def validate_regex(regex: str) -> None:
    """
    Validate a regular expression string.

    This function checks whether the string is a valid regular
    expression.

    Args:
        regex: A string representing a regular expression.

    Raises:
        NoRegexError: If the input string is empty.
        re.error: If the input string is not a valid regular expression.
    """
    if regex == '':
        raise NoRegexError('Regex string is empty.')

    re.compile(regex)


def validate_text(text: str) -> None:
    """
    Validate a text string.

    This function applies when deletion of a string is invalid.

    Args:
        text: A string of text.
    Raises:
        ValueError: If the text string is empty.
    """
    if text == '':
        raise NoTextError('Text string is empty.')
