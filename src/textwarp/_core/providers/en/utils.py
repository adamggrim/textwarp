"""English-specific utility functions."""

from __future__ import annotations

from collections.abc import Container
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Doc, Token

from textwarp._core.enums import UniversalPOSTag
from textwarp._core.providers import en
from textwarp._lib.punctuation import curly_to_straight

__all__ = [
    'find_subject_end_token',
    'find_subject_token',
    'get_negative_contraction_base_verb',
    'get_next_lexical_token',
    'get_prev_lexical_token',
]


def _is_demonstrative_subject(token: Token) -> bool:
    """
    Determine if a token is a demonstrative pronoun ('that', 'this')
    acting as a subject before a determiner (e.g., 'Ain't That a
    Shame').
    """
    doc = token.doc
    return (
        token.lower_ in en.constants.DEMONSTRATIVE_PRONOUNS
        and token.i + 1 < len(doc)
        and doc[token.i + 1].pos_ == UniversalPOSTag.DET
    )


def find_subject_end_token(subject_token: Token) -> Token:
    """
    Find the final token of a subject phrase in an inverted contraction.
    """
    if subject_token.pos_ in {UniversalPOSTag.PRON, UniversalPOSTag.DET}:
        return subject_token

    doc = subject_token.doc

    while (
        subject_token.dep_ in en.constants.SUBJECT_MODIFIER_DEP_TAGS
        and subject_token.head.i > subject_token.i
    ):
        subject_token = subject_token.head

    subject_end_token = subject_token.right_edge

    while subject_end_token.i + 1 < len(doc):
        next_token = doc[subject_end_token.i + 1]
        if next_token.dep_ in en.constants.COMPOUND_DEP_TAGS or (
            next_token.is_title
            and subject_end_token.is_title
            and next_token.pos_ not in {
                UniversalPOSTag.VERB,
                UniversalPOSTag.AUX
            }
        ):
            subject_end_token = next_token
        else:
            break

    return subject_end_token


def find_subject_token(verb_token: Token | None) -> Token | None:
    """
    Find the subject of a verb in a spaCy `Doc`, handling both
    standard order (subject to the left: `I don't`) and inverted order
    (subject to the right: `Don't I`).

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

    # Find the index immediately after the contraction suffix.
    right_start_idx = verb_token.i + 1
    if (
        right_start_idx < len(doc)
        and doc[right_start_idx].lower_
        in en.expansion.variants.N_T_SUFFIX_VARIANTS
    ):
        right_start_idx += 1

    dep_candidates = list(verb_token.children)
    if verb_token.dep_ in en.constants.AUX_DEP_TAGS:
        dep_candidates.extend(verb_token.head.children)

    for child in dep_candidates:
        if child.dep_ in en.constants.NSUBJ_DEP_TAGS:
            # If the parser found a subject to the right, ensure it did
            # not skip over an intervening demonstrative pronoun.
            if child.i > right_start_idx:
                for k in range(right_start_idx, child.i):
                    if _is_demonstrative_subject(doc[k]):
                        return doc[k]
            return child

    # Fallback A: Look immediately before the verb (standard order).
    for curr_idx in range(verb_token.i - 1, -1, -1):
        candidate = doc[curr_idx]
        if candidate.pos_ in en.constants.SUBJECT_POS_TAGS:
            return candidate
        if candidate.pos_ in en.constants.LEFT_SEARCH_STOP_TAGS:
            break

    # Fallback B: Look immediately after the suffix (inverted order).
    end_idx = min(right_start_idx + 6, len(doc))

    for j in range(right_start_idx, end_idx):
        candidate = doc[j]

        if (
            candidate.pos_ in en.constants.SUBJECT_POS_TAGS
            or _is_demonstrative_subject(candidate)
        ):
            return candidate
        if candidate.pos_ in en.constants.RIGHT_SEARCH_STOP_TAGS:
            break

    return None


def get_prev_lexical_token(
    doc: Doc,
    start_idx: int,
    skip_pos: Container[UniversalPOSTag] = frozenset(
        {UniversalPOSTag.PUNCT, UniversalPOSTag.SPACE}
    )
) -> Token | None:
    """
    Find the previous lexical token, skipping selected parts of speech.
    """
    for i in range(start_idx - 1, -1, -1):
        token = doc[i]
        if token.pos_ in skip_pos:
            continue
        return token
    return None


def get_negative_contraction_base_verb(contraction: str) -> str | None:
    """
    Determine the base verb from a standard negative contraction (e.g.,
    `won't` -> `will`).

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


def get_next_lexical_token(
    doc: Doc,
    start_idx: int,
    skip_pos: Container[UniversalPOSTag] = frozenset(
        {UniversalPOSTag.PUNCT, UniversalPOSTag.SPACE}
    )
) -> Token | None:
    """
    Find the next lexical token, skipping selected parts of speech.
    """
    for i in range(start_idx, len(doc)):
        token = doc[i]
        if token.pos_ in skip_pos:
            continue
        return token
    return None
