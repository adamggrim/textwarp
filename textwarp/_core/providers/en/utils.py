"""English-specific utility functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Token

from textwarp._core.providers import en
from textwarp._lib.punctuation import curly_to_straight

__all__ = [
    'find_subject_token',
    'get_negative_contraction_base_verb'
]


def find_subject_token(verb_token: Token | None) -> Token | None:
    """
    Find the subject of a verb in a spaCy `Doc`, handling both
    standard order (subject to the left: e.g., "I don't") and inverted
    order (subject to the right: e.g., "Don't I").

    This function attempts to use the dependency parser first. If the
    parser fails (common in questions or fragments), it falls back to
    positional heuristics.

    Args:
        verb_token | None: The token for the verb that predicates the subject;
            otherwise `None`.

    Returns:
        Token | None: The subject token, otherwise `None`.
    """
    if verb_token is None:
        return None

    doc = verb_token.doc

    for child in verb_token.children:
        if child.dep_ in {'nsubj', 'nsubjpass'}:
            return child

    if verb_token.dep_ in {'aux', 'auxpass'}:
        for child in verb_token.head.children:
            if child.dep_ in {'nsubj', 'nsubjpass'}:
                return child

    # Fallback A: Look immediately before the verb (standard order).
    curr_idx = verb_token.i - 1

    for curr_idx in range(verb_token.i - 1, -1, -1):
        candidate = doc[curr_idx]
        if candidate.pos_ in en.constants.SUBJECT_POS_TAGS:
            return candidate
        if candidate.pos_ in en.constants.LEFT_SEARCH_STOP_TAGS:
            break

        curr_idx -= 1

    # Fallback B: Look immediately after the suffix (inverted order).
    start_idx = verb_token.i + 1
    if start_idx < len(doc) and doc[start_idx].lower_ == "n't":
        start_idx += 1

    end_idx = min(start_idx + 6, len(doc))

    for j in range(start_idx, end_idx):
        candidate = doc[j]

        if candidate.pos_ in en.constants.SUBJECT_POS_TAGS:
            return candidate
        if candidate.pos_ in en.constants.RIGHT_SEARCH_STOP_TAGS:
            break

    return None


def get_negative_contraction_base_verb(contraction: str) -> str | None:
    """
    Determine the base verb from a standard negative contraction (e.g.,
    "won't" -> "will").

    Args:
        contraction: The contraction to analyze.

    Returns:
        str | None: The base verb corresponding to the contraction;
            otherwise `None`.
    """
    straight_contraction = curly_to_straight(contraction).lower()

    if straight_contraction == 'cannot':
        return 'can'

    expanded_contraction = (
        en.data.contraction_expansion.get_unambiguous_map().get(
            straight_contraction
        )
    )

    if expanded_contraction:
        if expanded_contraction == 'cannot':
            return 'can'
        return expanded_contraction.split()[0]

    if straight_contraction.endswith("n't"):
        return straight_contraction.replace("n't", '')

    return None
