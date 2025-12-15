from spacy.tokens import (
    Doc,
    Token
)

from ..._config import UNAMBIGUOUS_CONTRACTIONS_MAP
from .._quote_conversion import curly_to_straight


def apply_expansion_casing(original_word: str, expanded_word: str) -> str:
    """
    Apply the original word casing to the expanded word.

    Args:
        original_word: The original word.
        expanded_word: The cased word.

    Returns:
        str: The expanded word in the original word's casing.
    """
    if original_word.isupper():
        return expanded_word.upper()
    elif original_word.istitle():
        return expanded_word.capitalize()
    return expanded_word


def find_subject_token(verb_token: Token) -> Token | None:
    """
    Find the subject of a verb in a spaCy ``Doc``, handling both
    standard order (subject to the left: e.g., "I don't") and inverted
    order (subject to the right: e.g., "Don't I").

    This function attempts to use the dependency parser first. If the
    parser fails (common in questions or fragments), it falls back to
    positional heuristics.

    Args:
        verb_token: The token for the verb that predicates the subject.

    Returns:
        Token | None: The subject token, otherwise ``None``.
    """
    doc: Doc = verb_token.doc

    # Try to find the subject using the dependency parser.
    for child in verb_token.children:
        if child.dep_ in ('nsubj', 'nsubjpass'):
            return child

    # Fallback A: Look immediately before the verb (standard order).
    curr_idx = verb_token.i - 1
    while curr_idx >= 0:
        candidate = doc[curr_idx]

        if candidate.pos_ in ('PRON', 'PROPN', 'NOUN'):
            return candidate
        # Stop if the loop hits a determiner, verb, or punctuation.
        if candidate.pos_ in ('DET', 'VERB', 'PUNCT'):
            break

        # Otherwise, move one step left to skip adverbs.
        curr_idx -= 1

    # Fallback B: Look immediately after the suffix (inverted order).
    start_idx = verb_token.i + 1
    if start_idx < len(doc) and doc[start_idx].lower_ == "n't":
        start_idx += 1

    end_idx = min(start_idx + 6, len(doc))

    for j in range(start_idx, end_idx):
        candidate = doc[j]

        if candidate.pos_ in ('PRON', 'PROPN', 'NOUN'):
            return candidate
        # Stop if the loop hits a verb or punctuation.
        if candidate.pos_ in ('VERB', 'PUNCT'):
            break

    return None


def negative_contraction_to_base_verb(contraction: str) -> str:
    """
    Determine the base verb from a standard negative contraction (e.g.,
    "won't" -> "will").

    Args:
        contraction: The contraction to analyze.

    Returns:
        str: The base verb corresponding to the contraction.
    """
    straight_contraction = curly_to_straight(contraction).lower()

    # Look for the contraction in the unambiguous contractions map.
    expanded_contraction = UNAMBIGUOUS_CONTRACTIONS_MAP.get(
        straight_contraction, ''
    )

    if not expanded_contraction:
        # Fallback for edge cases: strip n't
        return straight_contraction.replace("n't", '')

    # "Cannot" is a special case.
    if expanded_contraction == 'cannot':
        return 'can'

    # Return the first word of the expansion.
    return expanded_contraction.split()[0]

