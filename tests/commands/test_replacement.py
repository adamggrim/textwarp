"""Tests for replacement command functions."""

import pytest

from textwarp._cli.constants.messages import (
    CASE_NOT_FOUND_MSG,
    ENTER_VALID_CASE_PROMPT,
    ENTER_VALID_REGEX_PROMPT,
    ENTER_VALID_TEXT_PROMPT,
    REGEX_NOT_FOUND_MSG,
    TEXT_NOT_FOUND_MSG
)
from textwarp._commands import replacement

CASE_TEST_STRING = 'pascal_case'


def test_replace_case(simulate_input, capsys):
    simulate_input(['camel', 'snake', 'pascal'])

    result = replacement.replace_case(CASE_TEST_STRING)
    captured = capsys.readouterr()

    assert CASE_NOT_FOUND_MSG in captured.out
    assert ENTER_VALID_CASE_PROMPT in captured.out
    assert result == 'PascalCase'


def test_replace_case_early_exit(simulate_input):
    simulate_input(['quit'])

    with pytest.raises(SystemExit):
        replacement.replace_case(CASE_TEST_STRING)


def test_replace_regex(simulate_input, capsys):
    target_regex = r'\d{5}'
    replacement_str = 'vingt-quatre mille six cent un'

    simulate_input([r'\d{6}', target_regex, replacement_str])

    result = replacement.replace_regex(
        'Il ne fut même plus Jean Valjean; il fut le numéro 24601.'
    )
    captured = capsys.readouterr()

    assert REGEX_NOT_FOUND_MSG in captured.out
    assert ENTER_VALID_REGEX_PROMPT in captured.out
    assert result == (
        'Il ne fut même plus Jean Valjean; '
        'il fut le numéro vingt-quatre mille six cent un.'
    )


def test_replace_text(simulate_input, capsys):
    simulate_input(['cyanide', 'hemlock', 'coffee'])

    result = replacement.replace_text(
        'My heart aches, and a drowsy numbness pains\n'
        'My sense, as though of hemlock I had drunk.'
    )
    captured = capsys.readouterr()

    assert TEXT_NOT_FOUND_MSG in captured.out
    assert ENTER_VALID_TEXT_PROMPT in captured.out
    assert 'of coffee I had drunk' in result
    assert 'hemlock' not in result
