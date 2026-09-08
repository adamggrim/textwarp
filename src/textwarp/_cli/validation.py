"""Validators for text, clipboard and regular expression content."""

import argparse
import gettext
import regex as re

from textwarp._cli.args import ARGS_MAP, CommandType
from textwarp._cli.constants.messages import (
    ANALYSIS_ORDER_ERROR_MSG,
    CASE_EMPTY_ERROR_MSG,
    CASE_WHITESPACE_ERROR_MSG,
    CLIPBOARD_EMPTY_ERROR_MSG,
    CLIPBOARD_WHITESPACE_ERROR_MSG,
    EXCLUSIVE_CMD_ERROR_MSG,
    FIND_REPLACE_ARG_ERROR_MSG,
    INVALID_CASE_ERROR_MSG,
    MULTIPLE_MUTUALLY_EXCLUSIVE_ERROR_MSG,
    MULTIPLE_REPLACEMENT_ERROR_MSG,
    REGEX_EMPTY_ERROR_MSG,
    TEXT_EMPTY_ERROR_MSG
)
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
    'validate_command_combinations',
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
        raise NoCaseNameError(_(CASE_EMPTY_ERROR_MSG))
    elif case_name.strip() == '':
        raise WhitespaceCaseNameError(_(CASE_WHITESPACE_ERROR_MSG))
    elif case_name.lower() not in CASE_NAMES_FUNC_MAP:
        raise InvalidCaseNameError(_(INVALID_CASE_ERROR_MSG))


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
        raise EmptyClipboardError(_(CLIPBOARD_EMPTY_ERROR_MSG))
    elif clipboard.strip() == '':
        raise WhitespaceClipboardError(_(CLIPBOARD_WHITESPACE_ERROR_MSG))


def validate_command_combinations(
    active_cmds: list[str],
    args: argparse.Namespace,
    parser: argparse.ArgumentParser
) -> None:
    """
    Validate that combined command-line arguments do not conflict.

    Args:
        active_cmds: The ordered list of active commands.
        args: The parsed command-line arguments.
        parser: The `ArgumentParser` instance used to display error
            messages.

    Raises:
        SystemExit: If there is any invalid combination of arguments.
    """
    active_standalones = [
        c
        for c in active_cmds
        if ARGS_MAP[c].command_type == CommandType.STANDALONE
    ]
    active_replacements = [
        c
        for c in active_cmds
        if ARGS_MAP[c].command_type == CommandType.REPLACEMENT
    ]

    first_analysis_cmd_seen = False
    for cmd in active_cmds:
        if ARGS_MAP[cmd].command_type == CommandType.ANALYSIS:
            first_analysis_cmd_seen = True
        elif first_analysis_cmd_seen:
            parser.error(
                _(ANALYSIS_ORDER_ERROR_MSG).format(cmd=cmd)
            )

    if len(active_standalones) > 1:
        parser.error(
            _(MULTIPLE_MUTUALLY_EXCLUSIVE_ERROR_MSG).format(
                commands=', '.join(active_standalones)
            )
        )
    if active_standalones and len(active_cmds) > 1:
        cmd = active_standalones[0]
        parser.error(_(EXCLUSIVE_CMD_ERROR_MSG).format(cmd=cmd))

    if len(active_replacements) > 1:
        parser.error(
            _(MULTIPLE_REPLACEMENT_ERROR_MSG).format(
                commands=', '.join(active_replacements)
            )
        )

    is_replacement_cmd = len(active_replacements) > 0
    if (args.find or args.replace) and not is_replacement_cmd:
        parser.error(_(FIND_REPLACE_ARG_ERROR_MSG))


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
        raise NoRegexError(_(REGEX_EMPTY_ERROR_MSG))

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
        raise NoTextError(_(TEXT_EMPTY_ERROR_MSG))
