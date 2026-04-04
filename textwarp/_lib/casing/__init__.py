"""Exposes casing logic for use across the package."""

from textwarp._lib.casing.case_conversion import (
    change_first_letter_case,
    doc_to_case,
    to_separator_case,
    word_to_pascal
)
from textwarp._lib.casing.entity_casing import map_all_entities
from textwarp._lib.casing.string_casing import case_from_string
from textwarp._lib.casing.token_casing import should_capitalize_pos_or_length

__all__ = [
    'change_first_letter_case',
    'doc_to_case',
    'to_separator_case',
    'word_to_pascal',
    'map_all_entities',
    'case_from_string',
    'should_capitalize_pos_or_length'
]
