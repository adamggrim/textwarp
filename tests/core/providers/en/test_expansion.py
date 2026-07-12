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
    span = get_contraction_span('He’d like to come and meet us', 'He’d')

    expansion, end_idx = _expand_ambiguous_contraction('He’d', span)

    assert expansion == 'He would'
    assert end_idx == span.end_char


def test_expand_idiomatic_phrases_casing():
    phrase = ('Ain’t Got No, I Got Life.')
    expanded = _expand_idiomatic_phrases(phrase)

    assert expanded == ('Ain’t Got Any, I Got Life.')


def test_expand_unambiguous_contraction():
    unambiguous_map = get_unambiguous_map()

    assert _expand_unambiguous_contraction(
        'won’t', unambiguous_map
    ) == 'will not'

    assert _expand_unambiguous_contraction(
        'shouldn’t’ve', unambiguous_map
    ) == 'should not have'
    assert _expand_unambiguous_contraction(
        'Shouldn’t’ve', unambiguous_map
    ) == 'Should not have'


def test_expand_contractions():
    text = (
        'Ain’t it just like the night to play tricks when you’re trying to be '
        'so quiet?'
    )
    doc = process_as_doc(text)

    result = expand_contractions(doc)

    assert result == (
        'Is it not just like the night to play tricks when you are trying to '
        'be so quiet?'
    )


def test_expand_contractions_no_matches():
    text = (
        'I exist as I am, that is enough.'
    )
    doc = process_as_doc(text)

    result = expand_contractions(doc)

    assert result == text
