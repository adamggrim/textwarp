"""
Utilities for applying casing and finding contraction subjects and
verbs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Token

from textwarp._core.config import ContractionExpansion
from textwarp._lib.casing.case_conversion import find_first_alphabetical_idx
from textwarp._lib.casing.string_casing import case_from_string
from textwarp._lib.punctuation import curly_to_straight

__all__ = [
    'apply_expansion_casing',
    'find_subject_token',
    'negative_contraction_to_base_verb'
]


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

    # Handle empty strings.
    if not original_text or not expanded_text:
        return expanded_text

    # Check for all caps.
    if original_text.isupper():
        return expanded_text.upper()

    original_parts: list[str] = original_text.split()
    expanded_parts: list[str] = expanded_text.split()

    is_title_case = (
        len(original_parts) > 1 and
        all(_starts_capitalized(part) for part in original_parts)
    )

    # Check for title case.
    if is_title_case:
        return ' '.join([
            case_from_string(part) for part in expanded_parts
        ])

    # Check for sentence case.
    if _starts_capitalized(original_text):
        first_part: str = case_from_string(expanded_parts[0])

        remaining_parts = [
            case_from_string(part, lowercase_by_default=True)
            for part in expanded_parts[1:]
        ]

        return ' '.join([first_part] + remaining_parts)

    # Otherwise, return the original ``expanded_text`` casing.
    return expanded_text


def find_subject_token(verb_token: Token | None) -> Token | None:
    """
    Find the subject of a verb in a spaCy ``Doc``, handling both
    standard order (subject to the left: e.g., "I don't") and inverted
    order (subject to the right: e.g., "Don't I").

    This function attempts to use the dependency parser first. If the
    parser fails (common in questions or fragments), it falls back to
    positional heuristics.

    Args:
        verb_token | None: The token for the verb that predicates the subject,
            otherwise ``None``.

    Returns:
        Token | None: The subject token, otherwise ``None``.
    """
    if verb_token is None:
        return None

    doc = verb_token.doc

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


def negative_contraction_to_base_verb(contraction: str) -> str | None:
    """
    Determine the base verb from a standard negative contraction (e.g.,
    "won't" -> "will").

    Args:
        contraction: The contraction to analyze.

    Returns:
        str | None: The base verb corresponding to the contraction,
            otherwise ``None``.
    """
    straight_contraction = curly_to_straight(contraction).lower()

    # Look for the contraction in the unambiguous contractions map.
    expanded_contraction = ContractionExpansion.get_unambiguous_map().get(
        straight_contraction
    )

    if expanded_contraction:
        # "Cannot" is a special case.
        if expanded_contraction == 'cannot':
            return 'can'
        # Return the first word of the expansion.
        return expanded_contraction.split()[0]

    # Only attempt to strip if "n't" is actually present.
    if straight_contraction.endswith("n't"):
        # Fallback for edge cases: strip n't
        return straight_contraction.replace("n't", '')

    return None
