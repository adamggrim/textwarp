class CaseNotFoundError(Exception):
    """Exception raised when the provided case is not found in the
    searched text."""


class EmptyClipboardError(Exception):
    """Exception raised when the clipboard is empty."""


class InvalidCaseNameError(Exception):
    """Exception raised when the provided case name string is
    invalid."""


class NoRegexError(Exception):
    """Exception raised when the provided regex string is empty."""


class NoCaseNameError(Exception):
    """Exception raised when the provided case name string is empty."""


class NoTextError(Exception):
    """Exception raised when the provided text string is empty."""


class RegexNotFoundError(Exception):
    """Exception raised when the provided regex string is not found in
    the searched text."""


class TextToReplaceNotFoundError(Exception):
    """Exception raised when the provided text to replace is not found
    in the searched text."""


class WhitespaceCaseNameError(Exception):
    """Exception raised when the case name contains only whitespace."""


class WhitespaceClipboardError(Exception):
    """Exception raised when the clipboard contains only whitespace."""
