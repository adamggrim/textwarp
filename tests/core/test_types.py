"""Tests for generic type definitions."""

from textwarp._core.types import EntityCasingContext


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
