"""Tests for custom exceptions."""

import pytest
import regex as re

from textwarp._core.exceptions import (
    CaseNotFoundError,
    EmptyClipboardError,
    InvalidCaseNameError,
    NoCaseNameError,
    NoRegexError,
    NoTextError,
    RegexNotFoundError,
    TextNotFoundError,
    WhitespaceCaseNameError,
    WhitespaceClipboardError
)


@pytest.mark.parametrize('exception_class', [
    CaseNotFoundError,
    EmptyClipboardError,
    InvalidCaseNameError,
    NoCaseNameError,
    NoRegexError,
    NoTextError,
    RegexNotFoundError,
    TextNotFoundError,
    WhitespaceCaseNameError,
    WhitespaceClipboardError
])
def test_exceptions_inherit_from_base_exception(exception_class):
    """
    Verify that all custom exceptions inherit from the base `Exception`
    class.
    """
    assert issubclass(exception_class, Exception)


def test_exception_msgs():
    """
    Verify that exceptions can be raised with custom literary messages.
    """

    with pytest.raises(EmptyClipboardError, match=re.escape(
        "Nothing will come of nothing."
    )):
        raise EmptyClipboardError('Nothing will come of nothing.')

    with pytest.raises(NoTextError, match=re.escape(
        'It is a tale\n'
        'Told by an idiot, full of sound and fury,\n'
        'Signifying nothing.'
    )):
        raise NoTextError(
            'It is a tale\n'
            'Told by an idiot, full of sound and fury,\n'
            'Signifying nothing.'
        )

    with pytest.raises(
        TextNotFoundError, match=re.escape(
            "I still haven't found what I'm looking for."
        )
    ):
        raise TextNotFoundError("I still haven't found what I'm looking for.")
