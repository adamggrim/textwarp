"""Functions for spaCy-based entity capitalization."""

import regex as re
from spacy.tokens import (
    Doc,
    Span
)

from .._config import (
    get_absolute_entities_map,
    get_contextual_entities_map,
)
from .._constants import PROPER_NOUN_ENTITIES
from .._types import CapitalizationContext

__all__ = [
    'map_proper_noun_entities',
    'should_capitalize_pos_or_length'
]


def _check_for_ngrams(
    doc: Doc,
    index: int,
    ngrams: list[str],
    context_window: int = 5
) -> bool:
    """
    Check if any of a given list of ngrams are present around a
    specific index in the Doc.

    Args:
        doc: The spaCy ``Doc`` to check.
        index: The index around which to check for ngrams.
        ngrams: A list of ngrams to check for.
        context_window: The size of the window around the index to
            check. Defaults to 5.

    Returns:
        bool: ``True`` if any ngram is found, otherwise ``False``.
    """
    start = max(0, index - context_window)
    end = min(len(doc), index + context_window + 1)
    context_text = doc[start:end].text.lower()

    for ngram in ngrams:
        pattern = r'(?<!\w)' + re.escape(ngram.lower()) + r'(?!\w)'
        if re.search(pattern, context_text):
            return True

    return False


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
    Map standard entities in a spaCy ``Doc``.

    Args:
        doc: The spaCy ``Doc`` to convert.

    Returns:
        dict[int, tuple[Span, int, None]]: A dictionary where each key
            is an entity's start token index and each value is a tuple
            containing:
                1. The entity's spaCy ``Span`` object.
                2. The entity's end token index.
                3. ``None`` (no forced casing).

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
