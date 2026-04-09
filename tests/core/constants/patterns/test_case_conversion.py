"""Tests for core case conversion regular expressions."""

import regex as re

from textwarp._core.constants.patterns.case_conversion import (
    get_any_separator,
    get_split_camel_or_pascal,
    get_split_for_pascal_conversion,
    get_split_for_separator_conversion
)


def test_get_any_separator():
    """Verify the pattern matching any supported separator."""
    pattern = get_any_separator()

    assert isinstance(pattern, re.Pattern)
    assert pattern.match('.') is not None
    assert pattern.match('-') is not None
    assert pattern.match('_') is not None


def test_get_split_camel_or_pascal():
    """Verify the pattern for splitting camel or Pascal case strings."""
    pattern = get_split_camel_or_pascal()

    assert isinstance(pattern, re.Pattern)
    assert pattern.split('camelCase') == ['camel', 'Case']
    assert pattern.split('PascalCase') == ['Pascal', 'Case']
    assert pattern.split('HTML5Parser') == ['HTML', '5', 'Parser']


def test_get_split_for_pascal_conversion():
    """
    Verify the pattern for splitting strings prior to Pascal conversion.
    """
    pattern = get_split_for_pascal_conversion()

    assert isinstance(pattern, re.Pattern)

    parts = pattern.split('snake_case_word')
    assert 'snake' in parts
    assert 'case' in parts

    parts2 = pattern.split('dot.case.word')
    assert 'dot' in parts2


def test_get_split_for_separator_conversion():
    """
    Verify the pattern for splitting on non-separator word boundaries.
    """
    pattern = get_split_for_separator_conversion()

    assert isinstance(pattern, re.Pattern)

    parts = pattern.split('hello darkness my old friend')
    assert 'hello' in parts
    assert 'darkness' in parts
    assert 'old' in parts
    assert 'friend' in parts
