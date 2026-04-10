"""Runners for replacement commands."""

import gettext
from typing import Callable

import regex as re

from textwarp._cli.constants.messages import (
    ENTER_CASE_TO_REPLACE_PROMPT,
    ENTER_REGEX_PROMPT,
    ENTER_REPLACEMENT_CASE_PROMPT,
    ENTER_REPLACEMENT_TEXT_PROMPT,
    ENTER_TEXT_TO_REPLACE_PROMPT,
    ENTER_VALID_CASE_PROMPT,
    ENTER_VALID_REGEX_PROMPT,
    ENTER_VALID_TEXT_PROMPT,
    CASE_NOT_FOUND_MSG,
    REGEX_NOT_FOUND_MSG,
    TEXT_NOT_FOUND_MSG
)
from textwarp._cli.constants.inputs import get_exit_inputs, get_no_inputs
from textwarp._cli.dispatch import CASE_NAMES_FUNC_MAP
from textwarp._core.constants.maps import get_case_names_regex_map
from textwarp._core.enums import PresenceCheckType
from textwarp._core.exceptions import (
    TextwarpValidationError,
    CaseNotFoundError,
    RegexNotFoundError,
    TextNotFoundError
)
from textwarp._cli.ui import print_wrapped, program_exit
from textwarp._cli.validation import (
    validate_any_text,
    validate_case_name,
    validate_regex,
    validate_text
)

_ = gettext.gettext

__all__ = [
    'replace',
    'replace_case',
    'replace_regex'
]


def _create_presence_validator(
    base_validator: Callable[[str], None],
    text: str,
    check_type: PresenceCheckType
) -> Callable[[str], None]:
    """
    Create a function that checks for the presence and validity of a
    case, regular expression or substring in a given string.

    Args:
        base_validator: A function that validates the input without
            checking for presence.
        text: The string to search.
        check_type: The type of check to perform (case, regex or
            substring).

    Returns:
        Callable[[str], None]: A validator function.
    """
    def validator(search_input: str) -> None:
        """
        Check the user input for presence in the given string.

        Args:
            search_input: A string input from the user, representing a
                case, regular expression or substring.

        Raises:
            CaseNotFoundError: If the case input is not found in the
                string.
            RegexNotFoundError: If the regular expression input is not
                found in the string.
            TextNotFoundError: If the substring input is not found in
                the string.
        """
        base_validator(search_input)

        if check_type is PresenceCheckType.CASE_NAME:
            case_key = search_input.lower()
            pattern = get_case_names_regex_map().get(case_key)

            if pattern and not pattern.search(text):
                raise CaseNotFoundError(_(CASE_NOT_FOUND_MSG))
        elif check_type is PresenceCheckType.REGEX:
            if not re.search(search_input, text):
                raise RegexNotFoundError(_(REGEX_NOT_FOUND_MSG))
        elif check_type is PresenceCheckType.SUBSTRING:
            if search_input not in text:
                raise TextNotFoundError(_(TEXT_NOT_FOUND_MSG))

    return validator


def _prompt_for_valid_input(
    enter_text_prompt: str,
    validation_func: Callable[[str], None],
    enter_valid_text_prompt: str,
    allow_early_exit: bool = False
) -> str:
    """
    Prompt the user for input until the input is valid.

    Args:
        enter_text_prompt: The prompt to display to the user.
        validation_func: A function that accepts a string as input and
            returns `None` if the string is valid or raises an
            exception if the string is invalid.
        enter_valid_text_prompt: The prompt to display when the input is
            invalid.
        allow_early_exit: Whether to allow the user to exit early by
            entering an exit input.
    """
    current_prompt = enter_text_prompt

    while True:
        print_wrapped(current_prompt)
        user_input = input().rstrip('\n')

        exit_commands: set[str] = get_exit_inputs() | get_no_inputs()
        is_exiting = user_input.strip().lower() in exit_commands

        if allow_early_exit and is_exiting:
            program_exit()

        try:
            validation_func(user_input)
            return user_input
        except TextwarpValidationError as e:
            print_wrapped(str(e))
            current_prompt = enter_valid_text_prompt


def replace(
    text: str,
    arg_to_replace: str | None = None,
    replacement_arg: str | None = None
) -> str:
    """
    Prompt the user or extract arguments for a string to replace and a
    string to replace it, and return the transformed text.

    Args:
        text: The string to transform.
        arg_to_replace: An optional string to replace. If not provided,
            the function will prompt the user for one.
        replacement_arg: An optional replacement string. If not
            provided, the function will prompt the user for one.

    Returns:
        str: The transformed text.
    """
    presence_validator = _create_presence_validator(
        validate_text,
        text,
        PresenceCheckType.SUBSTRING
    )

    if arg_to_replace is not None and replacement_arg is not None:
        presence_validator(arg_to_replace)
        # Accept any text (including empty text) for replacement.
        validate_any_text(replacement_arg)
        text_to_replace = arg_to_replace
        replacement_text = replacement_arg
    else:
        text_to_replace = _prompt_for_valid_input(
            ENTER_TEXT_TO_REPLACE_PROMPT,
            presence_validator,
            ENTER_VALID_TEXT_PROMPT
        )
        replacement_text = _prompt_for_valid_input(
            ENTER_REPLACEMENT_TEXT_PROMPT,
            # Accept any text (including empty text) for replacement.
            validate_any_text,
            ENTER_VALID_TEXT_PROMPT
        )

    return text.replace(text_to_replace, replacement_text)


def replace_case(
    text: str,
    arg_to_replace: str | None = None,
    replacement_arg: str | None = None
) -> str:
    """
    Prompt the user or extract arguments for a case to replace and a
    replacement case, and return the transformed text.

    Args:
        text: The string to transform.
        arg_to_replace: An optional case to replace. If not
            provided, the function will prompt the user for one.
        replacement_arg: An optional replacement case name. If not
            provided, the function will prompt the user for one.

    Returns:
        str: The transformed text.
    """
    presence_validator = _create_presence_validator(
        validate_case_name,
        text,
        PresenceCheckType.CASE_NAME
    )

    if arg_to_replace is not None and replacement_arg is not None:
        presence_validator(arg_to_replace)
        validate_case_name(replacement_arg)
        case_to_replace_name = arg_to_replace.lower()
        replacement_case_name = replacement_arg.lower()
    else:
        case_to_replace_name = _prompt_for_valid_input(
            ENTER_CASE_TO_REPLACE_PROMPT,
            presence_validator,
            ENTER_VALID_CASE_PROMPT,
            allow_early_exit=True
        ).lower()
        replacement_case_name = _prompt_for_valid_input(
            ENTER_REPLACEMENT_CASE_PROMPT,
            validate_case_name,
            ENTER_VALID_CASE_PROMPT,
            allow_early_exit=True
        ).lower()

    search_pattern = get_case_names_regex_map()[case_to_replace_name]
    conversion_func = CASE_NAMES_FUNC_MAP[replacement_case_name]

    return search_pattern.sub(
        lambda match: conversion_func(match.group(0)),
        text
    )


def replace_regex(
    text: str,
    arg_to_replace: str | None = None,
    replacement_arg: str | None = None
) -> str:
    """
    Prompt the user or extract arguments for a regular expression to
    find and a string to replace it, and return the transformed text.

    Args:
        text: The string to transform.

    Returns:
        str: The transformed text.
    """
    presence_validator = _create_presence_validator(
        validate_regex, text, PresenceCheckType.REGEX
    )

    if arg_to_replace is not None and replacement_arg is not None:
        presence_validator(arg_to_replace)
        # Accept any text (including empty text) for replacement.
        validate_any_text(replacement_arg)
        regex_text = arg_to_replace
        replacement_text = replacement_arg
    else:
        regex_text = _prompt_for_valid_input(
            ENTER_REGEX_PROMPT,
            presence_validator,
            ENTER_VALID_REGEX_PROMPT
        )
        replacement_text = _prompt_for_valid_input(
            ENTER_REPLACEMENT_TEXT_PROMPT,
            # Accept any text (including empty text) for replacement.
            validate_any_text,
            ENTER_VALID_TEXT_PROMPT
        )

    return re.sub(regex_text, replacement_text, text)
