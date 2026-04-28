"""Tests for command-line argument parsing."""

import sys
from importlib.metadata import PackageNotFoundError

import pytest

from textwarp._cli.parsing import parse_args


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


def test_parse_args_copy_flag_default_false(monkeypatch):
    """
    Test that `copy_to_clipboard` defaults to `False` when omitted.
    """
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


def test_parse_args_find_replace_without_replacement_cmd(monkeypatch, capsys):
    """
    Test that `--find` or `--replace` without a replacement command
    raises an error.
    """
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--uppercase', '-f', 'text'])

    with pytest.raises(SystemExit) as excinfo:
        parse_args()

    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert (
        'The --find (-f) and --replace (-r) arguments can only be used'
        in captured.err
    )


def test_parse_args_lang_argument(monkeypatch):
    """Test parsing a specific language argument."""
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--camel-case', '-l', 'fr'])
    parsed_args = parse_args()

    assert len(parsed_args.pipeline) == 1
    assert parsed_args.pipeline[0][0] == 'camel-case'
    assert parsed_args.lang == 'fr'


def test_parse_args_lang_default(monkeypatch):
    """Test that the language argument defaults to `en` when omitted."""
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--snake-case'])
    parsed_args = parse_args()

    assert parsed_args.lang == 'en'


def test_parse_args_markdown_with_separators(monkeypatch, capsys):
    """Test that `--markdown` cannot be combined with separator commands."""
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--snake-case', '--markdown'])

    with pytest.raises(SystemExit) as excinfo:
        parse_args()

    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert (
        'The --markdown flag cannot be combined with manual separator commands'
        in captured.err
    )


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


def test_parse_args_valid_pipeline(monkeypatch):
    """Test parsing multiple valid, non-conflicting commands."""
    monkeypatch.setattr(
        sys, 'argv', ['textwarp', '--strip', '--lowercase', '--snake-case']
    )
    parsed_args = parse_args()

    assert len(parsed_args.pipeline) == 3
    cmd_names = [cmd[0] for cmd in parsed_args.pipeline]
    assert cmd_names == ['strip', 'lowercase', 'snake-case']


def test_parse_args_valid_single_command(monkeypatch):
    """Test parsing a single valid command."""
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--camel-case'])
    parsed_args = parse_args()

    assert len(parsed_args.pipeline) == 1
    cmd_name, func = parsed_args.pipeline[0]
    assert cmd_name == 'camel-case'
    assert callable(func)


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
