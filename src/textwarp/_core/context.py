"""Thread-safe global context for the active locale and provider."""

import contextvars
import gettext
import logging
import os
import importlib
from pathlib import Path
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from textwarp._core.providers.base import LanguageProvider

__all__ = ['ctx', 'N_']

_ = gettext.gettext

logger = logging.getLogger(__name__)

SUPPORTED_LOCALES: Final[frozenset[str]] = frozenset({'en'})

_active_locale: contextvars.ContextVar[str] = contextvars.ContextVar(
    'locale', default='en'
)
_active_provider: contextvars.ContextVar[
    'LanguageProvider | None'
] = contextvars.ContextVar('provider', default=None)


class TextwarpContext:
    """
    Manage the active language locale and its corresponding provider
    safely across threads.
    """
    def __init__(self) -> None:
        """
        Initialize the context with the default locale and provider.
        """
        self._set_up_gettext()

    @property
    def locale(self) -> str:
        """Get the active language locale."""
        return _active_locale.get()

    @locale.setter
    def locale(self, value: str) -> None:
        """Set the active language locale."""
        _active_locale.set(value)

    @property
    def _provider(self) -> 'LanguageProvider | None':
        """Get the active language provider, or `None` if not set."""
        return _active_provider.get()

    @_provider.setter
    def _provider(self, value: 'LanguageProvider | None') -> None:
        """Set the active language provider."""
        _active_provider.set(value)

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
        requested_locale = locale.lower()
        fallback_triggered = False

        if requested_locale not in SUPPORTED_LOCALES:
            requested_locale = 'en'
            fallback_triggered = True

        self.locale = requested_locale

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
            # Fallback for when the `SUPPORTED_LOCALES` check passed but
            # the module failed to load.
            from textwarp._core.providers.en.provider import EnglishProvider
            self._provider = EnglishProvider()

        self._set_up_gettext()

        if fallback_triggered:
            msg = _(
                "Warning: Language '{locale}' is not supported. Falling back "
                'to English.'
            ).format(locale=locale)
            logger.warning(msg)

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


ctx = TextwarpContext()


def N_(message: str) -> str:
    """Dummy marker for gettext string extraction."""
    return message
