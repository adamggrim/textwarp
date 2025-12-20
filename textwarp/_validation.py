
from ._exceptions import (
    EmptyClipboardError,
    WhitespaceClipboardError,
)



def validate_clipboard(clipboard: str) -> None:
    """
    Validate the clipboard input.

    This function checks if the clipboard content is an empty string or
    contains only whitespace.

    Args:
        clipboard: A string representing the content of the clipboard.

    Raises:
        EmptyClipboardError: If the clipboard string is empty.
        WhitespaceClipboardError: If the clipboard string contains only
            whitespace.
    """
    if clipboard == '':
        raise EmptyClipboardError('Clipboard is empty.')
    elif clipboard.strip() == '':
        raise WhitespaceClipboardError('Clipboard contains only whitespace.')
