"""Functions for resolving ambiguous contractions based on context."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Span

from textwarp._core.constants.nlp import NOUN_TAGS, PARTICIPLE_TAGS, SINGULAR_PRONOUNS
from textwarp._core.constants.variants import (
    AIN_T_SUFFIX_VARIANTS,
    APOSTROPHE_D_VARIANTS,
    APOSTROPHE_S_VARIANTS
)
from textwarp._core.constants.regexes import WarpingPatterns
from textwarp._lib.contractions.utils import find_subject_token

__all__ = [
    'disambiguate_ain_t',
    'disambiguate_s_or_d',
    'disambiguate_whatcha'
]


def disambiguate_ain_t(span: Span) -> str | None:
    """
    Disambiguate the base verb for a matched "ain't" contraction.

    This function assumes the "n't" ``Span`` has already been identified as
    an "ain't" contraction (preceded by "ai").

    Args:
        span: The spaCy ``Span`` containing the negation ("n't").

    Returns:
        str | None : The base verb for the "ain't" contraction.
    """
    doc = span.doc
    suffix_token = span[-1]

    verb_token = (doc[suffix_token.i - 1] if suffix_token.i > 0 else None)

    if verb_token is None:
        return None

    subject_token = find_subject_token(verb_token)

    subject_text: str = subject_token.lower_ if subject_token else ''
    subject_tag: str = subject_token.tag_ if subject_token else ''

    next_token = (
        doc[suffix_token.i + 1]
        if suffix_token.i < len(doc) - 1
        else None
    )
    # If "ain't" is followed by a participle (VBN) or past tense
    # (VBD), it functions as "have/has not". Otherwise, it functions
    # as "am/is/are not".
    is_perfect_tense: bool = (
        next_token and next_token.tag_ in PARTICIPLE_TAGS
    )

    if not subject_token:
        return None

    if is_perfect_tense:
        # Disambiguate "has not" vs. "have not".
        if (subject_text in SINGULAR_PRONOUNS or
            subject_tag in NOUN_TAGS):
            return 'has'
        else:
            return 'have'
    else:
        # Disambiguate "am not" vs. "is not" vs. "are not".
        if subject_text == 'i':
            return 'am'
        elif (subject_text in SINGULAR_PRONOUNS or
            subject_tag in NOUN_TAGS):
            return 'is'
        else:
            # e.g., "You ain't", "We ain't", "They ain't".
            return 'are'


def disambiguate_s_or_d(span: Span) -> str | None:
    """
    Disambiguate the base verb for a matched "'s" or "'d" contraction.

    This function assumes the ``Span`` has already been identified as an
    "'s" or "'d" contraction.

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        str | None: The expanded version of the matched contraction, otherwise
            ``None``.
    """
    doc = span.doc
    suffix_token = span[-1]

    if suffix_token.i >= len(doc) - 1:
        # Defaults for end-of-sentence tokens.
        if suffix_token.lower_ in APOSTROPHE_S_VARIANTS:
            return 'is'
        if suffix_token.lower_ in APOSTROPHE_D_VARIANTS:
            return 'would'
        return None

    next_token = doc[suffix_token.i + 1]
    prev_token = doc[suffix_token.i - 1] if suffix_token.i > 0 else None

    if (prev_token and prev_token.lower_ == 'let' and
            suffix_token.lower_ in APOSTROPHE_S_VARIANTS):
        return 'us'

    # Disambiguate "'s": "is" vs. "has".
    if suffix_token.lower_ in APOSTROPHE_S_VARIANTS:
        # If followed by a participle (VBN, sometimes tagged as
        # VBD), 's is "has". Otherwise, 's is "is".
        if next_token and next_token.tag_ in PARTICIPLE_TAGS:
            return 'has'
        else:
            return 'is'

    # Disambiguate "'d": "would" vs. "had".
    elif suffix_token.lower_ in APOSTROPHE_D_VARIANTS:
        if next_token and next_token.lower_ == 'better':
            return 'had'
        elif next_token and next_token.tag_ in PARTICIPLE_TAGS:
            return 'had'
        else:
            return 'would'

    return None


def disambiguate_whatcha(span: Span) -> str | None:
    """
    Disambiguate the base verb for a matched "whatcha" contraction.

    This function assumes the ``Span`` has already been identified as a
    "whatcha" contraction.

    Args:
        span: The spaCy ``Span`` containing the "whatcha" contraction.

    Returns:
        str | None: The base verb for the "whatcha" contraction,
            otherwise ``None``.
    """
    doc = span.doc
    next_token = (doc[span.start + 1] if span.start + 1 < len(doc) else None)
    after_next_token = (
        doc[span.start + 2] if span.start + 2 < len(doc) else None
    )

    if next_token:
        next_text_lower = next_token.lower_
        tag = next_token.tag_

        # Check for the special case of "whatcha ain't".
        if after_next_token and (next_text_lower == 'ai' and
                after_next_token.lower_ in AIN_T_SUFFIX_VARIANTS):
            return ''

        # Disambiguate "are" vs. "has".
        if (
            WarpingPatterns.WHATCHA_ARE_WORDS.match(next_text_lower)
            or tag == 'VBG'
        ):
            return 'are'
        elif (
            WarpingPatterns.WHATCHA_HAVE_WORDS.match(next_text_lower)
            or tag in PARTICIPLE_TAGS
        ):
            return 'have'

        return 'do'

    return None
