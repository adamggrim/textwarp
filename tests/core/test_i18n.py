import logging

from textwarp._cli.constants.messages import EXIT_MSG
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


def test_n_marker_returns_original_string():
    """Verify that the `N_` dummy marker avoids mutating strings."""
    test_str = 'Traduttore, traditore'
    assert N_(test_str) == test_str
