"""Functions for resolving ambiguous contractions based on context."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from spacy.tokens import Span

from textwarp._core.constants.nlp import (
    BASE_VERB_TAGS,
    NOUN_PHRASE_TAGS,
    NOUN_TAGS,
    PARTICIPLE_TAGS,
    THIRD_PERSON_SINGULAR_PRONOUNS,
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

# Strings for verbs that expand to "would".
_PREFERENCE_VERBS: Final[frozenset[str]] = frozenset({'care', 'mind', 'prefer'})


def _disambiguate_a_or_to(span: Span) -> str:
    """
    Shared logic for 'gotta' and 'wanna' to disambiguate 'a' or 'to'.
    """
    doc = span.doc
    next_token = doc[span.end] if span.end < len(doc) else None

    if (next_token and next_token.tag_ in NOUN_PHRASE_TAGS
        and next_token.tag_ != 'VB'):
        return 'a'

    return 'to'


def disambiguate_ain_t(span: Span) -> str:
    """
    Disambiguate the base verb for an "ain't" contraction.

    This function assumes the "n't" ``Span`` is already an identified
    "ain't" contraction (preceded by "ai").

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        str : The base verb for the contraction.
    """
    doc = span.doc
    verb_token = span[0]
    subject_token = find_subject_token(verb_token)
    next_token = doc[span.end] if span.end < len(doc) else None

    action_verb = next_token
    if next_token and subject_token and next_token.i == subject_token.i:
        action_verb = doc[span.end + 1] if span.end + 1 < len(doc) else None

    is_singular = True
    is_first_person_i = False

    if subject_token:
        subj_text = subject_token.lower_
        is_singular = (
            subj_text in THIRD_PERSON_SINGULAR_PRONOUNS or
            subject_token.tag_ in NOUN_TAGS
        )
        is_first_person_i = (subj_text == 'i')

    if action_verb:
        if action_verb.lower_ == 'got' or action_verb.tag_ in PARTICIPLE_TAGS:
            return 'has' if is_singular else 'have'

    if is_first_person_i:
        return 'am'

    return 'is' if is_singular else 'are'


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

    This function assumes the ``Span`` is already an identified "gotta"
    contraction.

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        str: The base verb for the contraction.
    """
    return _disambiguate_a_or_to(span)


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

    if suffix_token.i > 0 and doc[suffix_token.i - 1].lower_ == 'let':
        return 'us'

    for i in range(suffix_token.i + 1, min(suffix_token.i + 4, len(doc))):
        tag = doc[i].tag_
        if tag in BASE_VERB_TAGS:
            return 'does'
        if tag in PARTICIPLE_TAGS:
            return 'has'
        if tag == 'VBG':
            return 'is'

    return 'is'


def disambiguate_wanna(span: Span) -> str:
    """
    Disambiguate the suffix for a "wanna" contraction.

    This function assumes the ``Span`` is already an identified "wanna"
    contraction.

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        str: The base verb for the contraction.
    """
    return _disambiguate_a_or_to(span)


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

    if after_next_token and (next_text_lower == 'ai' and
            after_next_token.lower_ in AIN_T_SUFFIX_VARIANTS):
        return ''

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
