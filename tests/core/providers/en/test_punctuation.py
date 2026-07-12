"""Tests for English-specific punctuation conversions."""

from textwarp._core.providers.en.punctuation import (
    curly_to_straight,
    remove_apostrophes,
    straight_to_curly
)


def test_curly_to_straight():
    assert curly_to_straight('“Hello, world”') == '"Hello, world"'
    assert curly_to_straight('It’s a ‘test’') == "It's a 'test'"


def test_remove_apostrophes():
    assert remove_apostrophes("don't") == 'dont'
    assert remove_apostrophes(
        'It’s Only the End of the World'
    ) == 'Its Only the End of the World'
    assert remove_apostrophes('‘quoted’') == '‘quoted’'


def test_straight_to_curly_double_quotes():
    assert straight_to_curly('"Hello"') == '“Hello”'
    assert straight_to_curly('She said, "Hi."') == 'She said, “Hi.”'


def test_straight_to_curly_single_quotes():
    assert straight_to_curly("'Hello'") == '‘Hello’'
    assert straight_to_curly("don't") == "don’t"
    assert straight_to_curly("It's 'written'") == "It’s ‘written’"
