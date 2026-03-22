"""Tests for command-line argument parsing."""

import sys
import pytest

from textwarp._cli.parsing import _calculate_max_arg_width, parse_args


def test_calculate_max_arg_width():
    """
    Test that the argument width calculation accounts for the prefix
    and padding.
    """
    dummy_map = {
        'short': (lambda x: x, 'help'),
        'a-very-long-argument-name': (lambda x: x, 'help')
    }

    assert _calculate_max_arg_width(dummy_map) == 31


def test_parse_args_valid_single_command(monkeypatch):
    """Test parsing a single valid command."""
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--camel-case'])
    pipeline, _ = parse_args()

    assert len(pipeline) == 1
    cmd_name, func = pipeline[0]
    assert cmd_name == 'camel-case'
    assert callable(func)


def test_parse_args_valid_pipeline(monkeypatch):
    """Test parsing multiple valid, non-conflicting commands."""
    monkeypatch.setattr(
        sys, 'argv', ['textwarp', '--strip', '--lowercase', '--snake-case']
    )
    pipeline, _ = parse_args()

    assert len(pipeline) == 3
    cmd_names = [cmd[0] for cmd in pipeline]
    assert cmd_names == ['strip', 'lowercase', 'snake-case']


def test_parse_args_no_args_prints_help(monkeypatch, capsys):
    """
    Test that running with no arguments in a terminal prints help and
    exits.
    """
    monkeypatch.setattr(sys, 'argv', ['textwarp'])
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)

    with pytest.raises(SystemExit) as excinfo:
        parse_args()

    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert 'usage: textwarp' in captured.err


def test_parse_args_conflicting_separators(monkeypatch, capsys):
    """
    Test that combining multiple separator commands raises an error.
    """
    monkeypatch.setattr(
        sys, 'argv', ['textwarp', '--camel-case', '--snake-case']
    )

    with pytest.raises(SystemExit) as excinfo:
        parse_args()

    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert 'Cannot combine multiple separator styles' in captured.err


def test_parse_args_conflicting_casings(monkeypatch, capsys):
    """Test that combining multiple casing commands raises an error."""
    monkeypatch.setattr(
        sys, 'argv', ['textwarp', '--lowercase', '--uppercase']
    )

    with pytest.raises(SystemExit) as excinfo:
        parse_args()

    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert 'Cannot combine multiple casing styles' in captured.err


def test_parse_args_mutually_exclusive_with_each_other(monkeypatch, capsys):
    """Test that mutually exclusive commands cannot be combined."""
    monkeypatch.setattr(
        sys, 'argv', ['textwarp', '--word-count', '--line-count']
    )

    with pytest.raises(SystemExit) as excinfo:
        parse_args()

    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert 'Cannot combine multiple exclusive commands' in captured.err


def test_parse_args_exclusive_with_formatting(monkeypatch, capsys):
    """
    Test that an exclusive command cannot be combined with standard
    formatting.
    """
    monkeypatch.setattr(
        sys, 'argv', ['textwarp', '--word-count', '--camel-case']
    )

    with pytest.raises(SystemExit) as excinfo:
        parse_args()

    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert (
        'cannot be combined with casing or separator commands' in captured.err
    )
