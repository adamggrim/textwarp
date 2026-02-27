"""Tests for pipeline processing and commands."""

import pytest
import sys

from textwarp import __main__ as main_module

def _dummy_lower(text: str) -> str:
    return text.lower()


def _dummy_reverse(text: str) -> str:
    return text[::-1]



def test_apply_pipeline_warping():
    """
    Test that a pipeline of warping functions transforms the text correctly.
    """
    pipeline = [
        ('lowercase', _dummy_lower),
        ('reverse', _dummy_reverse)
    ]
    result = main_module._apply_pipeline("HELLO WORLD", pipeline)
    assert result == 'dlrow olleh'


def test_apply_pipeline_analysis(monkeypatch):
    """Test that an analysis command stops the pipeline and returns None."""
    analysis_called = False

    def mock_analysis(text):
        nonlocal analysis_called
        analysis_called = True

    pipeline = [
        ('word-count', mock_analysis),
        ('lowercase', _dummy_lower)
    ]

    result = main_module._apply_pipeline('test text', pipeline)

    assert result is None
    assert analysis_called is True

def test_apply_pipeline_clear(monkeypatch):
    """
    Test that the clear command triggers the clear_clipboard function.
    """
    clear_called = False

    def mock_clear():
        nonlocal clear_called
        clear_called = True

    monkeypatch.setattr(main_module, 'clear_clipboard', mock_clear)

    pipeline = [('clear', lambda x: x)]
    main_module._apply_pipeline('some text', pipeline)

    assert clear_called is True


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

    monkeypatch.setattr(main_module, 'replace_text', mock_replace_text)

    monkeypatch.setattr(main_module, 'program_exit', lambda: sys.exit(0))

    pipeline = [('replace-case', lambda x: x)]

    with pytest.raises(SystemExit):
        main_module._process_interactive_mode(pipeline)

    assert replace_called is True


def test_process_piped_mode_warping(monkeypatch):
    """Test that piped mode reads from stdin and runs warp_and_copy."""
    monkeypatch.setattr(sys.stdin, 'read', lambda: 'Piped text\n')

    warp_called = False
    def mock_warp_and_copy(func, text):
        nonlocal warp_called
        warp_called = True
        assert text == 'Piped text'
        assert func('A') == 'a'

    monkeypatch.setattr(main_module, 'warp_and_copy', mock_warp_and_copy)

    pipeline = [('lowercase', _dummy_lower)]
    main_module._process_piped_mode(pipeline)

    assert warp_called is True


def test_validate_piped_commands_rejects_replacement(monkeypatch):
    """Test that replacement commands fail gracefully when piped."""
    monkeypatch.setattr(
        main_module,
        'print_wrapped',
        lambda *args, **kwargs: None
    )

    pipeline = [('replace', lambda x: x)]

    with pytest.raises(SystemExit) as excinfo:
        main_module._validate_piped_commands(pipeline)

    assert excinfo.value.code == 1


def test_main_keyboard_interrupt(monkeypatch):
    """Test that the main function catches a KeyboardInterrupt."""
    def mock_parse_args():
        raise KeyboardInterrupt()

    monkeypatch.setattr(main_module, 'parse_args', mock_parse_args)

    exit_called = False
    def mock_program_exit():
        nonlocal exit_called
        exit_called = True

    monkeypatch.setattr(main_module, 'print_padding', lambda: None)
    monkeypatch.setattr(main_module, 'program_exit', mock_program_exit)

    main_module.main()

    assert exit_called is True
