"""Runners for replacement commands."""

import regex as re
from typing import Callable

from .._core.constants import (
    CASE_NAMES_REGEX_MAP,
    ENTER_CASE_TO_REPLACE_PROMPT,
    ENTER_REGEX_PROMPT,
    ENTER_REPLACEMENT_CASE_PROMPT,
    ENTER_REPLACEMENT_TEXT_PROMPT,
    ENTER_TEXT_TO_REPLACE_PROMPT,
    ENTER_VALID_CASE_PROMPT,
    ENTER_VALID_REGEX_PROMPT,
    ENTER_VALID_TEXT_PROMPT
)
from .._cli.dispatch import CASE_NAMES_FUNC_MAP
from .._core.enums import PresenceCheckType
from .._core.exceptions import (
    CaseNotFoundError,
    RegexNotFoundError,
    TextToReplaceNotFoundError
)
from .._cli.ui import print_wrapped
from .._cli.validation import (
    validate_any_text,
    validate_case_name,
    validate_regex,
    validate_text
)

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
    Create a validator function that checks for the presence and
    validity of a case, regular expression or substring in a given
    string.

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

        search_input: A string input from the user, representing a case,
            regular expression or substring.
        """
        base_validator(search_input)

        if check_type is PresenceCheckType.CASE_NAME:
            case_key = search_input.lower()
            pattern = CASE_NAMES_REGEX_MAP.get(case_key)

            if pattern and not pattern.search(text):
                raise CaseNotFoundError('Case not found in text.')
        elif check_type is PresenceCheckType.REGEX:
            if not re.search(search_input, text):
                raise RegexNotFoundError(
                    'Regular expression not found in text.'
                )
        elif check_type is PresenceCheckType.SUBSTRING:
            if search_input not in text:
                raise TextToReplaceNotFoundError(
                    'Text to replace not found in text.'
                )

    return validator


def _prompt_for_valid_input(
    enter_text_prompt: str,
    validation_func: Callable[[str], None],
    enter_valid_text_prompt: str
) -> str:
    """
    Prompt the user for input until the input is valid.

    Args:
        enter_text_prompt: The prompt to display to the user.
        validation_func: A function that accepts a string as input,
            returning ``None`` if the string is valid or raising an
            exception if the string is invalid.
        enter_valid_text_prompt: The prompt to display when the input is
            invalid.
    """
    current_prompt = enter_text_prompt

    while True:
        print_wrapped(current_prompt)
        user_input = input().rstrip('\n')

        try:
            validation_func(user_input)
            return user_input
        except Exception as e:
            print_wrapped(str(e))
            current_prompt = enter_valid_text_prompt


def replace(text: str) -> str:
    """
    Prompt the user for a string to replace and a string to replace it,
    and return the transformed text.

    Args:
        text: The string to transform.

    Returns:
        str: The transformed text.
    """
    presence_validator = _create_presence_validator(
        validate_text,
        text,
        PresenceCheckType.SUBSTRING
    )

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


def replace_case(text: str) -> str:
    """
    Prompt the user for a case to replace and a replacement case, and
    return the transformed text.

    Args:
        text: The string to transform.

    Returns:
        str: The transformed text.
    """
    presence_validator = _create_presence_validator(
        validate_case_name,
        text,
        PresenceCheckType.CASE_NAME
    )

    case_to_replace_name = _prompt_for_valid_input(
        ENTER_CASE_TO_REPLACE_PROMPT,
        presence_validator,
        ENTER_VALID_CASE_PROMPT
    ).lower()
    replacement_case_name = _prompt_for_valid_input(
        ENTER_REPLACEMENT_CASE_PROMPT,
        validate_case_name,
        ENTER_VALID_CASE_PROMPT
    ).lower()

    search_pattern = CASE_NAMES_REGEX_MAP[case_to_replace_name]
    conversion_func = CASE_NAMES_FUNC_MAP[replacement_case_name]

    return search_pattern.sub(
        lambda match: conversion_func(match.group(0)),
        text
    )


def replace_regex(text: str) -> str:
    """
    Prompt the user for a regular expression to find and a string to
    replace it, and return the transformed text.

    Args:
        text: The string to transform.

    Returns:
        str: The transformed text.
    """
    presence_validator = _create_presence_validator(
        validate_regex, text, PresenceCheckType.REGEX
    )

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
