
from ._constants import CASE_NAMES_MAP
from ._exceptions import (
    EmptyClipboardError,
    WhitespaceClipboardError,
)
from .warping import (
    to_camel_case,
    to_dot_case,
    to_kebab_case,
    to_pascal_case,
    to_snake_case
)


# Mapping of valid case name inputs to their standardized names.
CASE_NAMES_MAP: Final[dict[str, Callable[[str], str]]]= {
    'camel': to_camel_case,
    'camel case': to_camel_case,
    'dot': to_dot_case,
    'dot case': to_dot_case,
    'lower': str.lower,
    'lowercase': str.lower,
    'kebab': to_kebab_case,
    'kebab case': to_kebab_case,
    'pascal': to_pascal_case,
    'pascal case': to_pascal_case,
    'snake': to_snake_case,
    'snake case': to_snake_case,
    'upper': str.upper,
    'uppercase': str.upper,
}


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
