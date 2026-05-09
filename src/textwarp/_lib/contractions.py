"""Main logic for expanding contractions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Doc

from textwarp._core.context import ctx
from textwarp._core.utils import find_first_alphabetical_idx
from textwarp._lib.casing.string_casing import case_from_string

__all__ = ['expand_contractions']


def apply_expansion_casing(
    original_text: str,
    expanded_text: str
) -> str:
    """
    Apply the original text casing to the expanded text.

    Args:
        original_text: The original text.
        expanded_text: The expanded text (not yet cased).

    Returns:
        str: The expanded text in the original text's casing.
    """
    def _starts_capitalized(text: str) -> bool:
        """
        Check if the first alphabetical character in the text is
        uppercase.
        """
        idx = find_first_alphabetical_idx(text)
        return idx is not None and text[idx].isupper()

    if not original_text or not expanded_text:
        return expanded_text

    if original_text.isupper():
        return expanded_text.upper()
    if original_text.islower():
        return expanded_text.lower()

    original_parts: list[str] = original_text.split()
    expanded_parts: list[str] = expanded_text.split()

    is_title_case = (
        len(original_parts) > 1
        and all(_starts_capitalized(part) for part in original_parts)
    )

    if is_title_case:
        return ' '.join(case_from_string(part) for part in expanded_parts)

    if _starts_capitalized(original_text):
        first_part: str = case_from_string(expanded_parts[0])

        remaining_parts = [
            case_from_string(part, lowercase_by_default=True)
            for part in expanded_parts[1:]
        ]

        return ' '.join([first_part] + remaining_parts)

    return expanded_text


def expand_contractions(doc: Doc) -> str:
    """
    Expand all contractions in a given spaCy `Doc` using the active
    language provider.

    Args:
        doc: A spaCy `Doc`.

    Returns:
        str: The converted `Doc` text.
    """
    return ctx.provider.expand_contractions(doc)
