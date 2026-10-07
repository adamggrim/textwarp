"""Tests for pipeline output routing."""

import sys
from unittest.mock import MagicMock

import pytest
import regex as re

from textwarp._cli import pipeline
from textwarp._cli.args import CLICommand, CommandType
from textwarp._cli.constants.messages import REPLACEMENT_CMD_ERROR_MSG
from textwarp._cli.parsing import TextwarpArgumentParser
from textwarp._core.exceptions import (
    MissingDependencyError,
    TextwarpValidationError
)


def _dummy_lower(text: str) -> str:
    return text.lower()


def _dummy_reverse(text: str) -> str:
    return text[::-1]


def test_apply_pipeline_analysis(monkeypatch):
    monkeypatch.setattr('textwarp._cli.pipeline.Spinner', MagicMock())

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

    result = pipeline.apply_pipeline(
        'To number the streaks of the tulip',
        test_pipeline
    )

    assert 'Word count: 7' in result
    assert 'Character count: 34' in result
    assert result == 'Word count: 7\nCharacter count: 34'
    mock_word_count.assert_called_once()
    mock_char_count.assert_called_once()


def test_apply_pipeline_clear(monkeypatch):
    mock_clear = MagicMock()

    monkeypatch.setattr(pipeline, 'clear_clipboard', mock_clear)

    test_pipeline = [
        CLICommand('clear', lambda x: x, '', CommandType.STANDALONE)
    ]
    pipeline.apply_pipeline(
        'scribit damnatque tabellas, et notat et delet',
        test_pipeline
    )

    mock_clear.assert_called_once()


def test_apply_pipeline_spacy_doc_persistence(monkeypatch):
    monkeypatch.setattr('textwarp._cli.pipeline.Spinner', MagicMock())

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

    input_text = 'La persistència de la memòria'
    result = pipeline.apply_pipeline(input_text, test_pipeline)

    assert result == input_text
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
    parser = TextwarpArgumentParser()
    active_cmds = ['strip', 'lowercase', 'snake-case']
    pipeline_result = pipeline.build_pipeline(active_cmds, parser)

    assert len(pipeline_result) == len(active_cmds)
    cmd_names = [cmd.name for cmd in pipeline_result]
    assert cmd_names == active_cmds


def test_build_valid_single_command():
    parser = TextwarpArgumentParser()
    cmd_name = 'camel-case'
    pipeline_result = pipeline.build_pipeline([cmd_name], parser)

    assert len(pipeline_result) == 1
    cmd = pipeline_result[0]
    assert cmd.name == cmd_name
    assert callable(cmd.func)


def test_validate_piped_commands_rejects_replacement():
    test_pipeline = [
        CLICommand('replace-text', lambda x: x, '', CommandType.REPLACEMENT)
    ]

    with pytest.raises(
        TextwarpValidationError,
        match=re.escape(REPLACEMENT_CMD_ERROR_MSG)
    ):
        pipeline.validate_piped_commands(test_pipeline, None, None)


def test_missing_marko_dependency(monkeypatch):
    monkeypatch.setitem(sys.modules, 'textwarp._lib.markdown', None)

    with pytest.raises(
        MissingDependencyError, match="Markdown support requires 'marko'"
    ):
        pipeline.route_text(
            '## Rain also is of the process', pipeline=[], parse_markdown=True
        )


def test_bind_pipeline_interactive_analysis_prompt(monkeypatch):
    mock_prompt = MagicMock(return_value=8)
    monkeypatch.setattr(
        'textwarp._cli.pipeline.prompt_for_integer', mock_prompt
    )

    from textwarp._cli.args import ARGS_MAP
    from textwarp._cli.parsing import DEFAULT_MAX_FILE_MB, ParsedArgs

    args = ParsedArgs(
        pipeline=[ARGS_MAP['mfws']],
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

    bound_args = pipeline.bind_pipeline(args, interactive=True)

    mock_prompt.assert_called_once()
    assert bound_args.number == 8
    result = pipeline.apply_pipeline(
        'punch wine bread cheese apples pipes and tobacco',
        bound_args.pipeline
    )
    assert "'pipes'" in result
