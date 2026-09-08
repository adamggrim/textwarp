"""Tests for the entry point of the package."""

import sys
from unittest.mock import MagicMock

import pytest

from textwarp import __main__
from textwarp._cli.args import ARGS_MAP
from textwarp._cli.parsing import ParsedArgs


def test_cli_version(capsys, monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--version'])

    with pytest.raises(SystemExit) as exc:
        __main__.main()

    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert 'textwarp' in captured.out


def test_main_keyboard_interrupt(monkeypatch):
    def mock_parse_args():
        raise KeyboardInterrupt()

    monkeypatch.setattr(__main__, 'parse_args', mock_parse_args)

    mock_program_exit = MagicMock()

    monkeypatch.setattr(__main__, 'print_padding', lambda: None)
    monkeypatch.setattr(__main__, 'program_exit', mock_program_exit)

    __main__.main()

    mock_program_exit.assert_called_once()


def test_main_sets_locale(monkeypatch):
    mock_args = ParsedArgs(
        pipeline=[ARGS_MAP['clear']],
        lang='en',
        input_files=[],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=False,
        debug=False
    )

    mock_parse_args = MagicMock(return_value=mock_args)
    monkeypatch.setattr(__main__, 'parse_args', mock_parse_args)

    mock_process_file = MagicMock()
    mock_process_piped = MagicMock()
    mock_process_interactive = MagicMock()

    monkeypatch.setattr(__main__, 'process_file_mode', mock_process_file)
    monkeypatch.setattr(__main__, 'process_piped_mode', mock_process_piped)
    monkeypatch.setattr(
        __main__, 'process_interactive_mode', mock_process_interactive
    )
    monkeypatch.setattr(sys.stdin, 'isatty', MagicMock(return_value=True))

    __main__.main()

    from textwarp._core.context import ctx
    assert ctx.locale == 'en'
    mock_process_interactive.assert_called_once_with(mock_args)
    mock_process_file.assert_not_called()
    mock_process_piped.assert_not_called()


def test_main_global_exception_handler(monkeypatch, capsys):
    mock_parse_args = MagicMock(
        side_effect=ValueError('Unexpected configuration error')
    )
    monkeypatch.setattr(__main__, 'parse_args', mock_parse_args)

    with pytest.raises(SystemExit) as excinfo:
        __main__.main()

    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert 'Unexpected configuration error' in captured.out


def test_main_global_exception_handler_debug_mode(monkeypatch):
    mock_args = ParsedArgs(
        pipeline=[ARGS_MAP['lowercase']],
        lang='en',
        input_files=['dummy.txt'],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=False,
        debug=True
    )

    mock_parse_args = MagicMock(return_value=mock_args)
    monkeypatch.setattr(__main__, 'parse_args', mock_parse_args)

    mock_process_file = MagicMock(
        side_effect=ValueError('Detailed debug error')
    )
    monkeypatch.setattr(__main__, 'process_file_mode', mock_process_file)

    with pytest.raises(ValueError, match='Detailed debug error'):
        __main__.main()
