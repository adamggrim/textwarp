"""Tests for lazy-loading configuration."""

from textwarp._core.config import (
    ContractionExpansion,
    Encoding,
    EntityCasing,
    Punctuation,
    StringCasing,
    TokenCasing
)


def test_contraction_expansion_config():
    """Test that contraction mappings load with the expected types."""
    assert isinstance(ContractionExpansion.get_ambiguous_map(), list)
    assert isinstance(ContractionExpansion.get_unambiguous_map(), dict)
    assert isinstance(ContractionExpansion.get_whatcha_are_words(), list)
    assert isinstance(ContractionExpansion.get_whatcha_have_words(), list)


def test_encoding_config_morse_maps():
    """Test that the Morse map loads and reverses correctly."""
    morse_map = Encoding.get_morse_map()
    assert isinstance(morse_map, dict)
    assert 'A' in morse_map
    assert morse_map['A'] == '.-'

    reversed_map = Encoding.get_morse_reversed_map()
    assert isinstance(reversed_map, dict)
    assert reversed_map['.-'] == 'A'


def test_entity_casing_config():
    """Test that entity casing data loads with expected types."""
    assert isinstance(EntityCasing.get_absolute_map(), dict)
    assert isinstance(EntityCasing.get_contextual_map(), dict)
    assert isinstance(EntityCasing.get_contraction_suffixes(), list)


def test_punctuation_config():
    """Test that punctuation data converts lists to sets."""
    elision_words = Punctuation.get_elision_words()
    assert isinstance(elision_words, frozenset)
    assert 'cause' in elision_words


def test_string_casing_config_types():
    """Test that string casing mappings load with expected types."""
    assert isinstance(StringCasing.get_lookup_map(), dict)
    assert isinstance(StringCasing.get_lowercase_abbreviations(), frozenset)
    assert isinstance(StringCasing.get_map_suffix_exceptions(), list)
    assert isinstance(StringCasing.get_surname_prefix_exceptions(), list)
    assert isinstance(StringCasing.get_surname_prefixes(), list)


def test_string_casing_lookup_map_merging():
    """
    Test that get_lookup_map correctly merges absolute and prefixed
    surname maps.
    """
    lookup_map = StringCasing.get_lookup_map()

    assert len(lookup_map) > 0
    assert lookup_map.get('abc') == 'ABC'
    assert lookup_map.get('dicrescenzo') == 'DiCrescenzo'


def test_token_casing_config():
    """Test that token casing lists are properly converted to sets."""
    particles = TokenCasing.get_lowercase_particles()
    assert isinstance(particles, frozenset)
    assert 'von' in particles
