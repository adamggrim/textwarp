"""Functions for handling specific types of English contractions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textwarp._core.enums import POSTag
from textwarp._core.providers import en
from textwarp._core.utils import starts_uppercase
from textwarp._lib.contractions import apply_expansion_casing

if TYPE_CHECKING:
    from spacy.tokens import Span

__all__ = [
    'expand_d_contraction',
    'expand_gotta',
    'expand_negative_contraction',
    'expand_s_contraction',
    'expand_wanna',
    'expand_whatcha'
]


def expand_d_contraction(span: Span) -> tuple[str, int] | None:
    """
    Replace a matched "'d" contraction with its expanded version.

    Args:
        span: The spaCy `Span` containing the contraction.

    Returns:
        tuple[str, int] | None: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The end index of the expanded contraction; otherwise `None`.
    """
    if not span.text.lower().endswith(
        tuple(en.expansion.variants.APOSTROPHE_D_VARIANTS)
    ):
        return None

    doc = span.doc
    suffix_token = span[-1]

    if suffix_token.i == 0:
        return span.text, span.end_char

    base_verb: str = en.expansion.disambiguation.disambiguate_d(span)
    subject_token = doc[suffix_token.i - 1]
    expanded_text: str = f'{subject_token.text} {base_verb}'
    cased_text: str = apply_expansion_casing(span.text, expanded_text)

    return cased_text, span.end_char


def expand_gotta(span: Span) -> tuple[str, int] | None:
    """
    Replace a matched "gotta" contraction with its expanded version.

    Args:
        span: The spaCy `Span` containing the contraction.

    Returns:
        tuple[str, int] | None: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The end index of the expanded contraction; otherwise
                `None`.
    """
    if span.text.lower() != 'gotta':
        return None

    suffix = en.expansion.disambiguation.disambiguate_gotta_or_wanna(span)
    prefix = ''

    if suffix == 'to':
        doc = span.doc

        has_aux = False
        prev_token = en.utils.get_prev_lexical_token(
            doc,
            span.start - 1,
            skip_pos={POSTag.SPACE, POSTag.PUNCT, POSTag.ADV}
        )

        if prev_token:
            is_have_auxiliary = (
                prev_token.lower_ in en.constants.HAVE_AUXILIARIES
                or prev_token.lower_ == "'s"
            )

            if is_have_auxiliary:
                has_aux = True

        if not has_aux:
            subject = en.utils.find_subject_token(span[0])
            if subject and (
                subject.lower_ in en.constants.THIRD_PERSON_SINGULAR_PRONOUNS
                or subject.tag_ in en.constants.SINGULAR_NOUN_TAGS
            ):
                prefix = 'has '
            else:
                prefix = 'have '

    expanded_text: str = f'{prefix}got {suffix}'
    cased_text: str = apply_expansion_casing(span.text, expanded_text)

    return cased_text, span.end_char


def expand_negative_contraction(span: Span) -> tuple[str, int] | None:
    """
    Replace a matched negative contraction (including "ain't") with its
    expanded version.

    This function handles "ain't", standard-order contractions and
    inversion contractions.

    Args:
        span: The spaCy `Span` containing the contraction.

    Returns:
        tuple[str, int] | None: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The end index of the expanded contraction; otherwise
                `None`.
    """
    if not en.patterns.get_n_t_suffix().search(span.text.lower()):
        return None

    suffix_token = span[-1]

    if suffix_token.i == 0:
        return span.text, span.end_char

    doc = span.doc
    prev_token = doc[suffix_token.i - 1]

    base_verb: str | None = None

    is_aint_contraction = (
        prev_token.lower_ == 'ai'
        and suffix_token.lower_ in en.expansion.variants.N_T_SUFFIX_VARIANTS
    )

    if is_aint_contraction:
        base_verb = en.expansion.disambiguation.disambiguate_ain_t(span)
    else:
        base_verb = en.utils.get_negative_contraction_base_verb(span.text)

    if base_verb is None:
        return span.text, span.end_char

    verb_token = prev_token
    subject_token = en.utils.find_subject_token(verb_token)

    # Verb comes before the subject (e.g., "Don't I").
    if subject_token and subject_token.i > prev_token.i:
        subject_end_token = subject_token.right_edge

        # Prevent negative slicing.
        if subject_end_token.i < span.end:
            subject_end_token = subject_token

        return_idx = subject_end_token.idx + len(subject_end_token)

        # Every token between the end of the contraction and the end of
        # the subject phrase.
        intermediate_tokens = doc[span.end : subject_end_token.i + 1]
        intermediate_text = ''.join(
            t.text + t.whitespace_ for t in intermediate_tokens
        )

        # Ensure spacing before 'not' does not change.
        if not intermediate_text.endswith(' '):
            intermediate_text += ' '

        cased_base, _, cased_not = (
            apply_expansion_casing(
                span.text, f'{base_verb} not').partition(' ')
        )
        cased_not = cased_not or 'not'

        if cased_not == 'not':
            alpha_words = [
                w for w in doc.text.split() if any(c.isalpha() for c in w)
            ]
            is_globally_capitalized = len(alpha_words) > 1 and all(
                starts_uppercase(w) for w in alpha_words
            )
            if is_globally_capitalized:
                cased_not = 'Not'

        return f'{cased_base} {intermediate_text}{cased_not}', return_idx

    # Verb comes after the subject (e.g., "I don't").
    else:
        return_idx = span.end_char
        expanded_text = 'cannot' if base_verb == 'can' else f'{base_verb} not'

    original_replaced_text = doc.text[span.start_char : return_idx]
    cased_text = apply_expansion_casing(original_replaced_text, expanded_text)
    return cased_text, return_idx


def expand_s_contraction(span: Span) -> tuple[str, int] | None:
    """
    Replace a matched "'s" contraction with its expanded version.

    Args:
        span: The spaCy `Span` containing the contraction.

    Returns:
        tuple[str, int] | None: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The end index of the expanded contraction; otherwise
                `None`.
    """
    if not span.text.lower().endswith(
        tuple(en.expansion.variants.APOSTROPHE_S_VARIANTS)
    ):
        return None

    doc = span.doc
    suffix_token = span[-1]

    if suffix_token.i == 0:
        return span.text, span.end_char

    base_verb: str = en.expansion.disambiguation.disambiguate_s(span)

    subject_token = doc[suffix_token.i - 1]
    expanded_text: str = f'{subject_token.text} {base_verb}'
    cased_text: str = apply_expansion_casing(span.text, expanded_text)

    return cased_text, span.end_char


def expand_wanna(span: Span) -> tuple[str, int] | None:
    """
    Replace a matched "wanna" contraction with its expanded version.

    Args:
        span: The spaCy `Span` containing the contraction.

    Returns:
        tuple[str, int] | None: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The end index of the expanded contraction; otherwise
                `None`.
    """
    if span.text.lower() != 'wanna':
        return None

    base_verb = en.expansion.disambiguation.disambiguate_gotta_or_wanna(span)

    expanded_text: str = f'want {base_verb}'
    cased_text: str = apply_expansion_casing(span.text, expanded_text)
    return cased_text, span.end_char


def expand_whatcha(span: Span) -> tuple[str, int] | None:
    """
    Replace a matched "whatcha" contraction with its expanded version.

    Args:
        span: The spaCy `Span` containing the contraction.

    Returns:
        tuple[str, int] | None: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The end index of the expanded contraction; otherwise
                `None`.
    """
    if span.text.lower() != 'whatcha':
        return None

    base_verb: str = en.expansion.disambiguation.disambiguate_whatcha(span)
    expanded_text: str = f'what {base_verb} you'
    cased_text: str = apply_expansion_casing(span.text, expanded_text)

    return cased_text, span.end_char
