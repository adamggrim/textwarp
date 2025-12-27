import regex as re
from typing import Callable

from .._constants import (
    CASE_NAMES_FUNC_MAP,
    CASE_NAMES_REGEX_MAP,
    ENTER_CASE_TO_REPLACE_PROMPT,
    ENTER_REGEX_PROMPT,
    ENTER_REPLACEMENT_CASE_PROMPT,
    ENTER_REPLACEMENT_TEXT_PROMPT,
    ENTER_TEXT_TO_REPLACE_PROMPT,
    ENTER_VALID_CASE_NAME_PROMPT,
    ENTER_VALID_REGEX_PROMPT,
    ENTER_VALID_TEXT_PROMPT
)
from .._enums import CheckType
from .._exceptions import (
    CaseNotFoundError,
    RegexNotFoundError,
    TextToReplaceNotFoundError
)
from .._ui import print_wrapped
from .._validation import (
    validate_any_text,
    validate_case_name,
    validate_regex,
    validate_text
)

__all__ = [
    'case_replace',
    'replace',
    'regex_replace'
]


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


def case_replace(text: str) -> str:
    """
    Prompt the user for a case to replace and a replacement case, and
    return the transformed text.

    Args:
        text: The string to transform.

    Returns:
        str: The transformed text.
    """
    case_to_replace = _prompt_for_valid_input(
        ENTER_CASE_TO_REPLACE_PROMPT,
        validate_case_name,
        ENTER_VALID_CASE_NAME_PROMPT
    )
    replacement_case = _prompt_for_valid_input(
        ENTER_REPLACEMENT_CASE_PROMPT,
        validate_case_name,
        ENTER_VALID_CASE_NAME_PROMPT
    )
    return text.replace(case_to_replace, replacement_case)


def replace(text: str) -> str:
    """
    Prompt the user for a string to replace and a string to replace it,
    and return the transformed text.

    Args:
        text: The string to transform.

    Returns:
        str: The transformed text.
    """
    text_to_replace = _prompt_for_valid_input(
        ENTER_TEXT_TO_REPLACE_PROMPT,
        validate_text,
        ENTER_VALID_TEXT_PROMPT
    )
    replacement_text = _prompt_for_valid_input(
        ENTER_REPLACEMENT_TEXT_PROMPT,
        validate_text,
        ENTER_VALID_TEXT_PROMPT
    )
    return text.replace(text_to_replace, replacement_text)


def regex_replace(text: str) -> str:
    """
    Prompt the user for a regular expression to find and a string to
    replace it, and return the transformed text.

    Args:
        text: The string to transform.

    Returns:
        str: The transformed text.
    """
    regex_text = _prompt_for_valid_input(
        ENTER_REGEX_PROMPT,
        validate_regex,
        ENTER_VALID_REGEX_PROMPT
    )
    replacement_text = _prompt_for_valid_input(
        ENTER_REPLACEMENT_TEXT_PROMPT,
        validate_text,
        ENTER_VALID_TEXT_PROMPT
    )
    return re.sub(regex_text, replacement_text, text)
