"""Tests for global fixtures and configurations."""

import pytest

from textwarp._lib.nlp import _nlp_instances


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
