"""Tests for the entry point of the package."""

import sys

import pytest

from textwarp import __main__
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

    exit_called = False
    def mock_program_exit():
        nonlocal exit_called
        exit_called = True

    monkeypatch.setattr(__main__, 'print_padding', lambda: None)
    monkeypatch.setattr(__main__, 'program_exit', mock_program_exit)

    __main__.main()

    assert exit_called is True


def test_main_sets_locale(monkeypatch):
    """
    Test that `main` extracts the language code from `parse_args` and
    applies it to the global context.
    """
    def mock_parse_args():
        return ParsedArgs(
            pipeline=[('clear', lambda x: x)],
            lang='en',
            input_files=[],
            output_file=None,
            markdown=False,
            find=None,
            replace=None,
            copy_to_clipboard=False,
            debug=False
        )

    monkeypatch.setattr(__main__, 'parse_args', mock_parse_args)

    # Mock the routing functions inside __main__.
    monkeypatch.setattr(__main__, 'process_file_mode', lambda args: None)
    monkeypatch.setattr(__main__, 'process_piped_mode', lambda args: None)
    monkeypatch.setattr(
        __main__, 'process_interactive_mode', lambda args: None
    )

    __main__.main()

    from textwarp._core.context import ctx
    assert ctx.locale == 'en'


def test_main_global_exception_handler(monkeypatch, capsys):
    def mock_parse_args():
        raise ValueError('Unexpected configuration error')

    monkeypatch.setattr(__main__, 'parse_args', mock_parse_args)

    with pytest.raises(SystemExit) as excinfo:
        __main__.main()

    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert 'Unexpected configuration error' in captured.out


def test_main_global_exception_handler_debug_mode(monkeypatch):
    def mock_parse_args():
        return ParsedArgs(
            pipeline=[('lowercase', lambda x: x)],
            lang='en',
            input_files=['dummy.txt'],
            output_file=None,
            markdown=False,
            find=None,
            replace=None,
            copy_to_clipboard=False,
            debug=True
        )

    def mock_process_file_mode(args):
        raise ValueError('Detailed debug error')

    monkeypatch.setattr(__main__, 'parse_args', mock_parse_args)
    monkeypatch.setattr(__main__, 'process_file_mode', mock_process_file_mode)

    with pytest.raises(ValueError, match='Detailed debug error'):
        __main__.main()
