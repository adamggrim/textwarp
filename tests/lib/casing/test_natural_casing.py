"""Tests for converting between cases."""

from textwarp._lib.casing.natural_casing import to_natural_case
from textwarp._core.enums import Casing
from textwarp._lib.nlp import process_as_doc


def test_to_natural_case_sentence():
    """Test applying sentence case to a spaCy Doc."""
    doc = process_as_doc('I HAVE NO MOUTH, AND I MUST SCREAM.')
    result = to_natural_case(doc, Casing.SENTENCE)
    assert result == 'I have no mouth, and i must scream.'

    doc_mixed = process_as_doc(
        'start writing. short sentences. describe it. just describe it.'
    )
    result_mixed = to_natural_case(doc_mixed, Casing.SENTENCE)
    assert result_mixed == (
        'Start writing. Short sentences. Describe it. Just describe it.'
    )


def test_to_natural_case_start():
    """Test applying start case to a spaCy Doc."""
    doc = process_as_doc('not that innocent')
    result = to_natural_case(doc, Casing.START)
    assert result == 'Not That Innocent'


def test_to_natural_case_title():
    """Test applying title case to a spaCy Doc."""
    doc = process_as_doc(
        'the tragical history of the life and death of doctor faustus'
    )
    result = to_natural_case(doc, Casing.TITLE)

    assert 'The Tragical History' in result
    assert 'of the Life' in result
    assert 'and Death' in result
    assert 'of Doctor Faustus' in result
