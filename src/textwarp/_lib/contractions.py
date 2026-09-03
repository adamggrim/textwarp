"""Main logic for expanding contractions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Doc, Span

from textwarp._core.context import ctx
from textwarp._core.utils import starts_uppercase
from textwarp._lib.casing.string_casing import case_from_string

__all__ = ['apply_expansion_casing', 'expand_contractions']


def apply_expansion_casing(
    original_text: str,
    expanded_text: str,
    span_context: Span | None = None
) -> str:
    """
    Apply the original text casing to the expanded text.

    Args:
        original_text: The original text.
        expanded_text: The expanded text (not yet cased).
        span_context: Optional spaCy `Span` context to determine casing.

    Returns:
        str: The expanded text in the original text's casing.
    """
    if not original_text or not expanded_text:
        return expanded_text

    if original_text.isupper():
        return expanded_text.upper()
    if original_text.islower():
        return expanded_text.lower()

    if span_context is not None:
        try:
            tokens = span_context.sent
        except ValueError:
            tokens = span_context.doc
        words = [t.text for t in tokens if t.is_alpha]
    else:
        words = original_text.split()

    expanded_parts = expanded_text.split()

    if len(words) > 1 and all(starts_uppercase(w) for w in words):
        return ' '.join(case_from_string(p) for p in expanded_parts)

    if starts_uppercase(original_text):
        return ' '.join(
            case_from_string(p, lowercase_by_default=bool(i))
            for i, p in enumerate(expanded_parts)
        )

    return expanded_text


def expand_contractions(doc: Doc) -> str:
    """
    Expand all contractions in a spaCy `Doc` using the active language
    provider.

    Args:
        doc: A spaCy `Doc`.

    Returns:
        str: The converted `Doc` text.
    """
    return ctx.provider.expand_contractions(doc)
