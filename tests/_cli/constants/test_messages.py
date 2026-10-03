"""Tests for CLI message constants."""

import pytest

from textwarp._cli.constants import messages
from textwarp._cli.constants.messages import (
    ANY_OTHER_TEXT_PROMPT,
    CASE_TO_REPLACE_NOT_FOUND_MSG,
    CLIPBOARD_ACCESS_ERROR_MSG,
    CLIPBOARD_CLEARED_MSG,
    ENTER_VALID_CASE_PROMPT,
    ENTER_VALID_RESPONSE_PROMPT,
    EXIT_MSG,
    TEXT_TO_REPLACE_NOT_FOUND_MSG
)


@pytest.mark.parametrize('msg_name', messages.__all__)
def test_msgs_are_strings_and_not_empty(msg_name):
    message = getattr(messages, msg_name)
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
