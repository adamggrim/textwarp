"""Tests for execution modes and pipeline processing."""

import sys
from unittest.mock import MagicMock

import pexpect
import pytest
import regex as re

from tests.helpers import normalize_output
from textwarp._cli import processing
from textwarp._cli.args import ARGS_MAP
from textwarp._cli.constants.messages import (
    BINARY_FILE_ERROR_MSG,
    FILE_ACCESS_ERROR_MSG,
    FILE_SIZE_LIMIT_ERROR_MSG,
    FILE_WRITE_SUCCESS_MSG,
    MODIFIED_TEXT_COPIED_MSG
)
from textwarp._cli.parsing import BYTES_PER_MB, DEFAULT_MAX_FILE_MB, ParsedArgs
from textwarp._core.exceptions import TextwarpError


@pytest.fixture
def mock_oversized_file(monkeypatch):
    oversized_bytes = (DEFAULT_MAX_FILE_MB + 1) * BYTES_PER_MB
    monkeypatch.setattr('os.path.getsize', lambda _: oversized_bytes)


def test_process_file_mode_binary_file(tmp_path):
    binary_file = tmp_path / 'las_meninas.png'
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
    missing_file = 'airy_nothing.txt'

    args = ParsedArgs(
        pipeline=pipeline,
        lang='en',
        input_files=[missing_file],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=False,
        debug=False,
        max_file_mb=DEFAULT_MAX_FILE_MB
    )

    expected_prefix = FILE_ACCESS_ERROR_MSG.format(
        file_path=missing_file, error=''
    )
    with pytest.raises(TextwarpError, match=re.escape(expected_prefix)):
        processing.process_file_mode(args)


@pytest.mark.usefixtures('mock_oversized_file')
def test_process_file_mode_oversized_file_warning(
    tmp_path,
    capsys
):
    input_file = tmp_path / 'sperm_whale_of_the_largest_magnitude.txt'
    input_file.write_text(
        'between eighty-five and ninety feet in length, and something less '
        'than forty feet in its fullest circumference',
        encoding='utf-8'
    )

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
    expected_error = FILE_SIZE_LIMIT_ERROR_MSG.format(
        limit=DEFAULT_MAX_FILE_MB
    )
    expected_warning = normalize_output(
        FILE_ACCESS_ERROR_MSG.format(
            file_path=str(input_file), error=expected_error
        )
    )
    assert expected_warning in normalize_output(captured.out)


@pytest.mark.usefixtures('mock_oversized_file')
def test_process_file_mode_oversized_regex_routing(
    tmp_path,
    monkeypatch,
):
    input_file = tmp_path / 'la_mancha.txt'
    input_file.write_text(
        'Bien pareció a don Quijote que eran gigantes, por más que Sancho le '
        'decía que no eran gigantes, sino molinos de viento.',
        encoding='utf-8'
    )

    args = ParsedArgs(
        pipeline=[ARGS_MAP['replace-regex']],
        lang='en',
        input_files=[str(input_file)],
        output_file=None,
        markdown=False,
        find=r'(?<!no eran )gigantes',
        replace='molinos de viento',
        copy_to_clipboard=False,
        debug=False,
        max_file_mb=DEFAULT_MAX_FILE_MB
    )

    mock_mmap_regex = MagicMock()
    monkeypatch.setattr(processing, '_process_mmap_regex', mock_mmap_regex)

    processing.process_file_mode(args)

    mock_mmap_regex.assert_called_once_with(
        str(input_file), args, sys.stdout.buffer
    )


def test_process_file_mode_success(tmp_path, capsys):
    input_file = tmp_path / 'bouvard.txt'
    input_file.write_text('copier comme autrefois', encoding='utf-8')
    output_file = tmp_path / 'pecuchet.txt'

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

    assert (
        output_file.read_text(encoding='utf-8').strip()
        == 'COPIER COMME AUTREFOIS'
    )
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


@pytest.mark.usefixtures('mock_oversized_file')
def test_process_mmap_regex_multiple_files(tmp_path):
    input_file1 = tmp_path / 'aristophanes.txt'
    input_file1.write_text(
        'χεῖρας δὲ τέτταρας εἶχε, καὶ σκέλη τὰ ἴσα ταῖς χερσίν, καὶ πρόσωπα '
        'δύ’ ἐπ’ αὐχένι κυκλοτερεῖ',
        encoding='utf-8'
    )
    input_file2 = tmp_path / 'zeus.txt'
    input_file2.write_text(
        'διατεμῶ δίχα ἕκαστον, καὶ ἅμα μὲν ἀσθενέστεροι ἔσονται',
        encoding='utf-8'
    )
    output_file = tmp_path / 'hephaestus.txt'

    args = ParsedArgs(
        pipeline=[ARGS_MAP['replace-regex']],
        lang='en',
        input_files=[str(input_file1), str(input_file2)],
        output_file=str(output_file),
        markdown=False,
        find=r'(?:τέτταρας|ἕκαστον)',
        replace='δύο',
        copy_to_clipboard=False,
        debug=False,
        max_file_mb=DEFAULT_MAX_FILE_MB
    )

    processing.process_file_mode(args)

    assert (
        output_file.read_text(encoding='utf-8')
        == (
            'χεῖρας δὲ δύο εἶχε, καὶ σκέλη τὰ ἴσα ταῖς χερσίν, καὶ πρόσωπα '
            'δύ’ ἐπ’ αὐχένι κυκλοτερεῖ\n'
            'διατεμῶ δίχα δύο, καὶ ἅμα μὲν ἀσθενέστεροι ἔσονται\n'
        )
    )


def test_process_piped_mode_copy_flag(
    monkeypatch,
    mock_clipboard,
    capsys
):
    mock_read = MagicMock(return_value='Ceci n’est pas une pipe\n')
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

    assert mock_clipboard.paste() == 'CECI N’EST PAS UNE PIPE'
    mock_read.assert_called_once()

    captured = capsys.readouterr()
    assert MODIFIED_TEXT_COPIED_MSG in captured.out


def test_process_piped_mode_warping():
    child = pexpect.spawn(
        f'{sys.executable} -m textwarp lowercase', encoding='utf-8'
    )
    child.sendline('Piping down the valleys wild')
    child.sendeof()
    child.expect(pexpect.EOF)

    assert 'piping down the valleys wild' in child.before.lower()
