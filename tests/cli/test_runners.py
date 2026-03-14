"""Tests for command-line runner logic and clipboard interaction."""

import pyperclip

from textwarp._cli.runners import (
    _paste_and_validate,
    _replace_and_copy,
    clear_clipboard,
    replace_text,
    run_command_loop,
    warp_and_copy
)
from textwarp._cli.constants.messages import (
    CLIPBOARD_ACCESS_ERROR_MESSAGE,
    CLIPBOARD_CLEARED_MESSAGE,
    MODIFIED_TEXT_COPIED_MESSAGE
)


def test_paste_and_validate_success(mock_clipboard):
    """Test successful pasting and validation of clipboard text."""
    mock_clipboard.copy('Valid text')
    assert _paste_and_validate() == 'Valid text'


def test_paste_and_validate_empty(mock_clipboard, capsys):
    """Test pasting an empty clipboard."""
    mock_clipboard.copy('')
    assert _paste_and_validate() is None

    captured = capsys.readouterr()
    assert 'Clipboard is empty.' in captured.out


def test_paste_and_validate_pyperclip_exception(monkeypatch, capsys):
    """Test handling of clipboard access errors."""
    def mock_paste():
        raise pyperclip.PyperclipException('xclip or xsel not found')

    monkeypatch.setattr(pyperclip, 'paste', mock_paste)

    assert _paste_and_validate() is None
    captured = capsys.readouterr()
    assert CLIPBOARD_ACCESS_ERROR_MESSAGE in captured.out
    assert 'sudo apt install xclip' in captured.out


def test_clear_clipboard(mock_clipboard, capsys):
    """Test clearing the clipboard contents."""
    mock_clipboard.copy('The Family Shakespeare')
    clear_clipboard()

    assert mock_clipboard.paste() == ''
    captured = capsys.readouterr()
    assert CLIPBOARD_CLEARED_MESSAGE in captured.out


def test_warp_and_copy(mock_clipboard, capsys):
    """Test transforming text and copying it back to the clipboard."""
    warp_and_copy(str.upper, 'kilroy')

    assert mock_clipboard.paste() == 'KILROY'
    captured = capsys.readouterr()
    assert MODIFIED_TEXT_COPIED_MESSAGE in captured.out


def test_replace_and_copy_success(mock_clipboard, capsys):
    """
    Test replacement command successfully finding and modifying text.
    """
    def dummy_replace(text):
        return text.replace('Evermore', 'Nevermore')

    _replace_and_copy(dummy_replace, 'Evermore.')

    assert mock_clipboard.paste() == 'Nevermore.'
    captured = capsys.readouterr()
    assert MODIFIED_TEXT_COPIED_MESSAGE in captured.out


def test_replace_and_copy_not_found(mock_clipboard, capsys):
    """Test replacement command when target is not found."""
    def dummy_replace(text):
        return text

    quote = (
        "Sometimes I’ve believed as many as six impossible things before "
        "breakfast."
    )

    mock_clipboard.copy(quote)
    _replace_and_copy(dummy_replace, quote)

    assert mock_clipboard.paste() == quote
    captured = capsys.readouterr()
    assert MODIFIED_TEXT_COPIED_MESSAGE in captured.out


def test_run_command_loop(monkeypatch, mock_clipboard):
    """
    Test the main command loop executes correctly and breaks when
    requested.
    """
    mock_clipboard.copy('Tomorrow, and tomorrow, and tomorrow')

    monkeypatch.setattr('textwarp._cli.runners.get_input', lambda: False)

    executed = False
    def dummy_command(text):
        nonlocal executed
        executed = True
        assert text == 'Tomorrow, and tomorrow, and tomorrow'
        return text

    run_command_loop(dummy_command)
    assert executed is True


def test_replace_text_lookup(monkeypatch):
    """
    Test that replace_text retrieves the replacement function and
    enters the loop.
    """
    loop_called = False

    def mock_run_command_loop(command_func, action_handler):
        nonlocal loop_called
        loop_called = True
        assert callable(command_func)
        assert action_handler == _replace_and_copy

    monkeypatch.setattr(
        'textwarp._cli.runners.run_command_loop',
        mock_run_command_loop
    )

    replace_text('replace_case')
    assert loop_called is True
