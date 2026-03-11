"""Tests for contraction utility functions."""

from textwarp._lib.contractions.utils import (
    apply_expansion_casing,
    find_subject_token,
    get_negative_contraction_base_verb
)
from textwarp._lib.nlp import process_as_doc


def test_apply_expansion_casing_lower():
    """Test that lowercase is preserved."""
    assert apply_expansion_casing("can't", "can not") == "can not"


def test_apply_expansion_casing_upper():
    """Test that all-caps is preserved."""
    assert apply_expansion_casing("CAN'T", "can not") == "CAN NOT"


def test_apply_expansion_casing_sentence():
    """Test that sentence casing (first letter capitalized) is applied."""
    assert apply_expansion_casing("Won't", "will not") == "Will not"
    assert apply_expansion_casing("Couldn't've", "could not have") == "Could not have"


def test_apply_expansion_casing_title():
    """Test that title case is preserved across the expanded words."""
    assert apply_expansion_casing("Do Not", "do not") == "Do Not"


def test_get_negative_contraction_base_verb():
    """Test the extraction of base verbs from negative contractions."""
    assert get_negative_contraction_base_verb("won't") == 'will'
    assert get_negative_contraction_base_verb("shan't") == 'shall'
    assert get_negative_contraction_base_verb("cannot") == 'can'
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
