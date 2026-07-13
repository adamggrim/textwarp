"""Custom exceptions for clipboard and validation errors."""

__all__ = [
    'CaseNotFoundError',
    'EmptyClipboardError',
    'InvalidCaseNameError',
    'InvalidRegexError',
    'MissingModelError',
    'NoCaseNameError',
    'NoRegexError',
    'NoTextError',
    'RegexNotFoundError',
    'TextNotFoundError',
    'TextwarpError',
    'TextwarpValidationError',
    'WhitespaceCaseNameError',
    'WhitespaceClipboardError'
]


class TextwarpError(Exception):
    """Base class for all textwarp errors."""


class TextwarpValidationError(TextwarpError):
    """Base class for all textwarp validation errors."""


class CaseNotFoundError(TextwarpValidationError):
    """
    Exception raised when the provided case is not found in the searched
    text.
    """


class EmptyClipboardError(TextwarpValidationError):
    """Exception raised when the clipboard is empty."""


class InvalidCaseNameError(TextwarpValidationError):
    """
    Exception raised when the provided case name string is invalid.
    """


class InvalidRegexError(TextwarpValidationError):
    """
    Exception raised when the provided regular expression string is not
    a valid regular expression.
    """


class MissingModelError(TextwarpError):
    """Exception raised when a required spaCy model is not installed."""


class NoRegexError(TextwarpValidationError):
    """Exception raised when the provided regex string is empty."""


class NoCaseNameError(TextwarpValidationError):
    """Exception raised when the provided case name string is empty."""


class NoTextError(TextwarpValidationError):
    """Exception raised when the provided text string is empty."""


class RegexNotFoundError(TextwarpValidationError):
    """
    Exception raised when the provided regex string is not found in the
    searched text.
    """


class TextNotFoundError(TextwarpValidationError):
    """
    Exception raised when the provided text to replace is not found in
    the searched text.
    """


class WhitespaceCaseNameError(TextwarpValidationError):
    """Exception raised when the case name contains only whitespace."""


class WhitespaceClipboardError(TextwarpValidationError):
    """Exception raised when the clipboard contains only whitespace."""
