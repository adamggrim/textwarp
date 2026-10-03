"""Custom exceptions for clipboard and validation errors."""

__all__ = [
    'EmptyClipboardError',
    'InvalidCaseNameError',
    'InvalidRegexError',
    'MissingDependencyError',
    'MissingModelError',
    'NoCaseNameError',
    'NoRegexError',
    'NoTextError',
    'TextwarpError',
    'TextwarpValidationError',
    'WhitespaceCaseNameError',
    'WhitespaceClipboardError'
]


class TextwarpError(Exception):
    """Base class for all textwarp errors."""


class TextwarpValidationError(TextwarpError):
    """Base class for all textwarp validation errors."""


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


class MissingDependencyError(TextwarpError):
    """
    Exception raised when a required optional dependency is not
    installed.
    """
    def __init__(
        self,
        package_name: str,
        feature_name: str,
        optional_dependency: str
    ) -> None:
        message = (
            f"Error: {feature_name} requires '{package_name}'. "
            f'Install it using: pip install textwarp[{optional_dependency}]'
        )
        super().__init__(message)


class MissingModelError(TextwarpError):
    """Exception raised when a required spaCy model is not installed."""


class NoRegexError(TextwarpValidationError):
    """Exception raised when the provided regex string is empty."""


class NoCaseNameError(TextwarpValidationError):
    """Exception raised when the provided case name string is empty."""


class NoTextError(TextwarpValidationError):
    """Exception raised when the provided text string is empty."""


class WhitespaceCaseNameError(TextwarpValidationError):
    """Exception raised when the case name contains only whitespace."""


class WhitespaceClipboardError(TextwarpValidationError):
    """Exception raised when the clipboard contains only whitespace."""
