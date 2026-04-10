"""Tests for the global application context."""

from textwarp._core.context import TextwarpContext
from textwarp._core.providers.en.provider import EnglishProvider


def test_context_default_initialization():
    """Verify that the context initializes with English defaults."""
    ctx = TextwarpContext()

    assert ctx.locale == 'en'
    assert isinstance(ctx.provider, EnglishProvider)


def test_context_set_locale_en():
    """Verify setting the locale explicitly to English."""
    ctx = TextwarpContext()
    ctx.set_locale('EN')

    assert ctx.locale == 'en'
    assert isinstance(ctx.provider, EnglishProvider)


def test_context_set_locale_fallback():
    """
    Verify that an unsupported locale safely falls back to English.
    """
    ctx = TextwarpContext()
    ctx.set_locale('fr')

    assert ctx.locale == 'en'
    assert isinstance(ctx.provider, EnglishProvider)
