"""Tests for execution modes and pipeline processing."""

import sys

import pytest

from textwarp._cli import processing
from textwarp._cli.parsing import ParsedArgs


def _dummy_lower(text: str) -> str:
    """Convert text to lowercase for testing."""
    return text.lower()


def test_process_file_mode_binary_file(tmp_path, capsys):
    """Test that file mode handles binary and undecodable files."""
    binary_file = tmp_path / 'image.png'
    binary_file.write_bytes(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')

    pipeline = [('uppercase', str.upper)]

    args = ParsedArgs(
        pipeline=pipeline,
        lang='en',
        input_files=[str(binary_file)],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=False,
        debug=False
    )

    with pytest.raises(SystemExit) as excinfo:
        processing.process_file_mode(args)

    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert 'binary file' in captured.out.replace('\n', ' ')


def test_process_file_mode_file_not_found(capsys):
    """
    Test that file mode handles missing files gracefully by exiting.
    """
    pipeline = [('uppercase', str.upper)]

    args = ParsedArgs(
        pipeline=pipeline,
        lang='en',
        input_files=['does_not_exist.txt'],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=False,
        debug=False
    )

    with pytest.raises(SystemExit) as excinfo:
        processing.process_file_mode(args)

    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert 'Error accessing file' in captured.out


def test_process_file_mode_success(tmp_path, capsys):
    """Test reading from an input file and writing to an output file."""
    input_file = tmp_path / 'input.txt'
    input_file.write_text('file content', encoding='utf-8')
    output_file = tmp_path / 'output.txt'

    pipeline = [('uppercase', str.upper)]

    args = ParsedArgs(
        pipeline=pipeline,
        lang='en',
        input_files=[str(input_file)],
        output_file=str(output_file),
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=False,
        debug=False
    )

    processing.process_file_mode(args)

    assert output_file.read_text(encoding='utf-8') == 'FILE CONTENT'
    captured = capsys.readouterr()
    assert 'successfully written' in captured.out


def test_process_interactive_mode_replacement(monkeypatch):
    """
    Test that replacement commands branch correctly in interactive mode
    and exit.
    """
    replace_called = False

    def mock_replace_text(cmd_name):
        nonlocal replace_called
        replace_called = True
        assert cmd_name == 'replace_case'

    monkeypatch.setattr(processing, 'replace_text', mock_replace_text)

    monkeypatch.setattr(processing, 'program_exit', lambda: sys.exit(0))

    args = ParsedArgs(
        pipeline=[('replace-case', lambda x: x)],
        lang='en',
        input_files=[],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=False,
        debug=False
    )

    with pytest.raises(SystemExit):
        processing.process_interactive_mode(args)

    assert replace_called is True


def test_process_piped_mode_copy_flag(
    monkeypatch,
    mock_clipboard,
    capsys
):
    """
    Test that when `copy_to_clipboard` is `True` in piped mode, the
    clipboard receives the modified text and a confirmation message
    prints to the console.
    """
    monkeypatch.setattr(sys.stdin, 'read', lambda: 'piped text\n')

    pipeline = [('uppercase', str.upper)]

    args = ParsedArgs(
        pipeline=pipeline,
        lang='en',
        input_files=[],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=True,
        debug=False
    )

    processing.process_piped_mode(args)

    assert mock_clipboard.paste() == 'PIPED TEXT'

    captured = capsys.readouterr()
    assert 'Modified text copied to clipboard.' in captured.out


def test_process_piped_mode_warping(monkeypatch, capsys):
    """
    Test that piped mode reads from stdin and runs `warp_and_copy`.
    """
    monkeypatch.setattr(sys.stdin, 'read', lambda: 'Piped text\n')

    args = ParsedArgs(
        pipeline=[('lowercase', _dummy_lower)],
        lang='en',
        input_files=[],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=False,
        debug=False
    )

    processing.process_piped_mode(args)

    captured = capsys.readouterr()
    assert 'piped text' in captured.out
