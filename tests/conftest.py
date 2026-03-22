"""Tests for global fixtures and configurations."""

import pytest
from spacy.tokens import Span

from textwarp._lib.nlp import _nlp_instances
from textwarp._lib.nlp import process_as_doc


@pytest.fixture
def get_contraction_span():
    """
    Fixture that returns a helper function to extract the spaCy `Span`
    for a given contraction in a string.
    """
    def _get_span(text: str, contraction: str) -> Span:
        doc = process_as_doc(text)
        start_char = text.lower().find(contraction.lower())
        end_char = start_char + len(contraction)
        span = doc.char_span(start_char, end_char)
        assert span is not None, (
            f"Could not map '{contraction}' to a Span in '{text}'"
        )
        return span

    return _get_span


@pytest.fixture(autouse=True)
def mock_clipboard(monkeypatch):
    """
    Mock pyperclip for all tests to protect the system clipboard.

    This fixture replaces the actual pyperclip module with a mock
    that stores data in memory.
    """
    class MockClipboard:
        content = ''

        @classmethod
        def copy(cls, text):
            cls.content = text

        @classmethod
        def paste(cls):
            return cls.content

    monkeypatch.setattr('pyperclip.copy', MockClipboard.copy)
    monkeypatch.setattr('pyperclip.paste', MockClipboard.paste)

    return MockClipboard


@pytest.fixture
def simulate_input(monkeypatch):
    """Simulate a sequence of user inputs."""
    def _setup_input(inputs):
        input_iterator = iter(inputs)
        monkeypatch.setattr('builtins.input', lambda: next(input_iterator))
    return _setup_input


@pytest.fixture(autouse=True)
def reset_nlp_cache():
    """Reset the spaCy model cache before or after tests."""
    yield
    _nlp_instances.clear()
