"""Tests for English-specific data loading and caching."""

from types import MappingProxyType

from textwarp._core.providers.en_rules.data import (
    EnContractionExpansion,
    EnEntityCasing,
    EnPunctuation,
    EnStringCasing,
    EnTokenCasing
)


def test_contraction_expansion_data():
    """Test that contraction mappings load with the expected types."""
    assert isinstance(EnContractionExpansion.get_ambiguous_map(), tuple)
    assert isinstance(
        EnContractionExpansion.get_common_stateless_participles(), tuple
    )
    assert isinstance(
        EnContractionExpansion.get_idiomatic_map(), MappingProxyType
    )
    assert isinstance(
        EnContractionExpansion.get_unambiguous_map(), MappingProxyType
    )
    assert isinstance(EnContractionExpansion.get_whatcha_are_words(), tuple)
    assert isinstance(EnContractionExpansion.get_whatcha_have_words(), tuple)


def test_entity_casing_data():
    """Test that entity casing data loads with the expected types."""
    assert isinstance(EnEntityCasing.get_absolute_map(), MappingProxyType)
    assert isinstance(EnEntityCasing.get_contextual_map(), MappingProxyType)
    assert isinstance(EnEntityCasing.get_contraction_suffixes(), frozenset)


def test_punctuation_data():
    """
    Test that punctuation data converts lists to `frozenset` objects.
    """
    elision_words = EnPunctuation.get_elision_words()
    assert isinstance(elision_words, frozenset)
    assert 'cause' in elision_words


def test_string_casing_data():
    """Test that string casing mappings load with the expected types."""
    assert isinstance(EnStringCasing.get_lookup_map(), MappingProxyType)
    assert isinstance(EnStringCasing.get_lowercase_abbreviations(), frozenset)
    assert isinstance(EnStringCasing.get_map_suffix_exceptions(), tuple)
    assert isinstance(EnStringCasing.get_surname_prefix_exceptions(), tuple)
    assert isinstance(EnStringCasing.get_surname_prefixes(), tuple)


def test_token_casing_data():
    """Test that token casing lists are properly converted to sets."""
    particles = EnTokenCasing.get_lowercase_particles()
    assert isinstance(particles, frozenset)
    assert 'von' in particles
