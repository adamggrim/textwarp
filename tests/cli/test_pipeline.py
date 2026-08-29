"""Tests for pipeline output routing."""

import argparse
import sys

import pytest

from textwarp._cli import pipeline
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
    monkeypatch.setattr(
        'textwarp._cli.spinner.run_with_spinner',
        lambda f, *args, **kwargs: f(*args, **kwargs)
    )

    def mock_word_count(text):
        return f'Word count: {len(text.split())}'

    def mock_char_count(text):
        return f'Character count: {len(text)}'

    test_pipeline = [
        ('lowercase', _dummy_lower),
        ('word-count', mock_word_count),
        ('char-count', mock_char_count)
    ]

    result = pipeline.apply_pipeline('Test text', test_pipeline)

    assert 'Word count: 2' in result
    assert 'Character count: 9' in result
    assert result == 'Word count: 2\nCharacter count: 9'


def test_apply_pipeline_clear(monkeypatch):
    clear_called = False

    def mock_clear():
        nonlocal clear_called
        clear_called = True

    monkeypatch.setattr(pipeline, 'clear_clipboard', mock_clear)

    test_pipeline = [('clear', lambda x: x)]
    pipeline.apply_pipeline('some text', test_pipeline)

    assert clear_called is True


def test_apply_pipeline_spacy_doc_persistence(monkeypatch):
    monkeypatch.setattr(
        'textwarp._cli.spinner.run_with_spinner',
        lambda f, *args, **kwargs: f(*args, **kwargs)
    )

    class DummyDoc:
        def __init__(self, text):
            self.text = text

    monkeypatch.setattr(
        'textwarp._cli.pipeline.process_as_doc',
        lambda x: DummyDoc(x) if isinstance(x, str) else x
    )

    docs_used = []

    def mock_spacy_cmd(content):
        docs_used.append(content)
        return content

    test_pipeline = [
        ('title-case', mock_spacy_cmd),
        ('sentence-case', mock_spacy_cmd)
    ]

    result = pipeline.apply_pipeline(
        'La persistència de la memòria', test_pipeline
    )

    assert result == 'La persistència de la memòria'
    assert len(docs_used) == 2
    assert isinstance(docs_used[0], DummyDoc)
    assert docs_used[0] is docs_used[1]


def test_apply_pipeline_warping():
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
    active_cmds = ['strip', 'lowercase', 'snake-case']
    pipeline_result = pipeline.build_pipeline(active_cmds, parser)

    assert len(pipeline_result) == 3
    cmd_names = [cmd[0] for cmd in pipeline_result]
    assert cmd_names == ['strip', 'lowercase', 'snake-case']


def test_build_valid_single_command():
    parser = argparse.ArgumentParser()
    active_cmds = ['camel-case']
    pipeline_result = pipeline.build_pipeline(active_cmds, parser)

    assert len(pipeline_result) == 1
    cmd_name, func = pipeline_result[0]
    assert cmd_name == 'camel-case'
    assert callable(func)


def test_validate_piped_commands_rejects_replacement():
    test_pipeline = [('replace-text', lambda x: x)]

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
