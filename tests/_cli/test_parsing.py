import sys
from importlib.metadata import PackageNotFoundError
from unittest.mock import MagicMock

import pytest

from textwarp._cli.parsing import parse_args


def test_parse_args_copy_flag_default_false(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['textwarp', 'uppercase'])
    parsed_args = parse_args()

    assert parsed_args.copy_to_clipboard is False


def test_parse_args_copy_flag_long(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['textwarp', 'snake-case', '--copy'])
    parsed_args = parse_args()

    assert parsed_args.copy_to_clipboard is True


def test_parse_args_copy_flag_short(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['textwarp', 'camel-case', '-c'])
    parsed_args = parse_args()

    assert parsed_args.copy_to_clipboard is True


@pytest.mark.parametrize('flag', ['--in-place', '-i'])
def test_parse_args_in_place_flag(monkeypatch, tmp_path, flag):
    test_file = tmp_path / 'red_queen.txt'
    test_file.write_text(
        'Now, here, you see, it takes all the running you can do, to keep in '
        'the same place.',
        encoding='utf-8'
    )
    monkeypatch.setattr(
        sys, 'argv', ['textwarp', flag, 'uppercase', str(test_file)]
    )
    parsed_args = parse_args()

    assert parsed_args.in_place is True


def test_parse_args_lang_argument(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['textwarp', 'camel-case', '-l', 'fr'])
    parsed_args = parse_args()

    assert len(parsed_args.pipeline) == 1
    assert parsed_args.pipeline[0].name == 'camel-case'
    assert parsed_args.lang == 'fr'


def test_parse_args_lang_default(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['textwarp', 'snake-case'])
    parsed_args = parse_args()

    assert parsed_args.lang == 'en'


def test_parse_args_once_flag_default_false(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['textwarp', 'uppercase'])
    parsed_args = parse_args()

    assert parsed_args.once is False


@pytest.mark.parametrize('flag', ['--once', '-1'])
def test_parse_args_once_flag(monkeypatch, flag):
    monkeypatch.setattr(sys, 'argv', ['textwarp', flag, 'uppercase'])
    parsed_args = parse_args()

    assert parsed_args.once is True


def test_parse_args_no_args_prints_help(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['textwarp'])
    monkeypatch.setattr(sys.stdin, 'isatty', MagicMock(return_value=True))

    with pytest.raises(SystemExit) as excinfo:
        parse_args()

    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert 'usage: textwarp' in captured.err


def test_parse_args_version_fallback(monkeypatch, capsys):
    mock_version = MagicMock(side_effect=PackageNotFoundError)

    monkeypatch.setattr('textwarp._cli.parsing.version', mock_version)
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--version'])

    with pytest.raises(SystemExit) as excinfo:
        parse_args()

    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert 'unknown (not installed)' in captured.out
