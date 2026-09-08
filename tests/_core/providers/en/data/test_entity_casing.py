"""Tests for English entity casing data loading."""

from types import MappingProxyType

from textwarp._core.providers.en.data import entity_casing


def test_entity_casing_config():
    """Test that entity casing data loads with the expected types."""
    assert isinstance(entity_casing.get_absolute_map(), MappingProxyType)
    assert isinstance(entity_casing.get_contextual_map(), MappingProxyType)
    assert isinstance(entity_casing.get_contraction_suffixes(), frozenset)
