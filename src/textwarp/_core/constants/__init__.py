"""Exposes constants for use across the package."""

from textwarp._core.constants.maps import get_case_names_regex_map
from textwarp._core.constants.patterns import (
    cases,
    warping
)

__all__ = [
    'cases',
    'get_case_names_regex_map',
    'warping'
]
