"""Tests for command-line runner logic and clipboard interaction."""

from unittest.mock import MagicMock

import pyperclip

from tests.helpers import normalize_output
from textwarp._cli.runners import (
    _paste_and_validate,
    _replace_and_copy,
    clear_clipboard,
    replace_text,
    run_command_loop,
    warp_and_copy
)
from textwarp._cli.constants.messages import (
    CLIPBOARD_ACCESS_ERROR_MSG,
    CLIPBOARD_CLEARED_MSG,
    CLIPBOARD_EMPTY_ERROR_MSG,
    LINUX_XCLIP_WARNING_MSG,
    MODIFIED_TEXT_COPIED_MSG
)

def test_paste_and_validate(mock_clipboard):
    expected = (
        'The only limit to the height of your achievements is the reach of '
        'your dreams and your willingness to work for them.'
    )
    mock_clipboard.copy(expected)
    result = _paste_and_validate()

    assert result == expected


def test_paste_and_validate_empty(mock_clipboard, capsys):
    mock_clipboard.copy('')
    assert _paste_and_validate() is None

    captured = capsys.readouterr()
    assert CLIPBOARD_EMPTY_ERROR_MSG in captured.out


def test_paste_and_validate_pyperclip_exception(monkeypatch, capsys):
    mock_paste = MagicMock(
        side_effect=pyperclip.PyperclipException('xclip or xsel not found')
    )

    monkeypatch.setattr(pyperclip, 'paste', mock_paste)

    assert _paste_and_validate() is None
    captured = capsys.readouterr()

    normalized_out = normalize_output(captured.out)
    expected_error = normalize_output(CLIPBOARD_ACCESS_ERROR_MSG)
    expected_warning = normalize_output(LINUX_XCLIP_WARNING_MSG)

    assert expected_error in normalized_out
    assert expected_warning in normalized_out
    mock_paste.assert_called_once()


def test_clear_clipboard(mock_clipboard, capsys):
    mock_clipboard.copy('The Family Shakespeare')
    clear_clipboard()

    assert mock_clipboard.paste() == ''
    captured = capsys.readouterr()
    assert CLIPBOARD_CLEARED_MSG in captured.out


def test_warp_and_copy(mock_clipboard, capsys):
    warp_and_copy(str.upper, 'kilroy')

    assert mock_clipboard.paste() == 'KILROY'
    captured = capsys.readouterr()
    assert MODIFIED_TEXT_COPIED_MSG in captured.out


def test_replace_and_copy_success(mock_clipboard, capsys):
    def dummy_replace(text):
        return text.replace('Evermore', 'Nevermore')

    _replace_and_copy(dummy_replace, 'Evermore.')

    assert mock_clipboard.paste() == 'Nevermore.'
    captured = capsys.readouterr()
    assert MODIFIED_TEXT_COPIED_MSG in captured.out


def test_replace_and_copy_not_found(mock_clipboard, capsys):
    def dummy_replace(text):
        return text

    quote = ('There is no there there.')

    mock_clipboard.copy(quote)
    _replace_and_copy(dummy_replace, quote)

    assert mock_clipboard.paste() == quote
    captured = capsys.readouterr()
    assert MODIFIED_TEXT_COPIED_MSG in captured.out


def test_run_command_loop(monkeypatch, mock_clipboard):
    mock_clipboard.copy('Tomorrow, and tomorrow, and tomorrow')

    monkeypatch.setattr('textwarp._cli.runners.get_input', lambda: False)

    mock_command = MagicMock()

    run_command_loop(mock_command)

    mock_command.assert_called_once_with(
        'Tomorrow, and tomorrow, and tomorrow'
    )


def test_replace_text_lookup(monkeypatch):
    mock_run_command_loop = MagicMock()

    monkeypatch.setattr(
        'textwarp._cli.runners.run_command_loop',
        mock_run_command_loop
    )

    monkeypatch.setattr(
        'textwarp._cli.ui.prompt_for_replacement_case',
        lambda: ('camel', 'snake')
    )

    replace_text('replace_case')

    mock_run_command_loop.assert_called_once()
