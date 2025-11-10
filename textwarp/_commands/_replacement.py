import regex as re

from .._constants import (
    ENTER_TEXT_TO_REPLACE_PROMPT,
    ENTER_REGEX_PROMPT,
    ENTER_REPLACEMENT_PROMPT
)
from .._ui import print_wrapped

__all__ = [
    'replace',
    'regex_replace',
]


def replace(text: str) -> str:
    """
    Prompt the user for a string to find and replace, and return the
    transformed text.

    Args:
        text: The string to transform.

    Returns:
        str: The transformed text.
    """
    print_wrapped(ENTER_TEXT_TO_REPLACE_PROMPT)
    to_replace_text: str = input().rstrip('\n')
    print_wrapped(ENTER_REPLACEMENT_PROMPT)
    replacement_text: str = input().rstrip('\n')
    return text.replace(to_replace_text, replacement_text)


def regex_replace(text: str) -> str:
    """
    Prompt the user for a regular expression to find and replace, and
    return the transformed text.

    Args:
        text: The string to process.
    """
    print_wrapped(ENTER_REGEX_PROMPT)
    regex_text: str = input().rstrip('\n')
    print_wrapped(ENTER_REPLACEMENT_PROMPT)
    replacement_text: str = input().rstrip('\n')
    return re.sub(regex_text, replacement_text, text)
