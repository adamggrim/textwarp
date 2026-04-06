"""Custom exceptions for clipboard and validation errors."""

__all__ = [
    'CaseNotFoundError',
    'EmptyClipboardError',
    'InvalidCaseNameError',
    'NoCaseNameError',
    'NoRegexError',
    'NoTextError',
    'RegexNotFoundError',
    'TextNotFoundError',
    'TextwarpValidationError',
    'WhitespaceCaseNameError',
    'WhitespaceClipboardError'
]


class TextwarpValidationError(Exception):
    """Base class for all textwarp validation errors."""


class CaseNotFoundError(TextwarpValidationError):
    """Exception raised when the provided case is not found in the
    searched text."""


class EmptyClipboardError(TextwarpValidationError):
    """Exception raised when the clipboard is empty."""


class InvalidCaseNameError(TextwarpValidationError):
    """Exception raised when the provided case name string is
    invalid."""


class NoRegexError(TextwarpValidationError):
    """Exception raised when the provided regex string is empty."""


class NoCaseNameError(TextwarpValidationError):
    """Exception raised when the provided case name string is empty."""


class NoTextError(TextwarpValidationError):
    """Exception raised when the provided text string is empty."""


class RegexNotFoundError(TextwarpValidationError):
    """Exception raised when the provided regex string is not found in
    the searched text."""


class TextNotFoundError(TextwarpValidationError):
    """Exception raised when the provided text to replace is not found
    in the searched text."""


class WhitespaceCaseNameError(TextwarpValidationError):
    """Exception raised when the case name contains only whitespace."""


class WhitespaceClipboardError(TextwarpValidationError):
    """Exception raised when the clipboard contains only whitespace."""
