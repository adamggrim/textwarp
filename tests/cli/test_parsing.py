"""Tests for command-line argument parsing."""

import sys
from importlib.metadata import PackageNotFoundError

import pytest

from textwarp._cli.parsing import parse_args


def test_parse_args_copy_flag_default_false(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--uppercase'])
    parsed_args = parse_args()

    assert parsed_args.copy_to_clipboard is False


def test_parse_args_copy_flag_long(monkeypatch):
    """
    Test that the long `--copy` flag sets `copy_to_clipboard` to `True`.
    """
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--snake-case', '--copy'])
    parsed_args = parse_args()

    assert parsed_args.copy_to_clipboard is True


def test_parse_args_copy_flag_short(monkeypatch):
    """
    Test that the short `-c` flag sets `copy_to_clipboard` to `True`.
    """
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--camel-case', '-c'])
    parsed_args = parse_args()

    assert parsed_args.copy_to_clipboard is True


def test_parse_args_lang_argument(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--camel-case', '-l', 'fr'])
    parsed_args = parse_args()

    assert len(parsed_args.pipeline) == 1
    assert parsed_args.pipeline[0][0] == 'camel-case'
    assert parsed_args.lang == 'fr'


def test_parse_args_lang_default(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--snake-case'])
    parsed_args = parse_args()

    assert parsed_args.lang == 'en'


def test_parse_args_no_args_prints_help(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['textwarp'])
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)

    with pytest.raises(SystemExit) as excinfo:
        parse_args()

    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert 'usage: textwarp' in captured.err


def test_parse_args_version_fallback(monkeypatch, capsys):
    """
    Test that the `--version` argument handles when the package metadata
    is not found.
    """
    def mock_version(pkg_name):
        raise PackageNotFoundError()

    monkeypatch.setattr('textwarp._cli.parsing.version', mock_version)
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--version'])

    with pytest.raises(SystemExit) as excinfo:
        parse_args()

    assert excinfo.value.code == 0

    captured = capsys.readouterr()
    assert 'unknown (not installed)' in captured.out
