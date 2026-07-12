"""Tests for pure string replacement functions."""

import regex as re

from textwarp._lib.casing.programming_casing import to_camel_case
from textwarp._lib.replacement import (
    replace_case,
    replace_regex,
    replace_text
)


def test_replace_case():
    search_pattern = re.compile(r'\b_?\p{L}[\p{L}\d]*(?:_[\p{L}\d]+)+\b')

    result = replace_case('pascal_case', search_pattern, to_camel_case)

    assert result == 'pascalCase'


def test_replace_regex():
    result = replace_regex(
        '525,600 minutes',
        r'(\d{3}),(\d{3})',
        'five hundred twenty-five thousand, six hundred'
    )

    assert result == 'five hundred twenty-five thousand, six hundred minutes'


def test_replace_text():
    result = replace_text(
        'Fand er sich in seinem Bett zu einem ungeheueren '
        'Ungeziefer verwandelt.',
        'Ungeziefer',
        'Feature'
    )

    assert 'zu einem ungeheueren Feature verwandelt' in result
    assert 'Ungeziefer' not in result
