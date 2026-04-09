"""Tests for core warping patterns."""

import regex as re

from textwarp._core.constants.patterns.warping import (
    create_words_regex,
    get_dash,
    get_em_dash_stand_in,
    get_multiple_spaces,
    get_period_separated_initialism,
    get_word_character
)


def test_create_words_regex():
    """Test the dynamic word regex generator."""
    words = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']
    pattern = create_words_regex(words)

    assert isinstance(pattern, re.Pattern)

    match = pattern.search('Slytherin will help you on the way to greatness.')
    assert match is not None
    assert match.group(0).lower() == 'slytherin'


def test_get_dash():
    """Test the en and em dash matching pattern."""
    pattern = get_dash()
    assert pattern.search('An en dash – is here.') is not None
    assert pattern.search('An em dash — is here.') is not None
    assert pattern.search('A standard-hyphen') is None


def test_get_em_dash_stand_in():
    """Test the em dash stand-in pattern."""
    pattern = get_em_dash_stand_in()
    match = pattern.search(
        'Excited, is all he gets, sometimes, an excitable kid, impressed '
        'with--’\n'
        '‘But the sounds he made.’\n'
        '‘Undescribable.\n’'
        '‘Like an animal.'
    )
    assert match is not None
    assert match.group(0) == '--'


def test_get_multiple_spaces():
    """Test the multiple consecutive spaces pattern."""
    pattern = get_multiple_spaces()
    assert pattern.search('Two  spaces') is not None
    assert pattern.search('Three   spaces') is not None
    assert pattern.search('One space') is None


def test_get_period_separated_initialism():
    """Test the period-separated initialism pattern."""
    pattern = get_period_separated_initialism()
    assert pattern.search('U.S.A.') is not None
    assert pattern.search('Ph.D.') is not None
    assert pattern.search('Mr. Smith') is None
    assert pattern.search('End of sentence.') is None


def test_get_word_character():
    """Test the standard word character pattern."""
    pattern = get_word_character()
    assert pattern.search('A') is not None
    assert pattern.search('7') is not None
    assert pattern.search('_') is not None
    assert pattern.match(' ') is None
    assert pattern.match('-') is None
