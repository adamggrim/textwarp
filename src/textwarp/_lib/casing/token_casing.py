"""Logic for spaCy-based token capitalization."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Token

from textwarp._core.context import ctx

__all__ = ['should_capitalize_pos_or_length']


def should_capitalize_pos_or_length(token: Token) -> bool:
    """
    Determine whether to capitalize a spaCy `Token` for title case based
    on its part of speech or length.
    """
    return ctx.provider.should_capitalize_in_title(token)
