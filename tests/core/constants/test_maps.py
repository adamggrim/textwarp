"""Tests for constant lookup maps."""

import regex as re
from types import MappingProxyType

from textwarp._core.constants.maps import get_case_names_regex_map


def test_get_case_names_regex_map_type():
    """
    Verify that the case names map is returned as an immutable
    `MappingProxyType`.
    """
    regex_map = get_case_names_regex_map()
    assert isinstance(regex_map, MappingProxyType)


def test_get_case_names_regex_map_keys():
    """Verify that the case names map contains the expected keys."""
    regex_map = get_case_names_regex_map()
    assert 'camel' in regex_map
    assert 'snake case' in regex_map
    assert 'pascal' in regex_map
    assert 'lowercase' in regex_map


def test_get_case_names_regex_map_values():
    """
    Verify that the values in the case names map are compiled regular
    expression patterns.
    """
    regex_map = get_case_names_regex_map()
    for pattern in regex_map.values():
        assert isinstance(pattern, re.Pattern)
