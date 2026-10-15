from types import MappingProxyType

from textwarp._core.providers.en.data import (
    contraction_expansion,
    entity_casing,
    punctuation,
    string_casing,
    token_casing
)


def test_contraction_expansion_config():
    assert isinstance(contraction_expansion.get_ambiguous_map(), tuple)
    assert isinstance(
        contraction_expansion.get_common_stateless_participles(), tuple
    )
    assert isinstance(
        contraction_expansion.get_idioms_map(), MappingProxyType
    )
    assert isinstance(
        contraction_expansion.get_unambiguous_map(), MappingProxyType
    )
    assert isinstance(contraction_expansion.get_whatcha_are_words(), tuple)
    assert isinstance(contraction_expansion.get_whatcha_have_words(), tuple)
    assert isinstance(
        contraction_expansion.get_infinitive_exceptions(), frozenset
    )


def test_entity_casing_config():
    assert isinstance(entity_casing.get_absolute_map(), MappingProxyType)
    assert isinstance(entity_casing.get_contextual_map(), MappingProxyType)
    assert isinstance(entity_casing.get_contraction_suffixes(), frozenset)


def test_punctuation_config():
    elision_words = punctuation.get_elision_words()
    assert isinstance(elision_words, frozenset)
    assert 'cause' in elision_words


def test_string_casing_config_types():
    assert isinstance(string_casing.get_lookup_map(), MappingProxyType)
    assert isinstance(string_casing.get_lowercase_abbreviations(), frozenset)
    assert isinstance(string_casing.get_map_suffix_exceptions(), frozenset)
    assert isinstance(string_casing.get_surname_prefix_exceptions(), frozenset)
    assert isinstance(string_casing.get_surname_prefixes(), frozenset)


def test_string_casing_lookup_map_merging():
    lookup_map = string_casing.get_lookup_map()

    assert len(lookup_map) > 0
    assert lookup_map.get('abc') == 'ABC'
    assert lookup_map.get('dicrescenzo') == 'DiCrescenzo'


def test_token_casing_config():
    particles = token_casing.get_lowercase_particles()
    assert isinstance(particles, frozenset)
    assert 'von' in particles
