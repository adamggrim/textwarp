"""Tests for contraction handler functions."""

from spacy.tokens import Span
from textwarp._lib.contractions.handlers import (
    handle_d,
    handle_gotta,
    handle_negation,
    handle_s,
    handle_wanna,
    handle_whatcha
)
from textwarp._lib.nlp import process_as_doc


def _get_contraction_span(text: str, contraction: str) -> Span:
    """
    Helper function to extract a spaCy Span for a given contraction in a
    string.
    """
    doc = process_as_doc(text)
    start_char = text.lower().find(contraction.lower())
    end_char = start_char + len(contraction)
    return doc.char_span(start_char, end_char)


def test_handle_d():
    """Test the full handler pipeline for "'d" contractions."""
    span = _get_contraction_span("I'd like to teach the world to sing.", "I'd")
    result = handle_d(span)
    assert result is not None
    assert result[0] == 'I would'


def test_handle_gotta():
    """
    Test the handler pipeline for "gotta", ensuring "have/has"
    prefixing.
    """
    span1 = _get_contraction_span('I gotta go see about a girl.', 'gotta')
    result1 = handle_gotta(span1)
    assert result1 is not None
    assert result1[0] == 'have got to'

    span2 = _get_contraction_span("It's gotta be the shoes.", 'gotta')
    result2 = handle_gotta(span2)
    assert result2 is not None
    assert result2[0] == 'got to'

    span3 = _get_contraction_span(
        "We've gotta hold on to what we've got.", 'gotta'
    )
    result3 = handle_gotta(span3)
    assert result3 is not None
    assert result3[0] == 'got to'


def test_handle_negation_standard():
    """Test standard negation expansions."""
    span = _get_contraction_span("Mama couldn't be persuaded.", "couldn't")
    result = handle_negation(span)
    assert result is not None
    expanded, _ = result
    assert expanded == 'could not'


def test_handle_negation_inverted():
    """Test inverted negation expansions (questions/fragments)."""
    span = _get_contraction_span(
        "Didn't I blow your mind this time?", "Didn't"
    )
    result = handle_negation(span)
    assert result is not None
    expanded, _ = result
    assert expanded == 'Did I not'


def test_handle_s():
    """Test the full handler pipeline for ''s' contractions."""
    span = _get_contraction_span("Here's Johnny", "Here's")
    result = handle_s(span)
    assert result is not None
    assert result[0] == 'Here is'


def test_handle_wanna():
    """Test the full handler pipeline for 'wanna' contractions."""
    span = _get_contraction_span('I wanna dance with somebody.', 'wanna')
    result = handle_wanna(span)
    assert result is not None
    assert result[0] == 'want to'


def test_handle_whatcha():
    """Test the full handler pipeline for whatcha expansion."""
    span = _get_contraction_span("Whatcha doin'?", 'Whatcha')
    result = handle_whatcha(span)
    assert result is not None
    assert result[0] == 'What are you'
