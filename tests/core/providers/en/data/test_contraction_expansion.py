"""Tests for English contraction expansion data loading."""

from types import MappingProxyType

from textwarp._core.providers.en.data import contraction_expansion


def test_contraction_expansion_config():
    """Test that contraction maps load with the expected types."""
    assert isinstance(contraction_expansion.get_ambiguous_map(), tuple)
    assert isinstance(
        contraction_expansion.get_common_stateless_participles(), tuple
    )
    assert isinstance(
        contraction_expansion.get_idiomatic_map(), MappingProxyType
    )
    assert isinstance(
        contraction_expansion.get_unambiguous_map(), MappingProxyType
    )
    assert isinstance(contraction_expansion.get_whatcha_are_words(), tuple)
    assert isinstance(contraction_expansion.get_whatcha_have_words(), tuple)

    assert isinstance(contraction_expansion.get_to_verb_words(), frozenset)
