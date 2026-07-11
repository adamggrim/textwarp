"""Tests for pipeline output routing."""

import argparse

import pytest

from textwarp._cli import pipeline


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

    test_pipeline = [
        ('word-count', mock_analysis),
        ('lowercase', _dummy_lower)
    ]

    result = pipeline.apply_pipeline('test text', test_pipeline)

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

    monkeypatch.setattr(pipeline, 'clear_clipboard', mock_clear)

    test_pipeline = [('clear', lambda x: x)]
    pipeline.apply_pipeline('some text', test_pipeline)

    assert clear_called is True


def test_apply_pipeline_warping():
    """
    Test that a pipeline of warping functions transforms the text
    correctly.
    """
    test_pipeline = [
        ('lowercase', _dummy_lower),
        ('reverse', _dummy_reverse)
    ]
    result = pipeline.apply_pipeline(
        'IN MY BEGINNING IS MY END', test_pipeline
    )
    assert result == 'dne ym si gninnigeb ym ni'


def test_build_valid_pipeline():
    """
    Test building a pipeline with multiple valid, non-conflicting
    commands.
    """
    parser = argparse.ArgumentParser()
    argv = ['textwarp', '--strip', '--lowercase', '--snake-case']
    pipeline_result = pipeline.build_pipeline(argv, parser)

    assert len(pipeline_result) == 3
    cmd_names = [cmd[0] for cmd in pipeline_result]
    assert cmd_names == ['strip', 'lowercase', 'snake-case']


def test_build_valid_single_command():
    """Test building a pipeline with a single valid command."""
    parser = argparse.ArgumentParser()
    argv = ['textwarp', '--camel-case']
    pipeline_result = pipeline.build_pipeline(argv, parser)

    assert len(pipeline_result) == 1
    cmd_name, func = pipeline_result[0]
    assert cmd_name == 'camel-case'
    assert callable(func)


def test_validate_piped_commands_rejects_replacement(monkeypatch):
    """Test that replacement commands fail gracefully when piped."""
    monkeypatch.setattr(
        pipeline,
        'print_wrapped',
        lambda *args, **kwargs: None
    )

    test_pipeline = [('replace-text', lambda x: x)]

    with pytest.raises(SystemExit) as excinfo:
        pipeline.validate_piped_commands(test_pipeline, None, None)

    assert excinfo.value.code == 1
