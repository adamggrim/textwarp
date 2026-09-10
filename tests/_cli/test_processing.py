"""Tests for execution modes and pipeline processing."""

from unittest.mock import MagicMock

import pexpect
import sys

import pytest
import regex as re

from tests.helpers import normalize_output
from textwarp._cli import processing
from textwarp._cli.args import ARGS_MAP
from textwarp._cli.constants.messages import (
    BINARY_FILE_ERROR_MSG,
    FILE_WRITE_SUCCESS_MSG,
    MODIFIED_TEXT_COPIED_MSG
)
from textwarp._cli.parsing import DEFAULT_MAX_FILE_MB, ParsedArgs
from textwarp._core.exceptions import TextwarpError


@pytest.fixture
def mock_oversized_file(monkeypatch):
    oversized_bytes = (DEFAULT_MAX_FILE_MB + 1) * 1024 * 1024
    monkeypatch.setattr('os.path.getsize', lambda _: oversized_bytes)


def test_process_file_mode_binary_file(tmp_path):
    binary_file = tmp_path / 'image.png'
    binary_file.write_bytes(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')

    pipeline = [ARGS_MAP['uppercase']]

    args = ParsedArgs(
        pipeline=pipeline,
        lang='en',
        input_files=[str(binary_file)],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=False,
        debug=False,
        max_file_mb=DEFAULT_MAX_FILE_MB
    )

    expected_msg = BINARY_FILE_ERROR_MSG.format(input_file=str(binary_file))

    with pytest.raises(TextwarpError, match=re.escape(expected_msg)):
        processing.process_file_mode(args)


def test_process_file_mode_file_not_found():
    pipeline = [ARGS_MAP['uppercase']]

    args = ParsedArgs(
        pipeline=pipeline,
        lang='en',
        input_files=['does_not_exist.txt'],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=False,
        debug=False,
        max_file_mb=DEFAULT_MAX_FILE_MB
    )

    with pytest.raises(TextwarpError, match='Error accessing file'):
        processing.process_file_mode(args)


@pytest.mark.usefixtures('mock_oversized_file')
def test_process_file_mode_oversized_file_warning(
    tmp_path,
    capsys
):
    input_file = tmp_path / 'input.txt'
    input_file.write_text('content', encoding='utf-8')

    args = ParsedArgs(
        pipeline=[ARGS_MAP['uppercase']],
        lang='en',
        input_files=[str(input_file)],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=True,
        debug=False,
        max_file_mb=DEFAULT_MAX_FILE_MB
    )

    processing.process_file_mode(args)

    captured = capsys.readouterr()
    assert 'Warning: Error accessing file' in captured.out
    assert 'File exceeds' in captured.out


@pytest.mark.usefixtures('mock_oversized_file')
def test_process_file_mode_oversized_regex_routing(
    tmp_path,
    monkeypatch,
):
    input_file = tmp_path / 'input.txt'
    input_file.write_text('content', encoding='utf-8')

    args = ParsedArgs(
        pipeline=[ARGS_MAP['replace-regex']],
        lang='en',
        input_files=[str(input_file)],
        output_file=None,
        markdown=False,
        find='foo',
        replace='bar',
        copy_to_clipboard=False,
        debug=False,
        max_file_mb=DEFAULT_MAX_FILE_MB
    )

    mock_mmap_regex = MagicMock()
    monkeypatch.setattr(processing, '_process_mmap_regex', mock_mmap_regex)

    processing.process_file_mode(args)

    mock_mmap_regex.assert_called_once_with(str(input_file), args)


def test_process_file_mode_success(tmp_path, capsys):
    input_file = tmp_path / 'input.txt'
    input_file.write_text('file content', encoding='utf-8')
    output_file = tmp_path / 'output.txt'

    pipeline = [ARGS_MAP['uppercase']]

    args = ParsedArgs(
        pipeline=pipeline,
        lang='en',
        input_files=[str(input_file)],
        output_file=str(output_file),
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=False,
        debug=False,
        max_file_mb=DEFAULT_MAX_FILE_MB
    )

    processing.process_file_mode(args)

    assert output_file.read_text(encoding='utf-8').strip() == 'FILE CONTENT'
    captured = capsys.readouterr()

    expected_msg = normalize_output(
        FILE_WRITE_SUCCESS_MSG.format(output_file=str(output_file))
    )
    assert expected_msg in normalize_output(captured.out)


def test_process_interactive_mode_replacement(monkeypatch):
    mock_replace_text = MagicMock()

    monkeypatch.setattr(processing, 'replace_text', mock_replace_text)
    monkeypatch.setattr(processing, 'program_exit', lambda: sys.exit(0))

    args = ParsedArgs(
        pipeline=[ARGS_MAP['replace-case']],
        lang='en',
        input_files=[],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=False,
        debug=False,
        max_file_mb=DEFAULT_MAX_FILE_MB
    )

    with pytest.raises(SystemExit):
        processing.process_interactive_mode(args)

    mock_replace_text.assert_called_once_with('replace_case')


def test_process_mmap_regex_multiple_files(tmp_path):
    input_file1 = tmp_path / 'input1.txt'
    input_file1.write_text('first target123', encoding='utf-8')
    input_file2 = tmp_path / 'input2.txt'
    input_file2.write_text('second target456', encoding='utf-8')
    output_file = tmp_path / 'output.txt'

    args = ParsedArgs(
        pipeline=[ARGS_MAP['replace-regex']],
        lang='en',
        input_files=[str(input_file1), str(input_file2)],
        output_file=str(output_file),
        markdown=False,
        find=r'target\d{3}',
        replace='replaced',
        copy_to_clipboard=False,
        debug=False,
        max_file_mb=DEFAULT_MAX_FILE_MB
    )

    processing._process_mmap_regex(str(input_file1), args)
    processing._process_mmap_regex(str(input_file2), args)

    assert (
        output_file.read_text(encoding='utf-8')
        == 'first replaced\nsecond replaced\n'
    )


def test_process_piped_mode_copy_flag(
    monkeypatch,
    mock_clipboard,
    capsys
):
    mock_read = MagicMock(return_value='piped text\n')
    monkeypatch.setattr(sys.stdin, 'read', mock_read)

    pipeline = [ARGS_MAP['uppercase']]

    args = ParsedArgs(
        pipeline=pipeline,
        lang='en',
        input_files=[],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=True,
        debug=False,
        max_file_mb=DEFAULT_MAX_FILE_MB
    )

    processing.process_piped_mode(args)

    assert mock_clipboard.paste() == 'PIPED TEXT'
    mock_read.assert_called_once()

    captured = capsys.readouterr()
    assert MODIFIED_TEXT_COPIED_MSG in captured.out


def test_process_piped_mode_warping():
    child = pexpect.spawn(
        f'{sys.executable} -m textwarp lowercase', encoding='utf-8'
    )
    child.sendline('Piped text')
    child.sendeof()
    child.expect(pexpect.EOF)

    assert 'piped text' in child.before.lower()
