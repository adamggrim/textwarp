"""Tests for lazy spaCy loading and text processing."""

from unittest.mock import MagicMock

import pytest
import spacy

from textwarp._core.enums import ModelPriority
from textwarp._lib.nlp import _get_nlp, process_as_doc


def test_process_as_doc_disable_pipes():
    doc = process_as_doc('Close the pod bay doors.', disable=['parser'])

    assert not doc.has_annotation('DEP')


def test_process_as_doc_from_doc():
    original_doc = process_as_doc(
        'I’m sorry, Dave. I’m afraid I can’t do that.'
    )
    returned_doc = process_as_doc(original_doc)

    assert original_doc is returned_doc


def test_process_as_doc_from_string():
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
    mock_is_package = MagicMock(side_effect=lambda name: name == 'en_core_web_md')
    mock_load_spacy = MagicMock(side_effect=lambda x: f'loaded_{x}')

    monkeypatch.setattr(spacy.util, 'is_package', mock_is_package)
    monkeypatch.setattr('textwarp._lib.nlp._load_spacy_model', mock_load_spacy)

    result = _get_nlp(model_priority=ModelPriority.SPEED)
    assert result == 'loaded_en_core_web_md'
    mock_is_package.assert_called()
    mock_load_spacy.assert_called_once_with('en_core_web_md')


def test_nlp_no_models_found_raises_missing_model_error(monkeypatch):
    from textwarp._core.exceptions import MissingModelError

    mock_is_package = MagicMock(return_value=False)
    mock_get_installed = MagicMock(return_value=[])

    monkeypatch.setattr(spacy.util, 'is_package', mock_is_package)
    monkeypatch.setattr(spacy.util, 'get_installed_models', mock_get_installed)

    with pytest.raises(MissingModelError, match='No EN spaCy models found.'):
        _get_nlp(model_priority=ModelPriority.SPEED)


def test_process_as_doc_with_disabled_pipes():
    doc = process_as_doc(
        'Daisy, Daisy, give me your answer do.', disable=['parser', 'ner']
    )

    assert not doc.has_annotation('DEP')
    assert not doc.has_annotation('ENT_IOB')


def test_load_spacy_raises_missing_dependency_error(monkeypatch):
    import builtins
    from textwarp._core.exceptions import MissingDependencyError
    from textwarp._lib.nlp import _load_spacy

    original_import = builtins.__import__

    def _import_side_effect(name, *args, **kwargs):
        if name == 'spacy':
            raise ImportError("No module named 'spacy'")
        return original_import(name, *args, **kwargs)

    mock_import = MagicMock(side_effect=_import_side_effect)
    monkeypatch.setattr(builtins, '__import__', mock_import)

    _load_spacy.cache_clear()

    with pytest.raises(
        MissingDependencyError,
        match="Error: NLP support requires 'spacy'."
    ):
        _load_spacy()
