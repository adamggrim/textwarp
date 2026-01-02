"""Functions for spaCy-based entity capitalization."""

from spacy.tokens import (
    Doc,
    Span,
    Token
)

from .._config import LOWERCASE_PARTICLES
from .._constants import (
    PROPER_NOUN_ENTITIES,
    TITLE_CASE_TAG_EXCEPTIONS
)
from .._constants import WarpingPatterns

__all__ = [
    'map_proper_noun_entities',
    'should_capitalize_pos_or_length'
]


def _should_always_lowercase(token: Token) -> bool:
    """
    Determine if a token should always be lowercase.

    This occurs when it is a lowercase particle (e.g., "de", "von") or a
    contraction suffix (e.g., "'ve", "n't").

    Args:
        token: The spaCy token to check.

    Returns:
        bool: ``True`` if the token should always be lowercase, otherwise
            ``False``.
    """
    return (token.text.lower() in LOWERCASE_PARTICLES or
        WarpingPatterns.CONTRACTION_SUFFIXES_PATTERN
        .fullmatch(token.text))


def map_proper_noun_entities(doc: Doc) -> dict[int, tuple[Span, int]]:
    """
    Create a map of specific indices for proper noun entities to Span objects
    and end indices from a spaCy ``Doc``.

    Args:
        doc: The spaCy ``Doc`` to convert.

    Returns:
        dict[int, tuple[Span, int]]: A dictionary where each key is an
            entity's start token index and each value is a tuple
            containing the entity's spaCy Span object and its end token
            index.
    """
    return {
        ent.start: (ent, ent.end) for ent in doc.ents
        if ent.label_ in PROPER_NOUN_ENTITIES
    }


def should_capitalize_pos_or_length(token: Token) -> bool:
    """
    Determine whether a spaCy token should be capitalized for title
    case based on its part of speech or length.

    Args:
        token: The spaCy token to check.

    Returns:
        bool: ``True`` if the tag should be capitalized, otherwise
            ``False``.
    """
    if _should_always_lowercase(token):
        return False
    # Capitalize long words regardless of POS tag.
    if len(token.text) >= 5:
        return True

    return token.tag_ not in TITLE_CASE_TAG_EXCEPTIONS
