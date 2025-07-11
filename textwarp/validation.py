class EmptyClipboardError(Exception):
    """Exception raised when the clipboard is empty."""


def validate_clipboard(clipboard: str) -> None:
    """
    Validate the clipboard input.

    This function checks if the clipboard content is an empty string.

    Args:
        clipboard: A string representing the content of the clipboard.

    Raises:
        EmptyClipboardError: If the clipboard string is empty.
    """
    if clipboard == '':
        raise EmptyClipboardError('Clipboard is empty.')
