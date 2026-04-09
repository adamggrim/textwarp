"""Tests for English string casing data loading."""

from types import MappingProxyType

from textwarp._core.providers.en.data import string_casing


def test_string_casing_config_types():
    """Test that string casing maps load with the expected types."""
    assert isinstance(string_casing.get_lookup_map(), MappingProxyType)
    assert isinstance(string_casing.get_lowercase_abbreviations(), frozenset)
    assert isinstance(string_casing.get_map_suffix_exceptions(), frozenset)
    assert isinstance(string_casing.get_surname_prefix_exceptions(), frozenset)
    assert isinstance(string_casing.get_surname_prefixes(), frozenset)


def test_string_casing_lookup_map_merging():
    """
    Test that `get_lookup_map` correctly merges absolute and prefixed
    surname maps.
    """
    lookup_map = string_casing.get_lookup_map()

    assert len(lookup_map) > 0
    assert lookup_map.get('abc') == 'ABC'
    assert lookup_map.get('dicrescenzo') == 'DiCrescenzo'
