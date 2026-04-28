"""Tests for lazy spaCy loading and text processing."""

import pytest
import spacy

from textwarp._core.enums import ModelPriority
from textwarp._lib.nlp import _get_nlp, extract_words_from_doc, process_as_doc


def test_extract_words_from_doc():
    """Test extracting words from a string."""
    text = "I'm sorry, Dave. I'm afraid I can't do that."
    doc = process_as_doc(text)

    words = extract_words_from_doc(doc)

    expected_words = [
        'i',
        "'m",
        'sorry',
        'dave',
        'i',
        "'m",
        'afraid',
        'i',
        'ca',
        "n't",
        'do',
        'that'
    ]

    assert words == expected_words

    assert ',' not in words
    assert '.' not in words
    assert '  ' not in words


def test_process_as_doc_disable_pipes():
    """Test that specific pipeline components can be disabled."""
    doc = process_as_doc('Close the pod bay doors.', disable=['parser'])

    assert not doc.has_annotation('DEP')


def test_process_as_doc_from_doc():
    """
    Test that passing an existing `Doc` returns the `Doc` unmodified.
    """
    original_doc = process_as_doc('Daisy, Daisy, give me your answer do.')
    returned_doc = process_as_doc(original_doc)

    assert original_doc is returned_doc


def test_process_as_doc_from_string():
    """Test that a string is converted into a spaCy `Doc`."""
    test_string = (
        'This mission is too important for me to allow you to jeopardize it.'
    )
    doc = process_as_doc(test_string)

    assert hasattr(doc, 'text')
    assert doc.text == (
        'This mission is too important for me to allow you to jeopardize it.'
    )


def test_get_nlp_priority_branching():
    """
    Test that `_get_nlp` respects the `ModelPriority` enum and
    successfully returns a `Language` object for both branches.
    """
    nlp_speed = _get_nlp(model_priority=ModelPriority.SPEED)
    nlp_accuracy = _get_nlp(model_priority=ModelPriority.ACCURACY)

    assert nlp_speed is not None
    assert nlp_accuracy is not None


def test_nlp_fallback_logic(monkeypatch):
    """
    Mock `spacy.util.is_package` to simulate a missing `sm` model
    and verify it tries the next in ranking.
    """
    def mock_is_package(name):
        if name == 'en_core_web_sm':
            return False
        if name == 'en_core_web_md':
            return True
        return False

    monkeypatch.setattr(spacy.util, 'is_package', mock_is_package)
    monkeypatch.setattr(
        'textwarp._lib.nlp._load_spacy_model', lambda x: f'loaded_{x}'
    )

    result = _get_nlp(model_priority=ModelPriority.SPEED)
    assert result == 'loaded_en_core_web_md'


def test_nlp_no_models_found_raises_runtime_error(monkeypatch):
    """
    Verify the error message if the user has no spaCy models installed.
    """
    monkeypatch.setattr(spacy.util, 'is_package', lambda x: False)
    monkeypatch.setattr(spacy.util, 'get_installed_models', lambda: [])

    with pytest.raises(RuntimeError, match='No EN spaCy models found.'):
        _get_nlp(model_priority=ModelPriority.SPEED)


def test_process_as_doc_with_disabled_pipes():
    """Ensure that pipes are disabled when requested."""
    doc = process_as_doc('xf', disable=['parser', 'ner'])

    assert not doc.has_annotation('DEP')
    assert not doc.has_annotation('ENT_IOB')
