"""Tests for core encoding maps and data loading."""

from types import MappingProxyType

from textwarp._core import encoding


def test_encoding_config_morse_maps():
    morse_map = encoding.get_morse_map()
    assert isinstance(morse_map, MappingProxyType)
    assert 'A' in morse_map
    assert morse_map['A'] == '.-'

    reversed_map = encoding.get_morse_reversed_map()
    assert isinstance(reversed_map, MappingProxyType)
    assert reversed_map['.-'] == 'A'
