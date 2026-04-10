"""Tests for the main contraction expansion engine."""

from textwarp._lib.contractions import expand_contractions
from textwarp._lib.nlp import process_as_doc


def test_expand_contractions_no_contractions():
    """Test that text without contractions remains unchanged."""
    text = (
        'This mission is too important for me to allow you to jeopardize it.'
    )
    doc = process_as_doc(text)
    assert expand_contractions(doc) == text


def test_expand_contractions_ambiguous():
    """Test expansion of ambiguous contractions requiring handlers."""
    doc = process_as_doc(
        "There's a starman waitin' in the sky\n"
        "He'd like to come and meet us\n"
        "But he thinks he'd blow our minds\n"
        "There's a starman waitin' in the sky\n"
        "He's told us not to blow it\n"
        "'Cause he knows it's all worthwhile\n"
    )
    result = expand_contractions(doc)
    assert result == (
        "There is a starman waitin' in the sky\n"
        'He would like to come and meet us\n'
        'But he thinks he would blow our minds\n'
        "There is a starman waitin' in the sky\n"
        'He has told us not to blow it\n'
        'Because he knows it is all worthwhile\n'
    )


def test_expand_contractions_unambiguous():
    """Test expansion of straightforward dictionary-mapped contractions."""
    doc = process_as_doc("They won't go when I go.")
    result = expand_contractions(doc)
    assert result == 'They will not go when I go.'


def test_expand_contractions_inverted_and_multiple():
    """Test expansion of multiple contractions while respecting case."""
    doc = process_as_doc(
        "Ain't it just like the night to play\n"
        "Tricks when you're trying to be so quiet?"
    )
    result = expand_contractions(doc)
    assert result == (
        'Is it not just like the night to play\n'
        'Tricks when you are trying to be so quiet?'
    )


def test_expand_contractions_chained():
    """Test expansion of chained contractions."""
    doc = process_as_doc("I shouldn't've said that. I should not have said that.")
    result = expand_contractions(doc)
    assert result == 'I should not have said that. I should not have said that.'
