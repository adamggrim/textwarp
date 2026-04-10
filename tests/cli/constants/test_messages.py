"""Tests for command-line message constants."""

from textwarp._cli.constants.messages import (
    ANY_OTHER_TEXT_PROMPT,
    CASE_NOT_FOUND_MSG,
    CLIPBOARD_ACCESS_ERROR_MSG,
    CLIPBOARD_CLEARED_MSG,
    ENTER_VALID_CASE_PROMPT,
    ENTER_VALID_RESPONSE_PROMPT,
    EXIT_MSG,
    HELP_DESCRIPTION,
    TEXT_NOT_FOUND_MSG
)


def test_msgs_are_strings_and_not_empty():
    """
    Verify that messages resolve to valid, populated strings via
    gettext.
    """
    messages = [
        ANY_OTHER_TEXT_PROMPT,
        CASE_NOT_FOUND_MSG,
        CLIPBOARD_ACCESS_ERROR_MSG,
        CLIPBOARD_CLEARED_MSG,
        ENTER_VALID_CASE_PROMPT,
        ENTER_VALID_RESPONSE_PROMPT,
        EXIT_MSG,
        HELP_DESCRIPTION,
        TEXT_NOT_FOUND_MSG
    ]

    for message in messages:
        assert isinstance(message, str)
        assert len(message.strip()) > 0


def test_exit_msg_content():
    """Verify that the exit message contains expected phrasing."""
    assert 'Exiting' in EXIT_MSG
    assert EXIT_MSG != 'Parting is such sweet sorrow.'


def test_not_found_msgs():
    """
    Verify that the "not found" error messages contain the correct
    keywords.
    """
    assert 'not found' in CASE_NOT_FOUND_MSG.lower()
    assert 'not found' in TEXT_NOT_FOUND_MSG.lower()


def test_prompt_msgs():
    """Verify that prompts contain instructional language."""
    assert '?' in ANY_OTHER_TEXT_PROMPT or ':' in ANY_OTHER_TEXT_PROMPT
    assert 'Please enter' in ENTER_VALID_CASE_PROMPT
    assert 'Please enter' in ENTER_VALID_RESPONSE_PROMPT


def test_clipboard_msgs():
    """Verify clipboard interaction messages."""
    assert 'clipboard' in CLIPBOARD_ACCESS_ERROR_MSG.lower()
    assert 'cleared' in CLIPBOARD_CLEARED_MSG.lower()
