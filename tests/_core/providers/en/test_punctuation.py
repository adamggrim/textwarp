import pytest

from textwarp._core.providers.en.punctuation import (
    curly_to_straight,
    punct_to_inside,
    punct_to_outside,
    remove_apostrophes,
    straight_to_curly
)


@pytest.mark.parametrize('text, expected', [
    (
        '“Curly quotes are the quotation marks used in good typography.”',
        '"Curly quotes are the quotation marks used in good typography."'
    ),
    (
        'I won’t waste your time or Catherine’s time bargaining for petty '
        'privileges.',
        "I won't waste your time or Catherine's time bargaining for petty "
        'privileges.'
    ),
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


def test_punct_to_inside():
    assert (
        punct_to_inside('“Get in, loser, we’re going shopping”.')
        == '“Get in, loser, we’re going shopping.”'
    )


def test_punct_to_outside():
    assert (
        punct_to_outside('“You can’t sit with us.”')
        == '“You can’t sit with us”.'
    )


@pytest.mark.parametrize('text, expected', [
    (
        "I imagine they'll call for your removal",
        'I imagine theyll call for your removal'
    ),
    (
        '‘Imagine no possessions.’',
        '‘Imagine no possessions.’'
    ),
    (
        "It's a Man's Man's Man's World",
        'Its a Mans Mans Mans World'
    ),
    (
        'Don’t (Don’t), don’t (Don’t), that’s what you say',
        'Dont (Dont), dont (Dont), thats what you say'
    )
])
def test_remove_apostrophes(text, expected):
    assert remove_apostrophes(text) == expected


@pytest.mark.parametrize('text, expected', [
    (
        '"What happens to a dream deferred?\n'
        '"Does it dry up\n'
        '"Like a raisin in the sun?"',
        '“What happens to a dream deferred?\n'
        '“Does it dry up\n'
        '“Like a raisin in the sun?”'
    ),
    (
        '"Once upon a time freedom used to be life—now it\'s money."',
        '“Once upon a time freedom used to be life—now it’s money.”'
    ),
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
