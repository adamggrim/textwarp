"""Functions for resolving ambiguous contractions based on context."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Span, Token

from textwarp._core.constants.nlp import (
    ACTION_POS_TAGS,
    NOUN_PHRASE_TAGS,
    NOUN_TAGS,
    PARTICIPLE_TAGS,
    PREFERENCE_VERBS,
    THIRD_PERSON_SINGULAR_PRONOUNS,
    SUBJECT_POS_TAGS,
    WH_WORDS
)
from textwarp._core.constants.apostrophes import AIN_T_SUFFIX_VARIANTS
from textwarp._core.constants.regexes import WarpingPatterns
from textwarp._lib.contractions.utils import find_subject_token

__all__ = [
    'disambiguate_ain_t',
    'disambiguate_d',
    'disambiguate_gotta',
    'disambiguate_s',
    'disambiguate_wanna',
    'disambiguate_whatcha'
]


def _get_wh_verb_token(span: Span) -> Token | None:
    """
    Identify the main verb in a "wh-" question.

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        Token | None: The token of the main verb, or ``None`` if there
            is no verb or the context is not a "wh-" question.
    """
    doc = span.doc
    suffix_token = span[-1]
    prev_token = doc[suffix_token.i - 1] if suffix_token.i > 0 else None

    if not prev_token or prev_token.lower_ not in WH_WORDS:
        return None
    if suffix_token.i + 1 >= len(doc):
        return None

    next_token = doc[suffix_token.i + 1]
    target_token = next_token

    # Skip the subject if necessary.
    if next_token.pos_ in SUBJECT_POS_TAGS:
        if suffix_token.i + 2 < len(doc):
            target_token = doc[suffix_token.i + 2]

    return target_token


def disambiguate_ain_t(span: Span) -> str:
    """
    Disambiguate the base verb for an "ain't" contraction.

    This function assumes the "n't" ``Span`` has already been identified as
    an "ain't" contraction (preceded by "ai").

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        str : The base verb for the contraction.
    """
    doc = span.doc
    suffix_token = span[-1]

    # If "ain't" is followed by a participle (VBN) or past tense
    # (VBD), it functions as "have/has not". Otherwise, it functions
    # as "am/is/are not".
    next_token = (
        doc[suffix_token.i + 1]
        if suffix_token.i < len(doc) - 1
        else None
    )
    is_perfect_tense: bool = (
        next_token and next_token.tag_ in PARTICIPLE_TAGS
    )

    verb_token = doc[suffix_token.i - 1] if suffix_token.i > 0 else None
    subject_token = find_subject_token(verb_token)

    if subject_token:
        subject_text: str = subject_token.lower_ if subject_token else ''
        subject_tag: str = subject_token.tag_ if subject_token else ''

        if is_perfect_tense:
            # Disambiguate "has not" vs. "have not".
            if (subject_text in THIRD_PERSON_SINGULAR_PRONOUNS or
                subject_tag in NOUN_TAGS):
                return 'has'
            else:
                return 'have'
        else:
            # Disambiguate "am not" vs. "is not" vs. "are not".
            if subject_text == 'i':
                return 'am'
            elif (subject_text in THIRD_PERSON_SINGULAR_PRONOUNS or
                subject_tag in NOUN_TAGS):
                return 'is'
            else:
                # e.g., "You ain't", "We ain't", "They ain't".
                return 'are'

    return 'have' if is_perfect_tense else 'is'


def disambiguate_d(span: Span) -> str:
    """
    Disambiguate the base verb for an "'d" contraction.

    This function assumes the ``Span`` is already a "'d" contraction.

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        str: The base verb for the contraction.
    """
    doc = span.doc
    suffix_token = span[-1]

    # Check for end-of-sentence token.
    if suffix_token.i >= len(doc) - 1:
        return 'would'

    wh_verb_token = _get_wh_verb_token(span)

    if not wh_verb_token:
        # Check for "d better" -> "had better".
        next_token = doc[suffix_token.i + 1]
        if next_token.lower_ == 'better' or next_token.tag_ in PARTICIPLE_TAGS:
            return 'had'
        return 'would'

    if wh_verb_token.tag_ in PARTICIPLE_TAGS:
        return 'had'
    if (wh_verb_token.tag_ == 'VB' and
        wh_verb_token.lemma_ in PREFERENCE_VERBS):
            return 'would'

    return 'did'


def disambiguate_gotta(span: Span) -> str:
    """
    Disambiguate the suffix for a "gotta" contraction.

    This function assumes the ``Span`` has already been identified as a
    "gotta" contraction.

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        str: The base verb for the contraction.
    """
    doc = span.doc
    next_token = (doc[span.end] if span.end + 1 < len(doc) else None)

    if next_token:
        if next_token.pos_ in ACTION_POS_TAGS or next_token.tag_ == 'VB':
            return 'to'
        if next_token.tag_ in NOUN_PHRASE_TAGS:
            return 'a'

    return 'to'


def disambiguate_s(span: Span) -> str:
    """
    Disambiguate the base verb for an "'s" contraction.

    This function assumes the ``Span`` is already an "'s" contraction.

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        str: The base verb for the contraction.
    """
    doc = span.doc
    suffix_token = span[-1]

    # Check for end-of-sentence tokens.
    if suffix_token.i >= len(doc) - 1:
        return 'is'

    prev_token = doc[suffix_token.i - 1] if suffix_token.i > 0 else None
    next_token = doc[suffix_token.i + 1]
    wh_verb_token = _get_wh_verb_token(span)

    # Disambiguate "'s" ("does", "has", "is", "us").
    # "Let's" -> "us"
    if prev_token and prev_token.lower_ == 'let':
        return 'us'

    # "Wh" context ("does", "has")
    if wh_verb_token:
        # "What's she want?" (VB) -> "does"
        if wh_verb_token.tag_ == 'VB':
            return 'does'
        # "What's she done?" (VBN) -> "has"
        if wh_verb_token.tag_ in PARTICIPLE_TAGS:
            return 'has'

    # Standard context ("has", "is")
    if next_token.tag_ in PARTICIPLE_TAGS:
        return 'has'

    return 'is'


def disambiguate_wanna(span: Span) -> str:
    """
    Disambiguate the suffix for a "wanna" contraction.

    This function assumes the ``Span`` has already been identified as a
    "wanna" contraction.

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        str: The base verb for the contraction.
    """
    doc = span.doc
    next_token = (doc[span.end] if span.end + 1 < len(doc) else None)

    if next_token:
        if next_token.pos_ in ACTION_POS_TAGS or next_token.tag_ == 'VB':
            return 'to'
        if next_token.tag_ in NOUN_PHRASE_TAGS:
            return 'a'

    return 'to'


def disambiguate_whatcha(span: Span) -> str:
    """
    Disambiguate the base verb for a "whatcha" contraction.

    This function assumes the ``Span`` has already been identified as a
    "whatcha" contraction.

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        str: The base verb for the contraction.
    """
    doc = span.doc
    next_token = doc[span.end] if span.end < len(doc) else None
    after_next_token = (
        doc[span.end + 1] if span.end + 1 < len(doc) else None
    )

    if not next_token:
        return 'are'

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
