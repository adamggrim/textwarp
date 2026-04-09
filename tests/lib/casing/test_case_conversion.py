"""Tests for converting between cases."""

from textwarp._lib.casing.case_conversion import (
    change_first_letter_case,
    doc_to_case,
    to_separator_case,
    word_to_pascal
)
from textwarp._core.enums import CaseSeparator, Casing
from textwarp._lib.nlp import process_as_doc


def test_change_first_letter_case():
    """Test changing only the first alphabetical character's case."""
    assert change_first_letter_case('101 dalmations', str.upper) == (
        '101 Dalmations'
    )
    assert change_first_letter_case('bang', str.upper) == 'Bang'
    assert change_first_letter_case('WHIMPER', str.lower) == 'wHIMPER'
    assert change_first_letter_case('!!!', str.upper) == '!!!'


def test_word_to_pascal():
    """Test converting a single word to PascalCase."""
    assert word_to_pascal('451') == '451'
    assert word_to_pascal('PascalCase') == 'PascalCase'
    assert word_to_pascal('camelCase') == 'CamelCase'
    assert word_to_pascal('case') == 'Case'


def test_to_separator_case_basic():
    """Test converting standard spaced text to separator cases."""
    assert to_separator_case('bell jar', CaseSeparator.SNAKE) == 'bell_jar'
    assert to_separator_case('bell jar', CaseSeparator.KEBAB) == 'bell-jar'
    assert to_separator_case('bell jar', CaseSeparator.DOT) == 'bell.jar'


def test_to_separator_case_existing_cases():
    """
    Test converting from existing programming cases to a new separator case.
    """
    assert to_separator_case(
        'existence-precedes-essence', CaseSeparator.SNAKE
    ) == 'existence_precedes_essence'
    assert to_separator_case(
        'being.nothingness', CaseSeparator.KEBAB
    ) == 'being-nothingness'
    assert to_separator_case(
        'deBeauvoir', CaseSeparator.SNAKE
    ) == 'de_beauvoir'
    assert to_separator_case(
        'LeMytheDeSisyphe', CaseSeparator.DOT
    ) == 'le.mythe.de.sisyphe'


def test_to_separator_case_non_alpha():
    """Test that separator casing safely handles numbers and symbols."""
    assert to_separator_case('April 4th 1984', CaseSeparator.SNAKE) == 'april_4th_1984'


def test_doc_to_case_sentence():
    """Test applying sentence case to a spaCy Doc."""
    doc = process_as_doc('I HAVE NO MOUTH, AND I MUST SCREAM.')
    result = doc_to_case(doc, Casing.SENTENCE)
    assert result == 'I have no mouth, and i must scream.'

    doc_mixed = process_as_doc(
        'start writing. short sentences. describe it. just describe it.'
    )
    result_mixed = doc_to_case(doc_mixed, Casing.SENTENCE)
    assert result_mixed == (
        'Start writing. Short sentences. Describe it. Just describe it.'
    )


def test_doc_to_case_start():
    """Test applying start case to a spaCy Doc."""
    doc = process_as_doc('not that innocent')
    result = doc_to_case(doc, Casing.START)
    assert result == 'Not That Innocent'


def test_doc_to_case_title():
    """Test applying title case to a spaCy Doc."""
    doc = process_as_doc(
        'the tragical history of the life and death of doctor faustus'
    )
    result = doc_to_case(doc, Casing.TITLE)

    assert 'The Tragical History' in result
    assert 'of the Life' in result
    assert 'and Death' in result
    assert 'of Doctor Faustus' in result
