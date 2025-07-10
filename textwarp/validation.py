class ClipboardError(Exception):
    """Base class for clipboard exceptions."""
    pass


class EmptyClipboardError(ClipboardError):
    """Exception raised when the clipboard is empty."""


class NonTextClipboardError(ClipboardError):
    """Exception raised when the clipboard content is not text."""
    pass

