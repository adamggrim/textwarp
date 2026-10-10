"""Tests for straight and curly quote conversion."""

import pytest

from textwarp._lib.punctuation import (
    curly_to_straight,
    remove_apostrophes,
    straight_to_curly
)


@pytest.mark.parametrize('text, expected', [
    (
        '“I don’t know what to do!” cried Scrooge.',
        '"I don\'t know what to do!" cried Scrooge.'
    ),
    (
        '“‘Please, sir, I want some more.’”',
        '"\'Please, sir, I want some more.\'"'
    ),
    (
        '“It’s enough for a man to understand his own business, and not to '
        'interfere with other people’s.”',
        '"It\'s enough for a man to understand his own business, and not to '
        'interfere with other people\'s."'
    )
])
def test_curly_to_straight(text, expected):
    assert curly_to_straight(text) == expected

@pytest.mark.parametrize('text, expected', [
    (
        '"I\'ll buy you a diamond ring, my friend."',
        '“I’ll buy you a diamond ring, my friend.”'
    ),
    (
        'She said, "I know what it\'s like to be dead."',
        'She said, “I know what it’s like to be dead.”'
    ),
    (
        '"There\'s nothing you can do that can\'t be done."',
        '“There’s nothing you can do that can’t be done.”'
    ),
    ("'Kronos'", '‘Kronos’'),
    (" 'Kronos' ", ' ‘Kronos’ '),
    ("don't", 'don’t'),
    ("'twas", '’twas'),
    ("Guns N' Roses", 'Guns N’ Roses'),
    ("90's", '90’s')
])
def test_straight_to_curly(text, expected):
    assert straight_to_curly(text) == expected

@pytest.mark.parametrize('text, expected', [
    ("It's a Man's Man's Man's World", 'Its a Mans Mans Mans World'),
    (
        'Don’t (Don’t), don’t (Don’t), that’s what you say',
        'Dont (Dont), dont (Dont), thats what you say'
    )
])
def test_remove_apostrophes(text, expected):
    assert remove_apostrophes(text) == expected