"""Tests for resolving ambiguous contractions based on context."""

from spacy.tokens import Span
from textwarp._lib.contractions.disambiguation import (
    disambiguate_ain_t,
    disambiguate_d,
    disambiguate_gotta,
    disambiguate_s,
    disambiguate_wanna,
    disambiguate_whatcha
)
from textwarp._lib.nlp import process_as_doc


def _get_contraction_span(text: str, contraction: str) -> Span:
    """
    Helper function to extract the spaCy ``Span`` for a given
    contraction in a string.
    """
    doc = process_as_doc(text)
    start_char = text.lower().find(contraction.lower())
    end_char = start_char + len(contraction)
    span = doc.char_span(start_char, end_char)
    assert span is not None, (
        f"Could not map '{contraction}' to a Span in '{text}'"
    )
    return span


def test_disambiguate_ain_t():
    """Test 'ain't' disambiguation based on subject and verb tense."""
    assert disambiguate_ain_t(_get_contraction_span(
        "I ain't no fortunate son.", "ain't"
    )) == 'am'
    assert disambiguate_ain_t(_get_contraction_span(
        "He ain't heavy, he's my brother.", "ain't"
    )) == 'is'
    assert disambiguate_ain_t(_get_contraction_span(
        "You ain't nothing but a hound dog.", "ain't"
    )) == 'are'
    assert disambiguate_ain_t(_get_contraction_span(
        "Ain't got no life", "ain't"
    )) == 'has'
    assert disambiguate_ain_t(_get_contraction_span(
        "You ain't seen nothing like me yet.", "ain't"
    )) == 'have'


def test_disambiguate_d():
    """Test "'d." disambiguation."""
    assert disambiguate_d(_get_contraction_span(
        "I'd do anything for love.", "I'd"
    )) == 'would'
    assert disambiguate_d(_get_contraction_span(
        "They'd seen his face before\n"
        "Nobody was really sure if he was from the House of Lords.", "They'd"
    )) == 'had'
    assert disambiguate_d(_get_contraction_span(
        "Why'd you have to rain on my parade?", "Why'd"
    )) == 'did'
    assert disambiguate_d(_get_contraction_span(
        "Guys, you know you'd better watch out.", "you'd"
    )) == 'had'


def test_disambiguate_gotta():
    """Test "gotta" disambiguation."""
    assert disambiguate_gotta(_get_contraction_span(
        "'Cause I gotta have faith.", 'gotta'
    )) == 'to'
    assert disambiguate_gotta(_get_contraction_span(
        "I gotta feelin.'.", 'gotta'
    )) == 'a'


def test_disambiguate_s():
    """Test "'s" disambiguation."""
    assert disambiguate_s(_get_contraction_span(
        "She's a woman who understands.", "She's"
    )) == 'is'
    assert disambiguate_s(_get_contraction_span(
        "It's been 14 years.", "It's")) == "has"
    assert disambiguate_s(_get_contraction_span(
        "Let's go girls.", "Let's"
    )) == 'us'
    assert disambiguate_s(_get_contraction_span(
        "How's it feel to be on your own?", "How's"
    )) == 'does'


def test_disambiguate_wanna():
    """Test "wanna" disambiguation."""
    assert disambiguate_wanna(_get_contraction_span(
        'I wanna hold your hand.', 'wanna'
    )) == 'to'
    assert disambiguate_wanna(_get_contraction_span(
        'You wanna piece of me?', 'wanna'
    )) == 'a'


def test_disambiguate_whatcha():
    """Test "whatcha" disambiguation."""
    assert disambiguate_whatcha(_get_contraction_span(
        "Chill out, whatcha yellin' for?", 'whatcha'
    )) == 'are'
    assert disambiguate_whatcha(_get_contraction_span(
        "Show 'em whatcha got.", 'whatcha'
    )) == 'have'
    assert disambiguate_whatcha(_get_contraction_span(
        "Tell me whatcha want, whatcha really, really want.", 'whatcha'
    )) == 'do'
