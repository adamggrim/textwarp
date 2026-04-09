"""Tests for the LanguageProvider abstract base class."""

import pytest

from textwarp._core.providers.base import LanguageProvider


def test_language_provider_cannot_be_instantiated():
    """
    Verify that the `LanguageProvider` abstract base class cannot be
    instantiated directly.
    """
    with pytest.raises(
        TypeError, match="Can't instantiate abstract class LanguageProvider"
    ):
        LanguageProvider()


def test_incomplete_subclass_cannot_be_instantiated():
    """
    Verify that a subclass missing abstract properties cannot be
    instantiated.
    """
    class IncompleteProvider(LanguageProvider):
        def cardinal_to_ordinal(self, text: str) -> str:
            return text

    with pytest.raises(
        TypeError, match="Can't instantiate abstract class IncompleteProvider"
    ):
        IncompleteProvider()
