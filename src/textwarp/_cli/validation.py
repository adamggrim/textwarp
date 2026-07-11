"""Validators for text, clipboard and regular expression content."""

import argparse
import gettext
import regex as re

from textwarp._cli.args import (
    ARGS_MAP,
    CASING_COMMANDS,
    MUTUALLY_EXCLUSIVE_COMMANDS,
    REPLACEMENT_COMMANDS,
    SEPARATOR_COMMANDS
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
        raise WhitespaceClipboardError(
            _('Clipboard contains only whitespace.')
        )


def validate_command_combinations(
    args: argparse.Namespace,
    parser: argparse.ArgumentParser
) -> None:
    """
    Validate that combined command-line arguments do not conflict.

    Args:
        args: The parsed command-line arguments.
        parser: The `ArgumentParser` instance used to display error
            messages.

    Raises:
        SystemExit: If there is any invalid combination of arguments.
    """
    active_cmds = [
        key for key in ARGS_MAP
        if getattr(args, key.replace('-', '_'), False)
    ]

    active_separators = [c for c in active_cmds if c in SEPARATOR_COMMANDS]
    active_casings = [c for c in active_cmds if c in CASING_COMMANDS]
    active_mutually_exclusives = [
        c for c in active_cmds if c in MUTUALLY_EXCLUSIVE_COMMANDS
    ]

    if len(active_separators) > 1:
        parser.error(
            _('Cannot combine multiple separator styles: {styles}').format(
                styles=', '.join(active_separators)
            )
        )
    if len(active_casings) > 1:
        parser.error(
            _('Cannot combine multiple casing styles: {styles}').format(
                styles=', '.join(active_casings)
            )
        )
    if len(active_mutually_exclusives) > 1:
        parser.error(
            _('Cannot combine multiple exclusive commands: {commands}').format(
                commands=', '.join(active_mutually_exclusives)
            )
        )
    if active_mutually_exclusives and (active_separators or active_casings):
        cmd = active_mutually_exclusives[0]
        msg = _(
            "Command '{cmd}' cannot be combined with casing or separator "
            'commands.'
        )
        parser.error(msg.format(cmd=cmd))

    is_replacement_cmd = any(c in REPLACEMENT_COMMANDS for c in active_cmds)
    if (args.find or args.replace) and not is_replacement_cmd:
        parser.error(
            _(
                'The --find (-f) and --replace (-r) arguments can only '
                'be used with replacement commands (--replace, '
                '--replace-case, --replace-regex).'
            )
        )

    if args.markdown:
        if active_separators:
            parser.error(
                _(
                    'The --markdown flag cannot be combined with manual '
                    'separator commands: {styles}'
                ).format(styles=', '.join(active_separators))
            )


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
