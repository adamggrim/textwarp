"""Tests for command-line message constants."""

import pytest

from textwarp._cli.constants.messages import (
    ANY_OTHER_TEXT_PROMPT,
    CASE_EMPTY_ERROR_MSG,
    CASE_TO_REPLACE_NOT_FOUND_MSG,
    CASE_WHITESPACE_ERROR_MSG,
    CLIPBOARD_ACCESS_ERROR_MSG,
    CLIPBOARD_CLEARED_MSG,
    CLIPBOARD_EMPTY_ERROR_MSG,
    CLIPBOARD_WHITESPACE_ERROR_MSG,
    ENTER_VALID_CASE_PROMPT,
    ENTER_VALID_RESPONSE_PROMPT,
    EXIT_MSG,
    HELP_DESCRIPTION,
    INVALID_CASE_ERROR_MSG,
    LINUX_XCLIP_WARNING_MSG,
    REGEX_EMPTY_ERROR_MSG,
    TEXT_EMPTY_ERROR_MSG,
    TEXT_TO_REPLACE_NOT_FOUND_MSG,
    UNEXPECTED_CLIPBOARD_ERROR_MSG
)


@pytest.mark.parametrize('message', [
    ANY_OTHER_TEXT_PROMPT,
    CASE_EMPTY_ERROR_MSG,
    CASE_TO_REPLACE_NOT_FOUND_MSG,
    CASE_WHITESPACE_ERROR_MSG,
    CLIPBOARD_ACCESS_ERROR_MSG,
    CLIPBOARD_CLEARED_MSG,
    CLIPBOARD_EMPTY_ERROR_MSG,
    CLIPBOARD_WHITESPACE_ERROR_MSG,
    ENTER_VALID_CASE_PROMPT,
    ENTER_VALID_RESPONSE_PROMPT,
    EXIT_MSG,
    HELP_DESCRIPTION,
    INVALID_CASE_ERROR_MSG,
    LINUX_XCLIP_WARNING_MSG,
    REGEX_EMPTY_ERROR_MSG,
    TEXT_EMPTY_ERROR_MSG,
    TEXT_TO_REPLACE_NOT_FOUND_MSG,
    UNEXPECTED_CLIPBOARD_ERROR_MSG
])
def test_msgs_are_strings_and_not_empty(message):
    assert isinstance(message, str)
    assert len(message.strip()) > 0


def test_exit_msg_content():
    assert 'Exiting' in EXIT_MSG
    assert EXIT_MSG != 'Parting is such sweet sorrow.'


def test_not_found_msgs():
    assert 'not found' in CASE_TO_REPLACE_NOT_FOUND_MSG.lower()
    assert 'not found' in TEXT_TO_REPLACE_NOT_FOUND_MSG.lower()


def test_prompt_msgs():
    assert '?' in ANY_OTHER_TEXT_PROMPT or ':' in ANY_OTHER_TEXT_PROMPT
    assert 'Please enter' in ENTER_VALID_CASE_PROMPT
    assert 'Please enter' in ENTER_VALID_RESPONSE_PROMPT


def test_clipboard_msgs():
    assert 'clipboard' in CLIPBOARD_ACCESS_ERROR_MSG.lower()
    assert 'cleared' in CLIPBOARD_CLEARED_MSG.lower()
