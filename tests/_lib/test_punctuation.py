from textwarp._lib.punctuation import (
    curly_to_straight,
    hyphens_to_em,
    hyphens_to_en,
    punct_to_inside,
    punct_to_outside,
    remove_apostrophes,
    straight_to_curly
)


def test_hyphens_to_em():
    original = (
        'Call me Ishmael. (Some years ago--never mind how long precisely--)'
    )
    expected = (
        'Call me Ishmael. (Some years ago—never mind how long precisely—)'
    )
    assert hyphens_to_em(original) == expected


def test_hyphens_to_en():
    assert hyphens_to_en('Books I-XII') == 'Books I–XII'


def test_provider_punctuation_delegation():
    assert (
        curly_to_straight('“I don’t know what to do!” cried Scrooge.')
        == '"I don\'t know what to do!" cried Scrooge.'
    )
    assert (
        straight_to_curly('"I\'ll buy you a diamond ring, my friend."')
        == '“I’ll buy you a diamond ring, my friend.”'
    )
    assert (
        punct_to_inside('“Get in, loser, we’re going shopping”.')
        == '“Get in, loser, we’re going shopping.”'
    )
    assert (
        punct_to_outside('“You can’t sit with us.”')
        == '“You can’t sit with us”.'
    )
    assert (
        remove_apostrophes("It's a Man's Man's Man's World")
        == 'Its a Mans Mans Mans World'
    )
