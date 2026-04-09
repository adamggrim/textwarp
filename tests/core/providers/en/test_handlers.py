"""Tests for contraction handler functions."""

from textwarp._core.providers.en.handlers import (
    handle_d,
    handle_gotta,
    handle_negation,
    handle_s,
    handle_wanna,
    handle_whatcha
)


def test_handle_d(get_contraction_span):
    """Test the full handler pipeline for "'d" contractions."""
    span = get_contraction_span("I'd like to teach the world to sing.", "I'd")
    result = handle_d(span)
    assert result is not None
    assert result[0] == 'I would'


def test_handle_gotta(get_contraction_span):
    """
    Test the handler pipeline for "gotta", ensuring "have/has"
    prefixing.
    """
    span1 = get_contraction_span('I gotta go see about a girl.', 'gotta')
    result1 = handle_gotta(span1)
    assert result1 is not None
    assert result1[0] == 'have got to'

    span2 = get_contraction_span("It's gotta be the shoes.", 'gotta')
    result2 = handle_gotta(span2)
    assert result2 is not None
    assert result2[0] == 'got to'

    span3 = get_contraction_span(
        "We've gotta hold on to what we've got.", 'gotta'
    )
    result3 = handle_gotta(span3)
    assert result3 is not None
    assert result3[0] == 'got to'


def test_handle_negation_standard(get_contraction_span):
    """Test standard negation expansions."""
    span = get_contraction_span("Mama couldn't be persuaded.", "couldn't")
    result = handle_negation(span)
    assert result is not None
    expanded, _ = result
    assert expanded == 'could not'


def test_handle_negation_inverted(get_contraction_span):
    """Test inverted negation expansions (questions/fragments)."""
    span = get_contraction_span(
        "Didn't I blow your mind this time?", "Didn't"
    )
    result = handle_negation(span)
    assert result is not None
    expanded, _ = result
    assert expanded == 'Did I not'


def test_handle_s(get_contraction_span):
    """Test the full handler pipeline for ''s' contractions."""
    span = get_contraction_span("Here's Johnny", "Here's")
    result = handle_s(span)
    assert result is not None
    assert result[0] == 'Here is'


def test_handle_wanna(get_contraction_span):
    """Test the full handler pipeline for 'wanna' contractions."""
    span = get_contraction_span('I wanna dance with somebody.', 'wanna')
    result = handle_wanna(span)
    assert result is not None
    assert result[0] == 'want to'


def test_handle_whatcha(get_contraction_span):
    """Test the full handler pipeline for whatcha expansion."""
    span = get_contraction_span("Whatcha doin'?", 'Whatcha')
    result = handle_whatcha(span)
    assert result is not None
    assert result[0] == 'What are you'
