"""Tests for straight and curly quote conversion."""

from textwarp._lib.punctuation import (
    curly_to_straight,
    remove_apostrophes,
    straight_to_curly
)


def test_curly_to_straight():
    """Test curly-to-straight quote conversion."""
    assert (
        curly_to_straight('“Here’s looking at you, kid.”')
        == '"Here\'s looking at you, kid."'
    )
    assert (
        curly_to_straight('“I’m gonna make him an offer he can’t refuse!”')
        == '"I\'m gonna make him an offer he can\'t refuse!"'
    )
    assert (
        curly_to_straight('“‘Please, sir, I want some more.’”')
        == '"\'Please, sir, I want some more.\'"'
    )


def test_straight_to_curly_double_quotes():
    """Test straight double quote conversion."""
    assert (
        straight_to_curly('"Hello, is it me you\'re looking for?"')
        == '“Hello, is it me you’re looking for?”'
    )
    assert (
        straight_to_curly('She said, "I know what it\'s like to be dead."')
        == 'She said, “I know what it’s like to be dead.”'
    )
    assert straight_to_curly('("Hello, it\'s me.")') == '(“Hello, it’s me.”)'


def test_straight_to_curly_single_quotes():
    """Test straight single quote conversion."""
    assert straight_to_curly("'Kronos'") == '‘Kronos’'
    assert straight_to_curly(" 'Kronos' ") == ' ‘Kronos’ '


def test_straight_to_curly_apostrophes():
    """Test intra-word apostrophe conversion."""
    assert straight_to_curly("don't") == "don’t"
    assert straight_to_curly("'twas") == "’twas"
    assert straight_to_curly("Guns N' Roses") == "Guns N’ Roses"
    assert straight_to_curly("90's") == "90’s"


def test_remove_apostrophes():
    """Test intra-word apostrophe removal."""
    assert (
        remove_apostrophes("It's a Man's Man's Man's World")
        == 'Its a Mans Mans Mans World'
    )
    assert (
        remove_apostrophes('Don’t (Don’t), don’t (Don’t), that’s what you say')
        == 'Dont (Dont), dont (Dont), thats what you say'
    )
