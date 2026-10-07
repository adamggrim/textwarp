"""Tests for execution modes and pipeline processing."""

import sys
from unittest.mock import MagicMock

import pexpect
import pytest
import regex as re

from tests.helpers import make_parsed_args, normalize_output
from textwarp._cli import processing
from textwarp._cli.args import ARGS_MAP
from textwarp._cli.constants.messages import (
    BINARY_FILE_ERROR_MSG,
    FILE_ACCESS_ERROR_MSG,
    FILE_SIZE_LIMIT_ERROR_MSG,
    FILE_WRITE_SUCCESS_MSG,
    MODIFIED_TEXT_COPIED_MSG
)
from textwarp._cli.parsing import BYTES_PER_MB, DEFAULT_MAX_FILE_MB
from textwarp._core.exceptions import TextwarpError


@pytest.fixture
def mock_oversized_file(monkeypatch):
    oversized_bytes = (DEFAULT_MAX_FILE_MB + 1) * BYTES_PER_MB
    monkeypatch.setattr('os.path.getsize', lambda _: oversized_bytes)


def test_process_file_mode_binary_file(tmp_path):
    binary_file = tmp_path / 'las_meninas.png'
    binary_file.write_bytes(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')

    args = make_parsed_args(input_files=[str(binary_file)])
    expected_msg = BINARY_FILE_ERROR_MSG.format(input_file=str(binary_file))

    with pytest.raises(TextwarpError, match=re.escape(expected_msg)):
        processing.process_file_mode(args)


def test_process_file_mode_file_not_found():
    missing_file = 'airy_nothing.txt'
    args = make_parsed_args(input_files=[missing_file])

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

    args = make_parsed_args(
        input_files=[str(input_file)],
        copy_to_clipboard=True
    )

    processing.process_file_mode(args)

    captured = capsys.readouterr()
    expected_error = FILE_SIZE_LIMIT_ERROR_MSG.format(
        max=DEFAULT_MAX_FILE_MB
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

    args = make_parsed_args(
        pipeline=[ARGS_MAP['replace-regex']],
        input_files=[str(input_file)],
        find=r'(?<!no eran )gigantes',
        replace='molinos de viento'
    )

    mock_mmap_regex = MagicMock()
    monkeypatch.setattr(processing, '_process_mmap_regex', mock_mmap_regex)

    processing.process_file_mode(args)

    mock_mmap_regex.assert_called_once()
    call_args = mock_mmap_regex.call_args[0]
    assert call_args[0] == str(input_file)
    assert call_args[1].find == args.find
    assert call_args[1].replace == args.replace
    assert call_args[2] is sys.stdout.buffer


def test_process_file_mode_success(tmp_path, capsys):
    input_file = tmp_path / 'bouvard.txt'
    input_file.write_text('copier comme autrefois', encoding='utf-8')
    output_file = tmp_path / 'pecuchet.txt'

    args = make_parsed_args(
        input_files=[str(input_file)],
        output_file=str(output_file)
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
    mock_prompt = MagicMock(return_value=('snake', 'pascal'))
    mock_loop = MagicMock()

    monkeypatch.setattr(
        'textwarp._cli.ui.prompt_for_replacement_case', mock_prompt
    )
    monkeypatch.setattr(processing, 'run_command_loop', mock_loop)

    args = make_parsed_args(pipeline=[ARGS_MAP['replace-case']])

    processing.process_interactive_mode(args)

    mock_prompt.assert_called_once()
    mock_loop.assert_called_once()


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

    args = make_parsed_args(
        pipeline=[ARGS_MAP['replace-regex']],
        input_files=[str(input_file1), str(input_file2)],
        output_file=str(output_file),
        find=r'(?:τέτταρας|ἕκαστον)',
        replace='δύο'
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

    args = make_parsed_args(copy_to_clipboard=True)

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
