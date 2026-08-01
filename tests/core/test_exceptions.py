"""Tests for custom exceptions."""

import pytest
import regex as re

from textwarp._core.exceptions import (
    CaseNotFoundError,
    EmptyClipboardError,
    InvalidCaseNameError,
    InvalidRegexError,
    NoCaseNameError,
    NoRegexError,
    NoTextError,
    RegexNotFoundError,
    TextNotFoundError,
    TextwarpValidationError,
    WhitespaceCaseNameError,
    WhitespaceClipboardError
)


@pytest.mark.parametrize('exception_class', [
    CaseNotFoundError,
    EmptyClipboardError,
    InvalidCaseNameError,
    InvalidRegexError,
    NoCaseNameError,
    NoRegexError,
    NoTextError,
    RegexNotFoundError,
    TextNotFoundError,
    TextwarpValidationError,
    WhitespaceCaseNameError,
    WhitespaceClipboardError
])
def test_exceptions_inherit_from_base_exception(exception_class):
    assert issubclass(exception_class, Exception)


@pytest.mark.parametrize('exception_class, error_msg', [
    (EmptyClipboardError, 'Nothing will come of nothing.'),
    (
        NoTextError,
        'It is a tale\nTold by an idiot, full of sound and fury,\n'
        'Signifying nothing.'
    ),
    (
        TextNotFoundError,
        'I found myself within a forest dark,\n'
        'For the straightforward pathway had been lost.'
    )
])
def test_exception_msgs(exception_class, error_msg):
    with pytest.raises(exception_class, match=re.escape(error_msg)):
        raise exception_class(error_msg)
