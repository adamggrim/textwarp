class ClipboardError(Exception):
    """Base class for clipboard exceptions."""
    pass


class EmptyClipboardError(ClipboardError):
    """Exception raised when the clipboard is empty."""


class NonTextClipboardError(ClipboardError):
    """Exception raised when the clipboard content is not text."""
    pass


def validate_clipboard(clipboard: str) -> None:
    """
    Validate the clipboard input.

    This function checks if the clipboard content is an empty string or
    not a string at all.

    Args:
        clipboard: A string representing the content of the clipboard.

    Raises:
        EmptyClipboardError: If the clipboard string is empty.
        NonTextClipboardError: If the clipboard content is not a string.
    """
    if clipboard == '':
        raise EmptyClipboardError('Clipboard is empty.')

    if not isinstance(clipboard, str):
        raise NonTextClipboardError('Clipboard content is not text.')
