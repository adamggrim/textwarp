"""Function for capitalizing strings through dictionary lookup."""

from textwarp._core.context import ctx

__all__ = ['case_from_string']


def case_from_string(
    word: str,
    lowercase_by_default: bool = False,
    preserve_mixed_case: bool = True
) -> str:
    """
    Capitalize a word according to the active language provider's
    specific rules.

    Args:
        word: The word to capitalize.
        lowercase_by_default: Whether to lowercase the word if no
            capitalization strategy applies. Defaults to `False`.
        preserve_mixed_case: Whether to preserve mixed-case words.
            Defaults to `True`.

    Returns:
        str: The capitalized word.
    """
    return ctx.provider.case_from_string(
        word,
        lowercase_by_default=lowercase_by_default,
        preserve_mixed_case=preserve_mixed_case
    )
