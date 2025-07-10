class EmptyClipboardError(Exception):
    """Exception raised when the clipboard is empty."""


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
