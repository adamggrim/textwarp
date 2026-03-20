"""Tests for lazy spaCy loading and text processing."""

from textwarp._lib.nlp import process_as_doc, extract_words_from_doc


def test_process_as_doc_from_string():
    """Test that a string is converted into a spaCy Doc."""
    doc = process_as_doc('This is a test.')

    assert hasattr(doc, 'text')
    assert doc.text == 'This is a test.'


def test_process_as_doc_from_doc():
    """Test that passing an existing Doc returns the Doc unmodified."""
    original_doc = process_as_doc('Another test.')
    returned_doc = process_as_doc(original_doc)

    assert original_doc is returned_doc


def test_extract_words_from_doc():
    """Test extracting words from a string."""
    text = "I'm sorry, Dave. I'm afraid I can't do that."
    doc = process_as_doc(text)

    words = extract_words_from_doc(doc)

    expected_words = [
        'i', "'m", 'sorry', 'dave', 'i', "'m", 'afraid', 'i', 'ca',
        "n't", 'do', 'that'
    ]

    assert words == expected_words

    assert "," not in words
    assert "." not in words
    assert "  " not in words
