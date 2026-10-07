"""Tests for CLI input and clipboard validation."""

import argparse

import pytest
import regex as re

from textwarp._cli.constants.messages import (
    ANALYSIS_ORDER_ERROR_MSG,
    CASE_EMPTY_ERROR_MSG,
    CASE_WHITESPACE_ERROR_MSG,
    CLIPBOARD_EMPTY_ERROR_MSG,
    CLIPBOARD_WHITESPACE_ERROR_MSG,
    CMD_AFTER_FILE_ERROR_MSG,
    EXCLUSIVE_CMD_ERROR_MSG,
    FILE_NOT_FOUND_CMD_HINT_ERROR_MSG,
    FIND_REPLACE_ARG_ERROR_MSG,
    INVALID_CASE_ERROR_MSG,
    MULTIPLE_REPLACEMENT_ERROR_MSG,
    REGEX_EMPTY_ERROR_MSG,
    TEXT_EMPTY_ERROR_MSG,
    UNRECOGNIZED_CMD_ERROR_MSG,
    UNRECOGNIZED_CMD_HINT_ERROR_MSG
)
from textwarp._cli.parsing import TextwarpArgumentParser
from textwarp._cli.validation import (
    validate_case_name,
    validate_clipboard,
    validate_command_combinations,
    validate_positional_args,
    validate_regex,
    validate_text
)
from textwarp._core.exceptions import (
    EmptyClipboardError,
    InvalidCaseNameError,
    InvalidRegexError,
    NoCaseNameError,
    NoRegexError,
    NoTextError,
    WhitespaceCaseNameError,
    WhitespaceClipboardError
)


def test_validate_case_name():
    validate_case_name('camel')
    validate_case_name('snake case')
    validate_case_name('PASCAL')

    with pytest.raises(NoCaseNameError, match=re.escape(CASE_EMPTY_ERROR_MSG)):
        validate_case_name('')

    with pytest.raises(
        WhitespaceCaseNameError,
        match=re.escape(CASE_WHITESPACE_ERROR_MSG)
    ):
        validate_case_name('   ')

    with pytest.raises(
        InvalidCaseNameError,
        match=re.escape(INVALID_CASE_ERROR_MSG)
    ):
        validate_case_name('Jarndyce and Jarndyce')


def test_validate_clipboard():
    validate_clipboard(
        'The knowledge and survey of vice is in this world so necessary to '
        'the constituting of human virtue.'
    )

    with pytest.raises(
        EmptyClipboardError,
        match=re.escape(CLIPBOARD_EMPTY_ERROR_MSG)
    ):
        validate_clipboard('')

    with pytest.raises(
        WhitespaceClipboardError,
        match=re.escape(CLIPBOARD_WHITESPACE_ERROR_MSG)
    ):
        validate_clipboard('   \n \t  ')


def test_validate_regex():
    validate_regex(r'^(\w)(?:(?1)|\w?)\1$')
    validate_regex(r'(?<=madeleine)À la recherche du temps perdu')

    with pytest.raises(NoRegexError, match=re.escape(REGEX_EMPTY_ERROR_MSG)):
        validate_regex('')

    with pytest.raises(InvalidRegexError):
        validate_regex(r'[They do not move')


def test_validate_text():
    validate_text('Truth will out.')
    validate_text(' ')

    with pytest.raises(NoTextError, match=re.escape(TEXT_EMPTY_ERROR_MSG)):
        validate_text('')


def test_validate_command_combinations_mutually_exclusive(capsys):
    parser = TextwarpArgumentParser()
    args = argparse.Namespace(find=None, replace=None, markdown=False)
    active_cmds = ['clear', 'uppercase']

    with pytest.raises(SystemExit):
        validate_command_combinations(active_cmds, args, parser)

    captured = capsys.readouterr()
    expected = f"Error: {EXCLUSIVE_CMD_ERROR_MSG.format(cmd='clear')}"
    assert expected in captured.err
    assert 'usage:' not in captured.err


def test_validate_command_combinations_multiple_replacements(capsys):
    parser = TextwarpArgumentParser()
    args = argparse.Namespace(find=None, replace=None, markdown=False)
    active_cmds = ['replace-text', 'replace-case']

    with pytest.raises(SystemExit):
        validate_command_combinations(active_cmds, args, parser)

    captured = capsys.readouterr()
    expected_msg = MULTIPLE_REPLACEMENT_ERROR_MSG.format(
        commands='replace-text, replace-case'
    )
    assert f'Error: {expected_msg}' in captured.err
    assert 'usage:' not in captured.err


def test_validate_command_combinations_analysis_order(capsys):
    parser = TextwarpArgumentParser()
    args = argparse.Namespace(find=None, replace=None, markdown=False)

    active_cmds_valid = ['uppercase', 'word-count', 'char-count']
    validate_command_combinations(active_cmds_valid, args, parser)

    active_cmds_invalid = ['word-count', 'uppercase']
    with pytest.raises(SystemExit):
        validate_command_combinations(active_cmds_invalid, args, parser)

    captured = capsys.readouterr()
    expected = f"Error: {ANALYSIS_ORDER_ERROR_MSG.format(cmd='uppercase')}"
    assert expected in captured.err
    assert 'usage:' not in captured.err


def test_validate_command_combinations_stray_find_replace(capsys):
    parser = TextwarpArgumentParser()
    args = argparse.Namespace(
        find='apple', replace='knowledge', markdown=False
    )
    active_cmds = ['uppercase']

    with pytest.raises(SystemExit):
        validate_command_combinations(active_cmds, args, parser)

    captured = capsys.readouterr()
    assert f'Error: {FIND_REPLACE_ARG_ERROR_MSG}' in captured.err
    assert 'usage:' not in captured.err


def test_validate_positional_args_unrecognized_cmd(capsys):
    parser = TextwarpArgumentParser()

    with pytest.raises(SystemExit):
        validate_positional_args([], ['camelcase'], parser)

    captured = capsys.readouterr()
    expected_msg = UNRECOGNIZED_CMD_HINT_ERROR_MSG.format(
        cmd='camelcase', match='camel-case'
    )
    assert f'Error: {expected_msg}' in captured.err
    assert 'usage:' not in captured.err


def test_validate_positional_args_unrecognized_cmd_no_hint(capsys):
    parser = TextwarpArgumentParser()

    with pytest.raises(SystemExit):
        validate_positional_args([], ['raphèl-mai-amècche-zabì-almi'], parser)

    captured = capsys.readouterr()
    expected_msg = UNRECOGNIZED_CMD_ERROR_MSG.format(
        cmd='raphèl-mai-amècche-zabì-almi'
    )
    assert f'Error: {expected_msg}' in captured.err
    assert 'usage:' not in captured.err


def test_validate_positional_args_cmd_after_file(capsys):
    parser = TextwarpArgumentParser()

    with pytest.raises(SystemExit):
        validate_positional_args(
            ['uppercase'], ['button.txt', 'lowercase'], parser
        )

    captured = capsys.readouterr()
    expected_msg = CMD_AFTER_FILE_ERROR_MSG.format(cmd='lowercase')
    assert f'Error: {expected_msg}' in captured.err
    assert 'usage:' not in captured.err


def test_validate_positional_args_file_not_found_cmd_hint(capsys):
    parser = TextwarpArgumentParser()

    with pytest.raises(SystemExit):
        validate_positional_args(
            ['uppercase'], ['camelcase'], parser
        )

    captured = capsys.readouterr()
    expected_msg = FILE_NOT_FOUND_CMD_HINT_ERROR_MSG.format(
        file='camelcase', match='camel-case'
    )
    assert f'Error: {expected_msg}' in captured.err
    assert 'usage:' not in captured.err
