from spacy.tokens import Token

from ..._config import UNAMBIGUOUS_CONTRACTIONS_MAP
from .._quote_conversion import curly_to_straight
from .._string_capitalization import capitalize_from_string


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
    # Handle empty strings.
    if not original_text or not expanded_text:
        return expanded_text

    # Check for all caps.
    if original_text.isupper():
        return expanded_text.upper()

    original_parts: list[str] = original_text.split()
    expanded_parts: list[str] = expanded_text.split()

    # Check for title case.
    if all(part[0].isupper() for part in original_parts):
        return ' '.join([
            capitalize_from_string(part) for part in expanded_parts
        ])
    # Check for sentence case.
    elif original_text[0].isupper():
        return ' '.join([
            capitalize_from_string(
                part,
                lowercase_by_default=True
            ) for part in expanded_parts
        ])
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


def negative_contraction_to_base_verb(contraction: str) -> str:
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

