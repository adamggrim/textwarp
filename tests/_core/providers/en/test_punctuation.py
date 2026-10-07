"""Tests for English-specific punctuation conversions."""

from textwarp._core.providers.en.punctuation import (
    curly_to_straight,
    punct_to_inside,
    punct_to_outside,
    remove_apostrophes,
    straight_to_curly
)


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


def test_curly_to_straight():
    assert curly_to_straight(
        '“Curly quotes are the quotation marks used in good typography.”'
    ) == '"Curly quotes are the quotation marks used in good typography."'
    assert curly_to_straight(
        'I won’t waste your time or Catherine’s time bargaining for petty '
        'privileges.'
    ) == (
        "I won't waste your time or Catherine's time bargaining for petty "
        'privileges.'
    )


def test_remove_apostrophes():
    single_quoted = '‘Imagine no possessions.’'
    assert remove_apostrophes(
        "I imagine they'll call for your removal"
    ) == 'I imagine theyll call for your removal'
    assert remove_apostrophes(single_quoted) == single_quoted


def test_straight_to_curly():
    assert straight_to_curly(
        '"What happens to a dream deferred?\n'
        '"Does it dry up\n'
        '"Like a raisin in the sun?"'
    ) == (
        '“What happens to a dream deferred?\n'
        '“Does it dry up\n'
        '“Like a raisin in the sun?”'
    )
    assert straight_to_curly(
        '"Once upon a time freedom used to be life—now it\'s money."'
    ) == '“Once upon a time freedom used to be life—now it’s money.”'
