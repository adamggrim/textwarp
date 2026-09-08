"""Tests for converting between natural cases."""

from textwarp._lib.casing.natural_casing import to_natural_case
from textwarp._core.enums import Casing
from textwarp._lib.nlp import process_as_doc


def test_to_natural_case_sentence():
    doc_uppercase = process_as_doc('HURRY UP PLEASE ITS TIME.')
    result = to_natural_case(doc_uppercase, Casing.SENTENCE)
    assert result == 'Hurry up please its time.'

    doc_mixed = process_as_doc(
        'what happens is a continual surrender of himself as he is at the '
        'moment to something which is more valuable. the progress of an '
        'artist is a continual self-sacrifice, a continual extinction of '
        'personality.'
    )
    result_mixed = to_natural_case(doc_mixed, Casing.SENTENCE)
    assert result_mixed == (
        'What happens is a continual surrender of himself as he is at the '
        'moment to something which is more valuable. The progress of an '
        'artist is a continual self-sacrifice, a continual extinction of '
        'personality.'
    )

    doc_sentence = process_as_doc('The Love Song of J. Alfred Prufrock.')
    result = to_natural_case(doc_sentence, Casing.SENTENCE)

    assert result == 'The Love Song of J. Alfred Prufrock.'


def test_to_natural_case_start():
    doc = process_as_doc('of man’s first disobedience')
    result = to_natural_case(doc, Casing.START)
    assert result == 'Of Man’s First Disobedience'


def test_to_natural_case_title():
    doc = process_as_doc(
        'the tragical history of the life and death of doctor faustus'
    )
    result = to_natural_case(doc, Casing.TITLE)

    assert 'The Tragical History' in result
    assert 'of the Life' in result
    assert 'and Death' in result
    assert 'of Doctor Faustus' in result
