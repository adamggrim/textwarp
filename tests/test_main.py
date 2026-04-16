"""Tests for pipeline processing and commands."""

import sys

import pytest

from textwarp import __main__
from textwarp._cli.parsing import ParsedArgs


def _dummy_lower(text: str) -> str:
    """Convert text to lowercase for testing."""
    return text.lower()


def _dummy_reverse(text: str) -> str:
    """Reverse text for testing."""
    return text[::-1]


def test_apply_pipeline_analysis():
    """
    Test that an analysis command stops the pipeline and returns `None`.
    """
    analysis_called = False

    def mock_analysis(text):
        nonlocal analysis_called
        analysis_called = True

    pipeline = [
        ('word-count', mock_analysis),
        ('lowercase', _dummy_lower)
    ]

    result = __main__._apply_pipeline('test text', pipeline)

    assert result is None
    assert analysis_called is True


def test_apply_pipeline_clear(monkeypatch):
    """
    Test that the clear command triggers the `clear_clipboard` function.
    """
    clear_called = False

    def mock_clear():
        nonlocal clear_called
        clear_called = True

    monkeypatch.setattr(__main__, 'clear_clipboard', mock_clear)

    pipeline = [('clear', lambda x: x)]
    __main__._apply_pipeline('some text', pipeline)

    assert clear_called is True


def test_apply_pipeline_warping():
    """
    Test that a pipeline of warping functions transforms the text
    correctly.
    """
    pipeline = [
        ('lowercase', _dummy_lower),
        ('reverse', _dummy_reverse)
    ]
    result = __main__._apply_pipeline('HELLO WORLD', pipeline)
    assert result == 'dlrow olleh'


def test_cli_version(capsys, monkeypatch):
    """Verify that "textwarp --version" exits correctly."""
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--version'])

    with pytest.raises(SystemExit) as exc:
        __main__.main()

    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert 'textwarp' in captured.out


def test_main_keyboard_interrupt(monkeypatch):
    """Test that the main function catches a `KeyboardInterrupt`."""
    def mock_parse_args():
        raise KeyboardInterrupt()

    monkeypatch.setattr(__main__, 'parse_args', mock_parse_args)

    exit_called = False
    def mock_program_exit():
        nonlocal exit_called
        exit_called = True

    monkeypatch.setattr(__main__, 'print_padding', lambda: None)
    monkeypatch.setattr(__main__, 'program_exit', mock_program_exit)

    __main__.main()

    assert exit_called is True


def test_main_sets_locale(monkeypatch):
    """
    Test that `main` extracts the language code from `parse_args` and
    applies it to the global context.
    """
    def mock_parse_args():
        return ParsedArgs(
            pipeline=[('clear', lambda x: x)],
            lang='en',
            input_files=[],
            output_file=None,
            markdown=False,
            find=None,
            replace=None
        )

    monkeypatch.setattr(__main__, 'parse_args', mock_parse_args)


def test_piped_input_mode_integration(monkeypatch, mock_clipboard):
    """
    Verify that data piped via `stdin` is processed and copied
    end-to-end.
    """
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: False)
    monkeypatch.setattr(sys.stdin, 'read', lambda: 'eureka\n')
    monkeypatch.setattr(sys, 'argv', ['textwarp', '--uppercase', '--copy'])

    __main__.main()

    assert mock_clipboard.paste() == 'EUREKA'


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
        copy_to_clipboard=False
    )

    with pytest.raises(SystemExit) as excinfo:
        __main__._process_file_mode(args)

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
        copy_to_clipboard=False
    )

    with pytest.raises(SystemExit) as excinfo:
        __main__._process_file_mode(args)

    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert 'not found' in captured.out


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
        copy_to_clipboard=False
    )

    __main__._process_file_mode(args)

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

    monkeypatch.setattr(__main__, 'replace_text', mock_replace_text)

    monkeypatch.setattr(__main__, 'program_exit', lambda: sys.exit(0))

    args = ParsedArgs(
        pipeline=[('replace-case', lambda x: x)],
        lang='en',
        input_files=[],
        output_file=None,
        markdown=False,
        find=None,
        replace=None,
        copy_to_clipboard=False
    )

    with pytest.raises(SystemExit):
        __main__._process_interactive_mode(args)

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
        copy_to_clipboard=True
    )

    __main__._process_piped_mode(args)

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
        copy_to_clipboard=False
    )

    __main__._process_piped_mode(args)

    captured = capsys.readouterr()
    assert 'piped text' in captured.out


def test_validate_piped_commands_rejects_replacement(monkeypatch):
    """Test that replacement commands fail gracefully when piped."""
    monkeypatch.setattr(
        __main__,
        'print_wrapped',
        lambda *args, **kwargs: None
    )

    pipeline = [('replace-text', lambda x: x)]

    with pytest.raises(SystemExit) as excinfo:
        __main__._validate_piped_commands(pipeline, None, None)

    assert excinfo.value.code == 1
