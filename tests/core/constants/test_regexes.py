"""Tests for core regular expression patterns."""

import pytest
import regex as re

from textwarp._core.constants.regexes import (
    CaseConversionPatterns,
    CasePatterns,
    WarpingPatterns
)


def test_pattern_classes_are_non_instantiable():
    """
    Verify that regular expression namespace classes cannot be
    instantiated.
    """
    with pytest.raises(
        RuntimeError, match='CaseConversionPatterns cannot be instantiated'
    ):
        CaseConversionPatterns()

    with pytest.raises(
        RuntimeError, match='CasePatterns cannot be instantiated'
    ):
        CasePatterns()

    with pytest.raises(
        RuntimeError, match='WarpingPatterns cannot be instantiated'
    ):
        WarpingPatterns()


def test_case_patterns_return_compiled_regexes():
    """
    Verify that CasePatterns methods return compiled regular expression
    objects.
    """
    assert isinstance(CasePatterns.get_camel_word(), re.Pattern)
    assert isinstance(CasePatterns.get_snake_word(), re.Pattern)
    assert isinstance(CasePatterns.get_pascal_word(), re.Pattern)


def test_warping_patterns_apostrophe():
    """Test the apostrophe matching pattern."""
    pattern = WarpingPatterns.get_any_apostrophe()
    match = pattern.search("It's alive!")
    assert match is not None
    assert match.group(0) == "'"


def test_warping_patterns_em_dash_stand_in():
    """Test the em dash stand-in pattern."""
    pattern = WarpingPatterns.get_em_dash_stand_in()
    match = pattern.search(
        'Excited, is all he gets, sometimes, an excitable kid, impressed '
        'with--’\n'
        '‘But the sounds he made.’\n'
        '‘Undescribable.\n’'
        '‘Like an animal.'
    )
    assert match is not None
    assert match.group(0) == '--'


def test_warping_patterns_create_words_regex():
    """Test the dynamic word regex generator."""
    words = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']
    pattern = WarpingPatterns._create_words_regex(words)

    assert isinstance(pattern, re.Pattern)

    match = pattern.search('Slytherin will help you on the way to greatness.')
    assert match is not None
    assert match.group(0).lower() == 'slytherin'
