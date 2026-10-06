"""Tests for replacement command functions."""

import pytest

from textwarp._cli import ui
from textwarp._cli.constants.messages import (
    ENTER_VALID_CASE_PROMPT,
    ENTER_VALID_REGEX_PROMPT,
    ENTER_VALID_TEXT_PROMPT
)
from textwarp._commands import replacement

CASE_TEST_TEXT = 'pascal_case'
REGEX_TEST_TEXT = 'Il ne fut même plus Jean Valjean; il fut le numéro 24601.'
TEXT_TEST_TEXT = (
    'My heart aches, and a drowsy numbness pains\n'
    'My sense, as though of hemlock I had drunk.'
)


def test_replace_case(simulate_input, capsys):
    simulate_input(['invalid_case', 'snake', 'pascal'])

    arg_to_replace, replacement_arg = ui.prompt_for_replacement_case()
    result = replacement.replace_case(
        CASE_TEST_TEXT,
        arg_to_replace,
        replacement_arg
    )
    captured = capsys.readouterr()

    assert ENTER_VALID_CASE_PROMPT in captured.out
    assert result == 'PascalCase'


def test_replace_case_not_found(simulate_input):
    simulate_input(['camel', 'snake'])

    arg_to_replace, replacement_arg = ui.prompt_for_replacement_case()
    result = replacement.replace_case(
        CASE_TEST_TEXT,
        arg_to_replace,
        replacement_arg
    )

    assert result == CASE_TEST_TEXT


def test_replace_case_early_exit(simulate_input):
    simulate_input(['quit'])

    with pytest.raises(SystemExit):
        ui.prompt_for_replacement_case()


def test_replace_regex(simulate_input, capsys):
    target_regex = r'\d{5}'
    replacement_str = 'vingt-quatre mille six cent un'

    simulate_input([r'[javert', target_regex, replacement_str])

    arg_to_replace, replacement_arg = ui.prompt_for_replacement_regex()
    result = replacement.replace_regex(
        REGEX_TEST_TEXT,
        arg_to_replace,
        replacement_arg
    )
    captured = capsys.readouterr()

    assert ENTER_VALID_REGEX_PROMPT in captured.out
    assert result == (
        'Il ne fut même plus Jean Valjean; il fut le numéro vingt-quatre '
        'mille six cent un.'
    )


def test_replace_regex_not_found(simulate_input):
    simulate_input([r'\d{6}', 'Monsieur Madeleine'])

    arg_to_replace, replacement_arg = ui.prompt_for_replacement_regex()
    result = replacement.replace_regex(
        REGEX_TEST_TEXT,
        arg_to_replace,
        replacement_arg
    )

    assert result == REGEX_TEST_TEXT


def test_replace_text(simulate_input, capsys):
    simulate_input(['', 'hemlock', 'coffee'])

    arg_to_replace, replacement_arg = ui.prompt_for_replacement_text()
    result = replacement.replace_text(
        TEXT_TEST_TEXT,
        arg_to_replace,
        replacement_arg
    )
    captured = capsys.readouterr()

    assert ENTER_VALID_TEXT_PROMPT in captured.out
    assert 'of coffee I had drunk' in result
    assert 'hemlock' not in result


def test_replace_text_not_found(simulate_input):
    simulate_input(['cyanide', 'coffee'])

    arg_to_replace, replacement_arg = ui.prompt_for_replacement_text()
    result = replacement.replace_text(
        TEXT_TEST_TEXT,
        arg_to_replace,
        replacement_arg
    )

    assert result == TEXT_TEST_TEXT


def test_parse_cli_escapes():
    raw_input = (
        r'(Life and Contacts)\n'
        r'\t“Vocat aestus in umbram”\n'
        r'\t\tNemesianus Ec. IV.\r \\'
    )
    expected_output = (
        '(Life and Contacts)\n'
        '\t“Vocat aestus in umbram”\n'
        '\t\tNemesianus Ec. IV.\r \\'
    )

    assert replacement.parse_cli_escapes(raw_input) == expected_output


def test_replace_regex_with_escapes(simulate_input):
    target_regex = r'(.+)\s(\w+)$'
    replacement_str = r'\2, \1\n'

    simulate_input([target_regex, replacement_str])

    arg_to_replace, replacement_arg = ui.prompt_for_replacement_regex()
    result = replacement.replace_regex(
        'Hugh Selwyn Mauberley',
        arg_to_replace,
        replacement_arg
    )

    assert result == 'Mauberley, Hugh Selwyn\n'


def test_replace_text_with_escapes(simulate_input):
    text_to_replace = ' / '
    replacement_str = r'\n'

    simulate_input([text_to_replace, replacement_str])

    arg_to_replace, replacement_arg = ui.prompt_for_replacement_text()
    result = replacement.replace_text(
        'Beneath half-watt rays / The eyes turn topaz.',
        arg_to_replace,
        replacement_arg
    )

    assert result == 'Beneath half-watt rays\nThe eyes turn topaz.'
