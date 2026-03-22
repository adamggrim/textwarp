"""Strategy pattern classes containing language-specific logic."""

from textwarp._core.providers.base import LanguageProvider
from textwarp._core.providers.en import EnglishProvider

__all__ = [
    'LanguageProvider',
    'EnglishProvider'
]
