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
    IN_PLACE_ANALYSIS_ERROR_MSG,
    IN_PLACE_CONFLICT_ERROR_MSG,
    IN_PLACE_NO_FILES_ERROR_MSG,
    INVALID_CASE_ERROR_MSG,
    MULTIPLE_REPLACEMENT_ERROR_MSG,
    REGEX_EMPTY_ERROR_MSG,
    TEXT_EMPTY_ERROR_MSG,
    UNRECOGNIZED_CMD_ERROR_MSG,
    UNRECOGNIZED_CMD_HINT_ERROR_MSG
)
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


@pytest.mark.parametrize('valid_case', ['camel', 'snake case', 'PASCAL'])
def test_validate_case_name_valid(valid_case):
    validate_case_name(valid_case)


@pytest.mark.parametrize(
    'invalid_case, exception_class, error_msg',
    [
        ('', NoCaseNameError, CASE_EMPTY_ERROR_MSG),
        ('   ', WhitespaceCaseNameError, CASE_WHITESPACE_ERROR_MSG),
        ('Jarndyce and Jarndyce', InvalidCaseNameError, INVALID_CASE_ERROR_MSG)
    ]
)
def test_validate_case_name_invalid(invalid_case, exception_class, error_msg):
    with pytest.raises(exception_class, match=re.escape(error_msg)):
        validate_case_name(invalid_case)


def test_validate_clipboard_valid():
    validate_clipboard(
        'The knowledge and survey of vice is in this world so necessary to '
        'the constituting of human virtue.'
    )


@pytest.mark.parametrize(
    'invalid_clipboard, exception_class, error_msg',
    [
        ('', EmptyClipboardError, CLIPBOARD_EMPTY_ERROR_MSG),
        (
            '   \n \t  ',
            WhitespaceClipboardError,
            CLIPBOARD_WHITESPACE_ERROR_MSG
        )
    ]
)
def test_validate_clipboard_invalid(
    invalid_clipboard, exception_class, error_msg
):
    with pytest.raises(exception_class, match=re.escape(error_msg)):
        validate_clipboard(invalid_clipboard)


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


def test_validate_command_combinations_mutually_exclusive(capsys, cli_parser):
    args = argparse.Namespace(find=None, replace=None, markdown=False)
    active_cmds = ['clear', 'uppercase']

    with pytest.raises(SystemExit):
        validate_command_combinations(active_cmds, args, cli_parser)

    captured = capsys.readouterr()
    expected = f"Error: {EXCLUSIVE_CMD_ERROR_MSG.format(cmd='clear')}"
    assert expected in captured.err
    assert 'usage:' not in captured.err


def test_validate_command_combinations_multiple_replacements(
    capsys,
    cli_parser
):
    args = argparse.Namespace(find=None, replace=None, markdown=False)
    active_cmds = ['replace-text', 'replace-case']

    with pytest.raises(SystemExit):
        validate_command_combinations(active_cmds, args, cli_parser)

    captured = capsys.readouterr()
    expected_msg = MULTIPLE_REPLACEMENT_ERROR_MSG.format(
        commands='replace-text, replace-case'
    )
    assert f'Error: {expected_msg}' in captured.err
    assert 'usage:' not in captured.err


def test_validate_command_combinations_analysis_order(capsys, cli_parser):
    args = argparse.Namespace(find=None, replace=None, markdown=False)

    active_cmds_valid = ['uppercase', 'count-words', 'count-chars']
    validate_command_combinations(active_cmds_valid, args, cli_parser)

    active_cmds_invalid = ['count-words', 'uppercase']
    with pytest.raises(SystemExit):
        validate_command_combinations(active_cmds_invalid, args, cli_parser)

    captured = capsys.readouterr()
    expected = f"Error: {ANALYSIS_ORDER_ERROR_MSG.format(cmd='uppercase')}"
    assert expected in captured.err
    assert 'usage:' not in captured.err


def test_validate_command_combinations_stray_find_replace(capsys, cli_parser):
    args = argparse.Namespace(
        find='apple', replace='knowledge', markdown=False
    )
    active_cmds = ['uppercase']

    with pytest.raises(SystemExit):
        validate_command_combinations(active_cmds, args, cli_parser)

    captured = capsys.readouterr()
    assert f'Error: {FIND_REPLACE_ARG_ERROR_MSG}' in captured.err
    assert 'usage:' not in captured.err


@pytest.mark.parametrize(
    'active_cmds, output_file, input_files, expected_msg',
    [
        (['uppercase'], None, [], IN_PLACE_NO_FILES_ERROR_MSG),
        (
            ['uppercase'],
            '其出彌遠_其知彌少.txt',
            ['不出戶.txt', '知天下.txt'],
            IN_PLACE_CONFLICT_ERROR_MSG
        ),
        (
            ['count-words'],
            None,
            ['the_farther_one_travels.txt', 'the_less_one_knows.txt'],
            IN_PLACE_ANALYSIS_ERROR_MSG
        ),
    ]
)
def test_validate_command_combinations_in_place_errors(
    capsys,
    cli_parser,
    active_cmds,
    output_file,
    input_files,
    expected_msg
):
    args = argparse.Namespace(
        find=None, replace=None, in_place=True,
        output_file=output_file, copy_to_clipboard=False
    )

    with pytest.raises(SystemExit):
        validate_command_combinations(
            active_cmds, args, cli_parser, input_files=input_files
        )

    captured = capsys.readouterr()
    assert f'Error: {expected_msg}' in captured.err
    assert 'usage:' not in captured.err


@pytest.mark.parametrize(
    'active_cmds, positional_files, expected_msg',
    [
        (
            [],
            ['camelcase'],
            UNRECOGNIZED_CMD_HINT_ERROR_MSG.format(
                cmd='camelcase', match='camel-case'
            )
        ),
        (
            [],
            ['raphèl-mai-amècche-zabì-almi'],
            UNRECOGNIZED_CMD_ERROR_MSG.format(
                cmd='raphèl-mai-amècche-zabì-almi'
            )
        ),
        (
            ['uppercase'],
            ['button.txt', 'lowercase'],
            CMD_AFTER_FILE_ERROR_MSG.format(cmd='lowercase')
        ),
        (
            ['uppercase'],
            ['camelcase'],
            FILE_NOT_FOUND_CMD_HINT_ERROR_MSG.format(
                file='camelcase', match='camel-case'
            )
        ),
    ]
)
def test_validate_positional_args_errors(
    capsys, cli_parser, active_cmds, positional_files, expected_msg
):
    with pytest.raises(SystemExit):
        validate_positional_args(active_cmds, positional_files, cli_parser)

    captured = capsys.readouterr()
    assert f'Error: {expected_msg}' in captured.err
    assert 'usage:' not in captured.err
