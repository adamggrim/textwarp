"""Tests for pure string replacement functions."""

import regex as re

from textwarp._core.enums import CaseSeparator
from textwarp._lib.casing.programming_casing import to_separator_case
from textwarp._lib.replacement import (
    replace_case,
    replace_regex,
    replace_text
)


def test_replace_case():
    search_pattern = re.compile(r'\b_?\p{L}[\p{L}\d]*(?:_[\p{L}\d]+)+\b')

    result = replace_case(
        'that_thing_I_harpoon',
        search_pattern,
        lambda match_text: to_separator_case(match_text, CaseSeparator.KEBAB)
    )

    assert result == 'that-thing-i-harpoon'


def test_replace_regex():
    result = replace_regex('Out, damned spot, out, I say!', r'\ss\w+t', '')

    assert result == 'Out, damned, out, I say!'


def test_replace_text():
    result = replace_text(
        'Fand er sich in seinem Bett zu einem ungeheueren '
        'Ungeziefer verwandelt.',
        'Ungeziefer',
        'Feature'
    )

    assert 'zu einem ungeheueren Feature verwandelt' in result
    assert 'Ungeziefer' not in result
