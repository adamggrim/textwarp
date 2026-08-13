"""
Functions for resolving ambiguous English contractions based on context.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Span, Token

from textwarp._core.constants import NOUN_TAGS
from textwarp._core.enums import POSTag
from textwarp._core.providers import en
from textwarp._core.providers.en.constants import (
    PARTICIPLE_SUFFIXES,
    QUOTATION_MARKS
)

__all__ = [
    'disambiguate_ain_t',
    'disambiguate_d',
    'disambiguate_gotta_or_wanna',
    'disambiguate_s',
    'disambiguate_whatcha'
]


def _is_present_participle(token: Token) -> bool:
    """
    Check if a token is a present participle (VBG), accounting for
    words that end in "in'".
    """
    if token.tag_ == 'VBG':
        return True

    text_lower = token.lower_

    if en.patterns.get_common_stateless_participles().match(text_lower):
        return True

    if text_lower.endswith(PARTICIPLE_SUFFIXES):
        return True

    if text_lower.endswith('in'):
        doc = token.doc
        next_token = en.utils.get_next_lexical_token(
            doc, token.i + 1, skip_pos={POSTag.SPACE}
        )
        is_followed_by_quote = (
            next_token and next_token.text in QUOTATION_MARKS
        )

        if is_followed_by_quote:
            return True

    return False


def _disambiguate_a_or_to(span: Span) -> str:
    """
    Shared logic for "gotta" and "wanna" disambiguation between "a"
    and "to".
    """
    doc = span.doc
    next_token = en.utils.get_next_lexical_token(doc, span.end)

    is_valid_noun_phrase = (
        next_token
        and next_token.tag_ in en.constants.NOUN_PHRASE_TAGS
        and next_token.tag_ != 'VB'
    )

    if is_valid_noun_phrase:
        is_infinitive_exception = (
            next_token.lower_
            in en.data.contraction_expansion.get_infinitive_exceptions()
        )

        if is_infinitive_exception:
            return 'to'

        return 'a'

    return 'to'


def disambiguate_ain_t(span: Span) -> str:
    """
    Disambiguate the base verb for an "ain't" contraction.

    This function assumes the "n't" `Span` is already an identified
    "ain't" contraction (preceded by "ai").
    """
    doc = span.doc
    verb_token = span[0]
    subject_token = en.utils.find_subject_token(verb_token)
    next_token = en.utils.get_next_lexical_token(
        doc, span.end, skip_pos={POSTag.SPACE, POSTag.PUNCT, POSTag.ADV}
    )

    action_verb = next_token
    if next_token and subject_token and next_token.i == subject_token.i:
        action_verb = en.utils.get_next_lexical_token(
            doc,
            next_token.i + 1,
            skip_pos={POSTag.SPACE, POSTag.PUNCT, POSTag.ADV}
        )

    is_singular = True
    is_first_person_i = False

    if subject_token:
        subj_text = subject_token.lower_
        is_singular = (
            subj_text in en.constants.THIRD_PERSON_SINGULAR_PRONOUNS
            or subject_token.tag_ in NOUN_TAGS
        )
        is_first_person_i = (subj_text == 'i')

    if action_verb:
        is_got_or_participle = (
            action_verb.lower_ == 'got'
            or action_verb.tag_ in en.constants.PARTICIPLE_TAGS
        )

        if is_got_or_participle:
            return 'has' if is_singular else 'have'

    if is_first_person_i:
        return 'am'

    return 'is' if is_singular else 'are'


def disambiguate_d(span: Span) -> str:
    """
    Disambiguate the base verb for an "'d" contraction.

    This function assumes the `Span` is already a "'d" contraction.
    """
    doc = span.doc
    suffix_token = span[-1]

    if suffix_token.i >= len(doc) - 1:
        return 'would'

    starts_with_wh_word = (
        span[0].lower_ in en.constants.WH_WORDS
        or (
            span.start > 0
            and doc[span.start - 1].lower_ in en.constants.WH_WORDS
        )
    )

    curr_idx = suffix_token.i + 1
    while curr_idx < len(doc):
        token = en.utils.get_next_lexical_token(
            doc,
            curr_idx,
            skip_pos={POSTag.SPACE, POSTag.PUNCT}
        )
        if not token:
            break

        is_better_or_participle = (
            token.lower_ == 'better'
            or token.tag_ in en.constants.PARTICIPLE_TAGS
        )

        if is_better_or_participle:
            return 'had'

        if token.tag_ in en.constants.BASE_VERB_TAGS:
            if token.lemma_ in en.constants.PREFERENCE_VERBS:
                return 'would'
            return 'did' if starts_with_wh_word else 'would'

        if token.pos_ in {
            POSTag.PRON, POSTag.NOUN, POSTag.PROPN, POSTag.DET, POSTag.ADV
        }:
            curr_idx = token.i + 1
            continue

        break

    return 'would'


def disambiguate_gotta_or_wanna(span: Span) -> str:
    """
    Disambiguate the suffix for a "gotta" or "wanna" contraction.

    This function assumes the `Span` is already an identified "gotta" or
    "wanna" contraction.
    """
    return _disambiguate_a_or_to(span)


def disambiguate_s(span: Span) -> str:
    """
    Disambiguate the base verb for an "'s" contraction.

    This function assumes the `Span` is already an "'s" contraction.
    """
    doc = span.doc
    suffix_token = span[-1]

    prev_token = en.utils.get_prev_lexical_token(doc, suffix_token.i)
    if prev_token and prev_token.lower_ == 'let':
        return 'us'

    curr_idx = suffix_token.i + 1
    while curr_idx < len(doc):
        token = en.utils.get_next_lexical_token(
            doc,
            curr_idx,
            skip_pos={POSTag.SPACE, POSTag.PUNCT}
        )
        if not token:
            break

        tag = token.tag_

        if token.lower_ == 'gotta':
            return 'has'
        if token.pos_ == POSTag.DET:
            return 'is'
        if tag in en.constants.BASE_VERB_TAGS:
            return 'does'
        if tag in en.constants.PARTICIPLE_TAGS:
            return 'has'
        if _is_present_participle(token):
            return 'is'

        if token.pos_ in {
            POSTag.PRON, POSTag.NOUN, POSTag.PROPN, POSTag.DET, POSTag.ADV
        }:
            curr_idx = token.i + 1
            continue

        break

    return 'is'


def disambiguate_whatcha(span: Span) -> str:
    """
    Disambiguate the base verb for a "whatcha" contraction.

    This function assumes the `Span` has already been identified as a
    "whatcha" contraction.
    """
    doc = span.doc

    next_token = en.utils.get_next_lexical_token(
        doc, span.end, skip_pos={POSTag.SPACE, POSTag.PUNCT, POSTag.ADV}
    )
    after_next_token = (
        en.utils.get_next_lexical_token(
            doc,
            next_token.i + 1,
            skip_pos={POSTag.SPACE, POSTag.PUNCT, POSTag.ADV}
        )
        if next_token else None
    )

    if not next_token:
        return 'are'

    next_text_lower = next_token.lower_
    tag = next_token.tag_

    suffix_variants = en.expansion.variants.N_T_SUFFIX_VARIANTS
    if (
        after_next_token
        and next_text_lower == 'ai'
        and after_next_token.lower_ in suffix_variants
    ):
        return ''

    if (
        en.patterns.get_whatcha_are_words().match(next_text_lower)
        or _is_present_participle(next_token)
    ):
        return 'are'
    elif (
        en.patterns.get_whatcha_have_words().match(next_text_lower)
        or tag in en.constants.PARTICIPLE_TAGS
    ):
        return 'have'

    return 'do'
