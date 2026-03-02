"""Tests for command-line input and clipboard validation."""

import pytest
import regex as re

from textwarp._cli.validation import (
    validate_any_text,
    validate_case_name,
    validate_clipboard,
    validate_regex,
    validate_text
)
from textwarp._core.exceptions import (
    EmptyClipboardError,
    InvalidCaseNameError,
    NoCaseNameError,
    NoRegexError,
    NoTextError,
    WhitespaceCaseNameError,
    WhitespaceClipboardError
)


def test_validate_any_text():
    """
    Test that validate_any_text accepts all strings without raising.
    """
    validate_any_text('Valid text')
    validate_any_text('   ')
    validate_any_text('')


def test_validate_case_name():
    """Test case name validation."""
    validate_case_name('camel')
    validate_case_name('snake case')
    validate_case_name('PASCAL')

    with pytest.raises(NoCaseNameError):
        validate_case_name('')

    with pytest.raises(WhitespaceCaseNameError):
        validate_case_name('   ')

    with pytest.raises(InvalidCaseNameError):
        validate_case_name('invalid_case_format')


def test_validate_clipboard():
    """Test clipboard validation."""
    validate_clipboard('Valid clipboard data')

    with pytest.raises(EmptyClipboardError):
        validate_clipboard('')

    with pytest.raises(WhitespaceClipboardError):
        validate_clipboard('   \n \t  ')


def test_validate_regex():
    """Test regular expression validation."""
    validate_regex(r'^[a-z]+$')
    validate_regex(r'(?<=foo)bar')

    with pytest.raises(NoRegexError):
        validate_regex('')

    with pytest.raises(re.error):
        validate_regex(r'[unclosed group')


def test_validate_text():
    """Test general text validation."""
    validate_text('Some valid text to replace')
    validate_text(' ')

    with pytest.raises(NoTextError):
        validate_text('')
