"""Universal utility functions."""

__all__ = ['find_first_alphabetical_idx']


def find_first_alphabetical_idx(text: str) -> int | None:
    """
    Find the index of the first alphabetical character in a string.

    Args:
        text: The string to search.

    Returns:
        int | None: The index of the first alphabetical character, or
            `None` if there are no alphabetical characters.
    """
    for i, char in enumerate(text):
        if char.isalpha():
            return i
    return None
