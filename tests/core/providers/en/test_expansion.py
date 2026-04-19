'''Tests for English-specific logic for expanding contractions.'''

from textwarp._core.providers.en.data.contraction_expansion import (
    get_unambiguous_map
)
from textwarp._core.providers.en.expansion import (
    _expand_ambiguous_contraction,
    _expand_idiomatic_phrases,
    _expand_unambiguous_contraction,
    expand_contractions
)
from textwarp._lib.nlp import process_as_doc


def test_expand_ambiguous_contraction(get_contraction_span):
    '''Test expansion of an ambiguous contraction using handlers.'''
    span = get_contraction_span("He'd like to come and meet us", "He'd")

    expansion, end_idx = _expand_ambiguous_contraction("He'd", span)

    assert expansion == 'He would'
    assert end_idx == span.end_char


def test_expand_ambiguous_contraction_unmatched(get_contraction_span):
    '''
    Test that an unmatched or unhandled ambiguous contraction returns
    the original string.
    '''
    span = get_contraction_span("They daren't go.", "daren't")

    expansion, end_idx = _expand_ambiguous_contraction("daren't", span)

    assert expansion == "daren't"
    assert end_idx == span.end_char


def test_expand_idiomatic_phrases_casing():
    '''
    Test that idiomatic phrase expansions preserve original casing.
    '''
    phrase = ("Ain’t Got No, I Got Life.")
    expanded = _expand_idiomatic_phrases(phrase)

    assert expanded == ("Ain’t Got Any, I Got Life.")


def test_expand_unambiguous_contraction():
    '''Test that unambiguous dictionary contractions properly expand.'''
    unambiguous_map = get_unambiguous_map()

    assert _expand_unambiguous_contraction(
        "won't", unambiguous_map
    ) == 'will not'

    assert _expand_unambiguous_contraction(
        "shouldn't've", unambiguous_map
    ) == 'should not have'
    assert _expand_unambiguous_contraction(
        "Shouldn't've", unambiguous_map
    ) == 'Should not have'


def test_expand_contractions():
    '''Test the full expansion pipeline on a spaCy `Doc`.'''
    text = (
        "Ain't it just like the night to play tricks when you're trying to be "
        'so quiet?'
    )
    doc = process_as_doc(text)

    result = expand_contractions(doc)

    assert result == (
        'Is it not just like the night to play tricks when you are trying to '
        'be so quiet?'
    )


def test_expand_contractions_no_matches():
    '''Test that a `Doc` with no contractions returns unmodified.'''
    text = (
        'This mission is too important for me to allow you to jeopardize it.'
    )
    doc = process_as_doc(text)

    result = expand_contractions(doc)

    assert result == text
