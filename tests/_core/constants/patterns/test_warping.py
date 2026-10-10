"""Tests for core warping patterns."""

import pytest
import regex as re

from textwarp._core.constants.patterns.warping import (
    create_words_regex,
    get_dash,
    get_em_dash_stand_in,
    get_multiple_spaces,
    get_period_separated_initialism,
    get_word_char
)


def test_create_words_regex():
    words = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']
    pattern = create_words_regex(words)

    assert isinstance(pattern, re.Pattern)

    match = pattern.search('Slytherin will help you on the way to greatness.')
    assert match is not None
    assert match.group(0).lower() == 'slytherin'


@pytest.mark.parametrize('text, expected_match', [
    ('I do not like them, Sam-I-am.', False),
    (
        'I speak for the trees, for the trees have no tongues. And I’m asking '
        'you, sir, at the top of my lungs”—', True
    ),
    ('1904–1991', True),

])
def test_get_dash(text, expected_match):
    pattern = get_dash()
    if expected_match:
        assert pattern.search(text) is not None
    else:
        assert pattern.search(text) is None


def test_get_em_dash_stand_in():
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


@pytest.mark.parametrize('text, expected_match', [
    ('Two  fish', True),
    ('Red   fish', True),
    ('Blue fish', False)
])
def test_get_multiple_spaces(text, expected_match):
    pattern = get_multiple_spaces()
    if expected_match:
        assert pattern.search(text) is not None
    else:
        assert pattern.search(text) is None


@pytest.mark.parametrize('text, expected_match', [
    ('U.S.A.', True),
    ('Ph.D.', True),
    ('Mrs. Robinson', False),
    ('This is the end.', False)
])
def test_get_period_separated_initialism(text, expected_match):
    pattern = get_period_separated_initialism()
    if expected_match:
        assert pattern.search(text) is not None
    else:
        assert pattern.search(text) is None


@pytest.mark.parametrize('text, is_match', [
    ('A', True),
    ('24', True),
    ('_', True),
    (' ', False),
    ('-', False)
])
def test_get_word_char(text, is_match):
    pattern = get_word_char()
    if is_match:
        assert pattern.search(text) is not None
    else:
        assert pattern.match(text) is None
