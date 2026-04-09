import logging

from textwarp._cli.constants.messages import EXIT_MESSAGE
from textwarp._core.context import N_, ctx


def test_set_locale_to_unsupported_falls_back_to_en(caplog):
    """
    Verify that an unsupported language triggers a warning and stays on
    English.
    """
    ctx.set_locale('en')

    with caplog.at_level(logging.WARNING):
        ctx.set_locale('egy')

    assert "Warning: Language 'egy' is not supported." in caplog.text
    assert ctx.locale == 'en'


def test_gettext_translation_install():
    """Verify that gettext is properly installed in the environment."""
    assert isinstance(EXIT_MESSAGE, str)
    assert EXIT_MESSAGE != 'NO_EXIT'
    assert 'Exiting' in EXIT_MESSAGE


def test_n_marker_returns_original_string():
    """Verify that the `N_` dummy marker avoids mutating strings."""
    test_str = 'Rumpelstiltskin'
    assert N_(test_str) == test_str
