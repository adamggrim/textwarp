"""Global singleton for the active locale and provider."""

import gettext
import os
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from textwarp._core.providers.base import LanguageProvider

_ = gettext.gettext

__all__ = ['ctx']


class TextwarpContext:
    """
    Manage the active language locale and its corresponding provider.
    """

    def __init__(self) -> None:
        self.locale: str = 'en'
        self._provider: 'LanguageProvider | None' = None
        self._set_up_gettext()

    def _set_up_gettext(self) -> None:
        """Configure gettext for the active locale."""
        os.environ['LANGUAGE'] = self.locale
        locales_dir = Path(__file__).parent.parent.parent / 'locales'

        try:
            gettext.bindtextdomain('textwarp', str(locales_dir))
            gettext.textdomain('textwarp')
            translation = gettext.translation(
                'textwarp',
                localedir=str(locales_dir),
                languages=[self.locale],
                fallback=True
            )
            translation.install()
        except FileNotFoundError:
            pass

    @property
    def provider(self) -> 'LanguageProvider':
        """
        Lazy-load the language provider to prevent circular imports.
        """
        if self._provider is None:
            from textwarp._core.providers.en.provider import EnglishProvider
            self._provider = EnglishProvider()
        return self._provider

    def set_locale(self, locale: str) -> None:
        """
        Set the active language locale and initialize its provider.

        Args:
            locale: The language locale to set.
        """
        self.locale = locale.lower()
        import importlib

        try:
            provider_module = importlib.import_module(
                f'textwarp._core.providers.{self.locale}.provider'
            )

            class_name = f'{self.locale.capitalize()}Provider'
            ProviderClass = getattr(provider_module, class_name, None)

            if ProviderClass:
                self._provider = ProviderClass()
            else:
                for attr_name in dir(provider_module):
                    attr = getattr(provider_module, attr_name)
                    if (
                        isinstance(attr, type)
                        and attr.__name__.endswith('Provider')
                        and attr.__name__ != 'LanguageProvider'
                    ):
                        self._provider = attr()
                        break
                else:
                    raise ImportError(
                        _('No valid provider class found in {module}').format(
                            module=provider_module
                        )
                    )

        except (ImportError, ModuleNotFoundError):
            # Fallback to the English default.
            self.locale = 'en'
            from textwarp._core.providers.en.provider import EnglishProvider
            self._provider = EnglishProvider()

        self._set_up_gettext()

ctx = TextwarpContext()
