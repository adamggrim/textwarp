"""Tests for straight and curly quote conversion."""

from textwarp._lib.punctuation import (
    curly_to_straight,
    remove_apostrophes,
    straight_to_curly
)


def test_curly_to_straight():
    assert (
        curly_to_straight('“I don’t know what to do!” cried Scrooge.')
        == '"I don\'t know what to do!" cried Scrooge.'
    )
    assert (
        curly_to_straight('“‘Please, sir, I want some more.’”')
        == '"\'Please, sir, I want some more.\'"'
    )
    assert (
        curly_to_straight(
            '“It’s enough for a man to understand his own business, and not '
            'to interfere with other people’s.”'
        )
        == '"It\'s enough for a man to understand his own business, and not '
           'to interfere with other people\'s."'
    )


def test_straight_to_curly_double_quotes():
    assert (
        straight_to_curly('"I\'ll buy you a diamond ring, my friend."')
        == '“I’ll buy you a diamond ring, my friend.”'
    )
    assert (
        straight_to_curly('She said, "I know what it\'s like to be dead."')
        == 'She said, “I know what it’s like to be dead.”'
    )
    assert (
        straight_to_curly('"There\'s nothing you can do that can\'t be done."')
        == '“There’s nothing you can do that can’t be done.”'
    )


def test_straight_to_curly_single_quotes():
    assert straight_to_curly("'Kronos'") == '‘Kronos’'
    assert straight_to_curly(" 'Kronos' ") == ' ‘Kronos’ '


def test_straight_to_curly_apostrophes():
    assert straight_to_curly("don't") == 'don’t'
    assert straight_to_curly("'twas") == '’twas'
    assert straight_to_curly("Guns N' Roses") == 'Guns N’ Roses'
    assert straight_to_curly("90's") == '90’s'


def test_remove_apostrophes():
    assert (
        remove_apostrophes("It's a Man's Man's Man's World")
        == 'Its a Mans Mans Mans World'
    )
    assert (
        remove_apostrophes('Don’t (Don’t), don’t (Don’t), that’s what you say')
        == 'Dont (Dont), dont (Dont), thats what you say'
    )
