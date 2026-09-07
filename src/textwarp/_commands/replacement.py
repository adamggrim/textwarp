"""Runners for find-and-replace commands."""

import gettext
import regex as re

from textwarp._cli.spinner import run_with_spinner
from textwarp._cli.constants.messages import (
    CASE_TO_REPLACE_NOT_FOUND_MSG,
    REGEX_TO_REPLACE_NOT_FOUND_MSG,
    TEXT_TO_REPLACE_NOT_FOUND_MSG
)
from textwarp._cli.dispatch import CASE_NAMES_FUNC_MAP
from textwarp._core.constants.maps import get_case_names_regex_map
from textwarp._cli.ui import print_wrapped
from textwarp._cli.validation import (
    validate_case_name,
    validate_regex,
    validate_text
)
from textwarp._lib import replacement as lib_replacement

_ = gettext.gettext

__all__ = [
    'replace_case',
    'replace_regex',
    'replace_text'
]

_ESCAPE_PATTERN = re.compile(r'\\[nrt\\]')
_ESCAPE_MAP = {
    r'\n': '\n',
    r'\r': '\r',
    r'\t': '\t',
    r'\\': '\\'
}


def _parse_cli_escapes(text: str) -> str:
    """
    Convert CLI escape strings into their corresponding whitespace
    characters.
    """
    def _replace_escape(match: re.Match[str]) -> str:
        return _ESCAPE_MAP[match.group(0)]

    # Match a backslash followed by "n", "r", "t" or another backslash.
    return re.sub(_ESCAPE_PATTERN, _replace_escape, text)


def replace_case(text: str, arg_to_replace: str, replacement_arg: str) -> str:
    """
    Extract arguments for a case to replace and a replacement case,
    and return the transformed text.

    Args:
        text: The string to transform.
        arg_to_replace: The case to replace.
        replacement_arg: The replacement case name.

    Returns:
        str: The transformed text.
    """
    validate_case_name(arg_to_replace)
    case_to_replace_name = arg_to_replace.lower()
    search_pattern = get_case_names_regex_map().get(case_to_replace_name)

    if search_pattern and not search_pattern.search(text):
        print_wrapped(_(CASE_TO_REPLACE_NOT_FOUND_MSG))
        return text

    validate_case_name(replacement_arg)
    replacement_case_name = replacement_arg.lower()

    search_pattern = get_case_names_regex_map()[case_to_replace_name]
    conversion_func = CASE_NAMES_FUNC_MAP[replacement_case_name]

    return run_with_spinner(
        lib_replacement.replace_case, text, search_pattern, conversion_func
    )


def replace_regex(text: str, arg_to_replace: str, replacement_arg: str) -> str:
    """
    Extract arguments for a target regular expression and a string to
    replace it, and return the transformed text.

    Args:
        text: The string to transform.
        arg_to_replace: The regular expression to search for.
        replacement_arg: The replacement text.

    Returns:
        str: The transformed text.
    """
    validate_regex(arg_to_replace)
    if not re.search(arg_to_replace, text):
        print_wrapped(_(REGEX_TO_REPLACE_NOT_FOUND_MSG))
        return text

    parsed_replacement = _parse_cli_escapes(replacement_arg)

    return run_with_spinner(
        lib_replacement.replace_regex, text, arg_to_replace, parsed_replacement
    )


def replace_text(text: str, arg_to_replace: str, replacement_arg: str) -> str:
    """
    Extract arguments for a target string and a string to replace it,
    and return the transformed text.

    Args:
        text: The string to transform.
        arg_to_replace: The specific string to find and replace.
        replacement_arg: The replacement text.

    Returns:
        str: The transformed text.
    """
    validate_text(arg_to_replace)
    if arg_to_replace not in text:
        print_wrapped(_(TEXT_TO_REPLACE_NOT_FOUND_MSG))
        return text

    parsed_replacement = _parse_cli_escapes(replacement_arg)

    return run_with_spinner(
        lib_replacement.replace_text, text, arg_to_replace, parsed_replacement
    )
