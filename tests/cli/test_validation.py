"""Tests for command-line input and clipboard validation."""

import pytest

from textwarp._cli.validation import (
    validate_case_name,
    validate_clipboard,
    validate_regex,
    validate_text
)
from textwarp._core.exceptions import (
    EmptyClipboardError,
    InvalidCaseNameError,
    InvalidRegexError,
    NoCaseNameError,
    NoRegexError,
    NoTextError,
    WhitespaceCaseNameError,
    WhitespaceClipboardError
)


def test_validate_case_name():
    validate_case_name('camel')
    validate_case_name('snake case')
    validate_case_name('PASCAL')

    with pytest.raises(NoCaseNameError):
        validate_case_name('')

    with pytest.raises(WhitespaceCaseNameError):
        validate_case_name('   ')

    with pytest.raises(InvalidCaseNameError):
        validate_case_name('Jarndyce and Jarndyce')


def test_validate_clipboard():
    validate_clipboard(
        'The knowledge and survey of vice is in this world so necessary to '
        'the constituting of human virtue.'
    )

    with pytest.raises(EmptyClipboardError):
        validate_clipboard('')

    with pytest.raises(WhitespaceClipboardError):
        validate_clipboard('   \n \t  ')


def test_validate_regex():
    validate_regex(r'^[a-z]+$')
    validate_regex(r'(?<=madeleine)À la recherche du temps perdu')

    with pytest.raises(NoRegexError):
        validate_regex('')

    with pytest.raises(InvalidRegexError):
        validate_regex(r'[They do not move')


def test_validate_text():
    validate_text('Truth will out.')
    validate_text(' ')

    with pytest.raises(NoTextError):
        validate_text('')
