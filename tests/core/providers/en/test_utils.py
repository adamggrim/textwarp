"""Tests for contraction utility functions."""

from textwarp._core.providers.en.utils import (
    find_subject_token,
    get_negative_contraction_base_verb
)
from textwarp._lib.nlp import process_as_doc


def test_get_negative_contraction_base_verb():
    """Test the extraction of base verbs from negative contractions."""
    assert get_negative_contraction_base_verb("won't") == 'will'
    assert get_negative_contraction_base_verb("shan't") == 'shall'
    assert get_negative_contraction_base_verb('cannot') == 'can'
    assert get_negative_contraction_base_verb("can't") == 'can'
    assert get_negative_contraction_base_verb("didn't") == 'did'
    assert get_negative_contraction_base_verb("hasn't") == 'has'
    assert get_negative_contraction_base_verb("doesn't") == 'does'


def test_find_subject_token_standard_order():
    """Test finding the subject when it precedes the verb."""
    doc = process_as_doc("We don't need no education.")
    verb_token = doc[1]
    subject = find_subject_token(verb_token)

    assert subject is not None
    assert subject.text == 'We'


def test_find_subject_token_inverted_order():
    """Test finding the subject when it follows the verb."""
    doc = process_as_doc("Isn't she lovely?")
    verb_token = doc[0]
    subject = find_subject_token(verb_token)

    assert subject is not None
    assert subject.text.lower() == 'she'
