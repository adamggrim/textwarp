"""Tests for replacement command functions."""

import pytest

from textwarp._cli.constants.messages import (
    CASE_NOT_FOUND_MESSAGE,
    ENTER_VALID_CASE_PROMPT,
    ENTER_VALID_REGEX_PROMPT,
    ENTER_VALID_TEXT_PROMPT,
    REGEX_NOT_FOUND_MESSAGE,
    TEXT_NOT_FOUND_MESSAGE
)
from textwarp._commands import replacement

CASE_TEST_STRING = 'pascal_case'

REGEX_TEST_STRING = '525,600 minutes'

TEXT_TEST_STRING = (
    'My heart aches, and a drowsy numbness pains\n'
    'My sense, as though of hemlock I had drunk.'
)


def test_replace_case(simulate_input, capsys):
    """Test case replacement and presence validation."""
    simulate_input(['camel', 'snake', 'pascal'])

    result = replacement.replace_case(CASE_TEST_STRING)
    captured = capsys.readouterr()

    assert CASE_NOT_FOUND_MESSAGE in captured.out
    assert ENTER_VALID_CASE_PROMPT in captured.out
    assert result == 'PascalCase'


def test_replace_case_early_exit(simulate_input):
    """Test that early exit commands exit the program gracefully."""
    simulate_input(['quit'])

    with pytest.raises(SystemExit):
        replacement.replace_case(CASE_TEST_STRING)


def test_replace_text(simulate_input, capsys):
    """Test text replacement and presence validation."""
    simulate_input(['cyanide', 'hemlock', 'poison'])

    result = replacement.replace(TEXT_TEST_STRING)
    captured = capsys.readouterr()

    assert TEXT_NOT_FOUND_MESSAGE in captured.out
    assert ENTER_VALID_TEXT_PROMPT in captured.out
    assert 'of poison I had drunk' in result
    assert 'hemlock' not in result


def test_replace_regex(simulate_input, capsys):
    """Test regular expression replacement and presence validation."""
    target_regex = r'(\d{3}),(\d{3})'
    replacement_str = 'Five hundred twenty-five thousand, six hundred'

    simulate_input([r'\d{4}', target_regex, replacement_str])

    result = replacement.replace_regex(REGEX_TEST_STRING)
    captured = capsys.readouterr()

    assert REGEX_NOT_FOUND_MESSAGE in captured.out
    assert ENTER_VALID_REGEX_PROMPT in captured.out
    assert result == 'Five hundred twenty-five thousand, six hundred minutes'
