"""Tests for contraction handler functions."""

from textwarp._core.providers.en.expansion.strategies import (
    expand_d_contraction,
    expand_gotta,
    expand_negative_contraction,
    expand_s_contraction,
    expand_wanna,
    expand_whatcha
)


def test_expand_d_contraction(get_contraction_span):
    span = get_contraction_span('I’d like to teach the world to sing.', 'I’d')
    result = expand_d_contraction(span)
    assert result is not None
    assert result[0] == 'I would'


def test_expand_gotta(get_contraction_span):
    span1 = get_contraction_span('I gotta go see about a girl.', 'gotta')
    result1 = expand_gotta(span1)
    assert result1 is not None
    assert result1[0] == 'have got to'

    span2 = get_contraction_span('It’s gotta be the shoes.', 'gotta')
    result2 = expand_gotta(span2)
    assert result2 is not None
    assert result2[0] == 'has got to'

    span3 = get_contraction_span(
        'We’ve gotta hold on to what we’ve got.', 'gotta'
    )
    result3 = expand_gotta(span3)
    assert result3 is not None
    assert result3[0] == 'have got to'


def test_expand_gotta_complex(get_contraction_span):
    span1 = get_contraction_span(
        'Cause sometimes you just feel tired\n'
        'Feel weak, and when you feel weak\n'
        'You feel like you wanna just give up\n'
        'But you ‘gotta’ search within you',
        'gotta'
    )
    result1 = expand_gotta(span1)

    assert result1 is not None
    assert result1[0] == 'have got to'

    span2 = get_contraction_span(
        '“This man’s just gotta go”, declared his enemies', 'gotta'
    )
    result2 = expand_gotta(span2)

    assert result2 is not None
    assert result2[0] == 'has got to'


def test_expand_negative_contraction_standard(get_contraction_span):
    span = get_contraction_span('Mama couldn’t be persuaded.', 'couldn’t')
    result = expand_negative_contraction(span)
    assert result is not None
    expanded, _ = result
    assert expanded == 'could not'


def test_expand_negative_contraction_inverted(get_contraction_span):
    span = get_contraction_span(
        'Didn’t I blow your mind this time?', 'Didn’t'
    )
    result = expand_negative_contraction(span)
    assert result is not None
    expanded, _ = result
    assert expanded == 'Did I not'


def test_expand_negative_contraction_inverted_capitalized(
    get_contraction_span
):
    span = get_contraction_span(
        'Didn’t It Rain', 'Didn’t'
    )
    result = expand_negative_contraction(span)
    assert result is not None
    expanded, _ = result
    assert expanded == 'Did It Not'


def test_expand_s_contraction(get_contraction_span):
    span = get_contraction_span('Here’s Johnny', 'Here’s')
    result = expand_s_contraction(span)
    assert result is not None
    assert result[0] == 'Here is'


def test_expand_wanna(get_contraction_span):
    span = get_contraction_span('I wanna dance with somebody.', 'wanna')
    result = expand_wanna(span)
    assert result is not None
    assert result[0] == 'want to'


def test_expand_whatcha(get_contraction_span):
    span = get_contraction_span('Whatcha doin’?', 'Whatcha')
    result = expand_whatcha(span)
    assert result is not None
    assert result[0] == 'What are you'
