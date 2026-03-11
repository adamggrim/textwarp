"""Tests for spaCy-based token capitalization."""

from textwarp._lib.casing.token_casing import should_capitalize_pos_or_length
from textwarp._lib.nlp import process_as_doc


def test_should_capitalize_lowercase_particles():
    """
    Test that particles like "von" and "de" are flagged to stay lowercase.
    """
    doc = process_as_doc('Maria Augusta von Trapp')
    von_token = doc[2]

    assert von_token.text.lower() == 'von'
    assert should_capitalize_pos_or_length(von_token) is False


def test_should_capitalize_contraction_suffixes():
    """
    Test that contraction suffixes are flagged to stay lowercase.
    """
    doc = process_as_doc("don't, don't")
    nt_token = doc[4]

    assert nt_token.text.lower() == "n't"
    assert should_capitalize_pos_or_length(nt_token) is False


def test_should_capitalize_length():
    """
    Test that words five characters or longer are capitalized
    regardless of part of speech.
    """
    doc = process_as_doc('about')
    token = doc[0]

    assert len(token.text) >= 5
    assert should_capitalize_pos_or_length(token) is True


def test_should_capitalize_pos_exception():
    """Test that specific short parts of speech are lowercased."""
    doc = process_as_doc('and')
    token = doc[0]

    assert token.pos_ in ('CCONJ', 'CONJ') or token.tag_ == 'CC'
    assert should_capitalize_pos_or_length(token) is False


def test_should_capitalize_normal():
    """Test that standard nouns and verbs are capitalized."""
    doc = process_as_doc('seitan')
    token = doc[0]

    assert should_capitalize_pos_or_length(token) is True
