"""Exposes constants for use across the package."""

from textwarp._core.constants.maps import get_case_names_regex_map
from textwarp._core.constants.nlp import NOUN_TAGS, POS_TAGS, POS_WORD_TAGS
from textwarp._core.constants.patterns import (
    case_conversion,
    cases,
    warping
)

__all__ = [
    'get_case_names_regex_map',
    'NOUN_TAGS',
    'POS_TAGS',
    'POS_WORD_TAGS',
    'case_conversion',
    'cases',
    'warping'
]
