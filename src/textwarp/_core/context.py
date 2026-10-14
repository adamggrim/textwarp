"""Thread-safe global context for the active locale and provider."""

import contextvars
import gettext
import importlib
import importlib.resources
import logging
from functools import cache
from typing import TYPE_CHECKING, Final, cast

if TYPE_CHECKING:
    from textwarp._core.providers.base import LanguageProvider

__all__ = ['N_', '_', 'ctx', 'ngettext']

logger = logging.getLogger(__name__)

SUPPORTED_LOCALES: Final[frozenset[str]] = frozenset({'en'})

_active_locale: contextvars.ContextVar[str] = contextvars.ContextVar(
    'locale', default='en'
)
_active_provider: contextvars.ContextVar[
    'LanguageProvider | None'
] = contextvars.ContextVar('provider', default=None)


@cache
def _get_translations(locale: str) -> gettext.NullTranslations:
    """Load and cache the gettext translation object for a locale."""
    locales_resource = importlib.resources.files('textwarp').joinpath(
        'locales'
    )
    with importlib.resources.as_file(locales_resource) as locales_dir:
        return gettext.translation(
            'textwarp',
            localedir=str(locales_dir),
            languages=[locale],
            fallback=True
        )


@cache
def _get_provider_instance(requested_locale: str) -> 'LanguageProvider':
    """Load and cache the singleton LanguageProvider for a locale."""
    provider_module = importlib.import_module(
        f'textwarp._core.providers.{requested_locale}.provider'
    )
    class_name = f'{requested_locale.capitalize()}Provider'
    ProviderClass = getattr(provider_module, class_name, None)

    if ProviderClass:
        return cast('LanguageProvider', ProviderClass())

    for attr_name in dir(provider_module):
        attr = getattr(provider_module, attr_name)
        if (
            isinstance(attr, type)
            and attr.__name__.endswith('Provider')
            and attr.__name__ != 'LanguageProvider'
        ):
            return cast('LanguageProvider', attr())

    raise ImportError(
        _('No valid provider class found in {module}').format(
            module=provider_module
        )
    )


class TextwarpContext:
    """
    Manage the active language locale and its corresponding provider
    safely across threads.
    """
    @property
    def locale(self) -> str:
        """Get the active language locale."""
        return _active_locale.get()

    @locale.setter
    def locale(self, value: str) -> None:
        """Set the active language locale and reset the cached provider."""
        _active_locale.set(value)
        _active_provider.set(None)

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
        Lazy-load the language provider for the active locale to prevent
        circular imports.
        """
        if self._provider is None:
            self.set_locale(self.locale)
        assert self._provider is not None
        return self._provider

    def set_locale(self, locale: str) -> None:
        """
        Set the active language locale and initialize its provider.

        Args:
            locale: The language locale to set.
        """
        requested_locale = locale.lower()
        fallback_triggered = False

        try:
            provider_instance = _get_provider_instance(requested_locale)
            self.locale = requested_locale
            self._provider = provider_instance
        except (ImportError, ModuleNotFoundError):
            fallback_triggered = requested_locale not in SUPPORTED_LOCALES
            self.locale = 'en'
            self._provider = _get_provider_instance('en')

        if fallback_triggered:
            msg = _(
                "Warning: Language '{locale}' is not supported. Falling back "
                'to English.'
            ).format(locale=locale)
            logger.warning(msg)


ctx = TextwarpContext()


def _(message: str) -> str:
    """Translate a string using the active context locale."""
    return _get_translations(ctx.locale).gettext(message)


def ngettext(singular: str, plural: str, n: int) -> str:
    """
    Translate a pluralizable string using the active context locale.
    """
    return _get_translations(ctx.locale).ngettext(singular, plural, n)


def N_(message: str) -> str:
    """Dummy marker for gettext string extraction."""
    return message