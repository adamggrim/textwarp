"""Tests for pipeline output routing."""

import argparse
import sys
from unittest.mock import MagicMock

import pytest

from textwarp._cli import pipeline
from textwarp._cli.args import CLICommand, CommandType
from textwarp._core.exceptions import (
    MissingDependencyError,
    TextwarpValidationError
)


def _dummy_lower(text: str) -> str:
    return text.lower()


def _dummy_reverse(text: str) -> str:
    return text[::-1]


def test_apply_pipeline_analysis(monkeypatch):
    """
    Test that analysis commands freeze the text stream and join outputs.
    """
    mock_spinner = MagicMock(
        side_effect=lambda f, *args, **kwargs: f(*args, **kwargs)
    )
    monkeypatch.setattr('textwarp._cli.spinner.run_with_spinner', mock_spinner)

    mock_word_count = MagicMock(
        side_effect=lambda text: f'Word count: {len(text.split())}'
    )
    mock_char_count = MagicMock(
        side_effect=lambda text: f'Character count: {len(text)}'
    )

    test_pipeline = [
        CLICommand('lowercase', _dummy_lower, '', CommandType.WARPING),
        CLICommand('word-count', mock_word_count, '', CommandType.ANALYSIS),
        CLICommand('char-count', mock_char_count, '', CommandType.ANALYSIS)
    ]

    result = pipeline.apply_pipeline('Test text', test_pipeline)

    assert 'Word count: 2' in result
    assert 'Character count: 9' in result
    assert result == 'Word count: 2\nCharacter count: 9'
    mock_word_count.assert_called_once()
    mock_char_count.assert_called_once()


def test_apply_pipeline_clear(monkeypatch):
    mock_clear = MagicMock()

    monkeypatch.setattr(pipeline, 'clear_clipboard', mock_clear)

    test_pipeline = [
        CLICommand('clear', lambda x: x, '', CommandType.STANDALONE)
    ]
    pipeline.apply_pipeline('some text', test_pipeline)

    mock_clear.assert_called_once()


def test_apply_pipeline_spacy_doc_persistence(monkeypatch):
    mock_spinner = MagicMock(
        side_effect=lambda f, *args, **kwargs: f(*args, **kwargs)
    )
    monkeypatch.setattr('textwarp._cli.spinner.run_with_spinner', mock_spinner)

    class DummyDoc:
        def __init__(self, text):
            self.text = text

    mock_process_doc = MagicMock(
        side_effect=lambda x: DummyDoc(x) if isinstance(x, str) else x
    )
    monkeypatch.setattr(
        'textwarp._cli.pipeline.process_as_doc', mock_process_doc
    )

    mock_spacy_cmd = MagicMock(side_effect=lambda x: x)

    test_pipeline = [
        CLICommand(
            'title-case',
            mock_spacy_cmd,
            '',
            CommandType.WARPING,
            requires_spacy=True
        ),
        CLICommand(
            'sentence-case',
            mock_spacy_cmd,
            '',
            CommandType.WARPING,
            requires_spacy=True
        )
    ]

    result = pipeline.apply_pipeline(
        'La persistència de la memòria', test_pipeline
    )

    assert result == 'La persistència de la memòria'
    assert mock_spacy_cmd.call_count == 2

    first_call_arg = mock_spacy_cmd.call_args_list[0][0][0]
    second_call_arg = mock_spacy_cmd.call_args_list[1][0][0]

    assert isinstance(first_call_arg, DummyDoc)
    assert first_call_arg is second_call_arg


def test_apply_pipeline_warping():
    test_pipeline = [
        CLICommand('lowercase', _dummy_lower, '', CommandType.WARPING),
        CLICommand('reverse', _dummy_reverse, '', CommandType.WARPING)
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
    active_cmds = ['strip', 'lowercase', 'snake-case']
    pipeline_result = pipeline.build_pipeline(active_cmds, parser)

    assert len(pipeline_result) == 3
    cmd_names = [cmd.name for cmd in pipeline_result]
    assert cmd_names == ['strip', 'lowercase', 'snake-case']


def test_build_valid_single_command():
    parser = argparse.ArgumentParser()
    active_cmds = ['camel-case']
    pipeline_result = pipeline.build_pipeline(active_cmds, parser)

    assert len(pipeline_result) == 1
    cmd = pipeline_result[0]
    assert cmd.name == 'camel-case'
    assert callable(cmd.func)


def test_validate_piped_commands_rejects_replacement():
    test_pipeline = [
        CLICommand('replace-text', lambda x: x, '', CommandType.REPLACEMENT)
    ]

    with pytest.raises(
        TextwarpValidationError,
        match='Replacement commands require'
    ):
        pipeline.validate_piped_commands(test_pipeline, None, None)


def test_missing_marko_dependency(monkeypatch, capsys):
    monkeypatch.setitem(sys.modules, 'textwarp._lib.markdown', None)

    with pytest.raises(
        MissingDependencyError, match="Markdown support requires 'marko'"
    ):
        pipeline.route_text(
            '## Rain also is of the process', pipeline=[], parse_markdown=True
        )
