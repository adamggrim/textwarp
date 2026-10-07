"""Tests for English-specific logic for expanding contractions."""

from textwarp._core.providers.en.data.contraction_expansion import (
    get_unambiguous_map
)
from textwarp._core.providers.en.expansion.core import (
    _expand_ambiguous_contraction,
    _expand_idioms,
    _expand_unambiguous_contraction,
    expand_contractions
)
from textwarp._lib.nlp import process_as_doc


def test_expand_ambiguous_contraction(get_contraction_span):
    span = get_contraction_span('He’d like to come and meet us', 'He’d')

    expansion, end_idx = _expand_ambiguous_contraction('He’d', span)

    assert expansion == 'He would'
    assert end_idx == span.end_char


def test_expand_idioms_casing():
    phrase = ('Ain’t Got No, I Got Life.')
    expanded = _expand_idioms(phrase)

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
    original = (
        'Ain’t That a Shame'
    )
    doc = process_as_doc(original)

    result = expand_contractions(doc)

    assert result == (
        'Is That Not a Shame'
    )


def test_expand_contractions_no_matches():
    original = (
        'I exist as I am, that is enough.'
    )
    doc = process_as_doc(original)

    result = expand_contractions(doc)

    assert result == original
