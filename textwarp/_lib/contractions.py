"""Main logic for expanding contractions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Doc

from textwarp._core.context import ctx

__all__ = ['expand_contractions']


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
