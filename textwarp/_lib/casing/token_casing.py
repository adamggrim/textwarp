"""Logic for spaCy-based token capitalization."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Token

from textwarp._core.context import ctx

__all__ = ['should_capitalize_pos_or_length']


def _should_always_lowercase(token: Token) -> bool:
    """
    Determine if a token should always be lowercase.

    This occurs when it is a lowercase particle (e.g., "de", "von") or a
    contraction suffix (e.g., "'ve", "n't").

    Args:
        token: The spaCy `Token` to check.

    Returns:
        bool: `True` if the token should always be lowercase, otherwise
            `False`.
    """
    return ctx.provider.should_always_lowercase(token.text)


def should_capitalize_pos_or_length(token: Token) -> bool:
    """
    Determine whether a spaCy `Token` should be capitalized for title
    case based on its part of speech or length.

    Args:
        token: The spaCy `Token` to check.

    Returns:
        bool: `True` if the tag should be capitalized, otherwise
            `False`.
    """
    if _should_always_lowercase(token):
        return False
    # Capitalize long words regardless of part-of-speech tag.
    if len(token.text) >= 5:
        return True

    return token.tag_ not in ctx.provider.title_case_tag_exceptions
