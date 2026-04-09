"""Tests for generic type definitions."""

import typing

from textwarp._core.types import (
    EntityCasingContext,
    JSONType,
    Pipeline,
    PipelineItem
)


def test_entity_casing_context_dict():
    """
    Verify that `EntityCasingContext` acts as a valid dictionary at runtime.
    """

    context: EntityCasingContext = {
        'casing': 'Moby-Dick',
        'pos_sequences': [['PROPN', 'PUNCT', 'PROPN']],
        'ngrams': ['captain ahab', 'harpoon', 'harpoons', 'ishmael', 'whale']
    }

    assert isinstance(context, dict)
    assert context['casing'] == 'Moby-Dick'
    assert len(context['pos_sequences']) == 1
    assert 'whale' in context['ngrams']


def test_type_aliases():
    """
    Verify that the generic type aliases are defined and accessible.
    """
    assert JSONType is not None

    assert PipelineItem is not None
    assert typing.get_origin(PipelineItem) is tuple

    assert Pipeline is not None
    assert typing.get_origin(Pipeline) is list
