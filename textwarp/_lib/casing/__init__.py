"""Exposes casing logic for use across the package."""

from textwarp._lib.casing.case_conversion import (
    to_camel_case,
    to_natural_case,
    to_pascal_case,
    to_separator_case
)
from textwarp._lib.casing.entity_casing import map_all_entities
from textwarp._lib.casing.string_casing import case_from_string
from textwarp._lib.casing.token_casing import should_capitalize_pos_or_length

__all__ = [
    'case_from_string',
    'map_all_entities',
    'should_capitalize_pos_or_length',
    'to_camel_case',
    'to_natural_case',
    'to_pascal_case',
    'to_separator_case'
]
