"""Exposes English-specific data modules."""

from textwarp._core.providers.en.data import (
    contraction_expansion,
    entity_casing,
    punctuation,
    string_casing,
    token_casing
)

__all__ = [
    'contraction_expansion',
    'entity_casing',
    'load_data',
    'punctuation',
    'string_casing',
    'token_casing'
]
