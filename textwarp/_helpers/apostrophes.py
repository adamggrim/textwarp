from .._constants import WarpingPatterns

__all__ = ['remove_apostrophes']


def remove_apostrophes(text: str) -> str:
    """
    Remove apostrophes from a string without removing single quotes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return WarpingPatterns.APOSTROPHE_IN_WORD.sub('', text)
