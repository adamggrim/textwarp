"""Global singleton for the active locale and provider."""

import gettext
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from textwarp._core.providers.base import LanguageProvider

__all__ = ['ctx']


class TextwarpContext:
    """
    Manage the active language locale and its corresponding provider.
    """

    def __init__(self) -> None:
        self.locale: str = 'en'
        self._provider: 'LanguageProvider | None' = None
        self._setup_gettext()

    @property
    def provider(self) -> 'LanguageProvider':
        """Lazy-load the language provider to prevent circular imports."""
        if self._provider is None:
            from textwarp._core.providers.en import EnglishProvider
            self._provider = EnglishProvider()
        return self._provider

    def set_locale(self, locale: str) -> None:
        """
        Set the active language locale and initialize its provider.

        Args:
            locale: The language locale to set.
        """
        self.locale = locale.lower()

        from textwarp._core.providers.en import EnglishProvider

        if self.locale == 'en':
            self._provider = EnglishProvider()
        else:
            # Fallback to the English default.
            self.locale = 'en'
            self._provider = EnglishProvider()

        self._setup_gettext()

    def _setup_gettext(self) -> None:
        """
        Configure the gettext translation bindings for the command line.
        """
        localedir = Path(__file__).parent.parent / 'locales'

        try:
            translation = gettext.translation(
                domain='textwarp',
                localedir=localedir,
                languages=[self.locale]
            )
            translation.install()
        except FileNotFoundError:
            # Fallback to the English default.
            gettext.install('textwarp')


ctx = TextwarpContext()
