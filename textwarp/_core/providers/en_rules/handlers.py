"""Functions for handling specific types of contractions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textwarp._core.constants.nlp import (
    HAVE_AUXILIARIES,
    SINGULAR_NOUN_TAGS,
    THIRD_PERSON_SINGULAR_PRONOUNS
)

if TYPE_CHECKING:
    from spacy.tokens import Span

from textwarp._core.constants.apostrophes import (
    AIN_T_SUFFIX_VARIANTS,
    APOSTROPHE_D_VARIANTS,
    APOSTROPHE_S_VARIANTS
)
from textwarp._core.constants.regexes import WarpingPatterns
from textwarp._core.providers.en_rules.disambiguation import (
    disambiguate_ain_t,
    disambiguate_d,
    disambiguate_gotta,
    disambiguate_s,
    disambiguate_wanna,
    disambiguate_whatcha
)
from textwarp._core.providers.en_rules.utils import (
    apply_expansion_casing,
    find_subject_token,
    get_negative_contraction_base_verb
)

__all__ = [
    'handle_d',
    'handle_gotta',
    'handle_negation',
    'handle_s',
    'handle_wanna',
    'handle_whatcha'
]


def handle_d(span: Span) -> tuple[str, int] | None:
    """
    Replace a matched "'d" contraction with its expanded version.

    Args:
        span: The spaCy `Span` containing the contraction.

    Returns:
        tuple[str, int] | None: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The end index of the expanded contraction; otherwise `None`.
    """
    if not any(
        span.text.lower().endswith(suffix) for suffix in APOSTROPHE_D_VARIANTS
    ):
        return None

    doc = span.doc
    suffix_token = span[-1]

    if suffix_token.i == 0:
        return span.text, span.end_char

    base_verb: str = disambiguate_d(span)
    subject_token = doc[suffix_token.i - 1]
    expanded_text: str = f'{subject_token.text} {base_verb}'
    cased_text: str = apply_expansion_casing(span.text, expanded_text)

    return cased_text, span.end_char


def handle_gotta(span: Span) -> tuple[str, int] | None:
    """
    Replace a matched "gotta" contraction with its expanded version.

    Args:
        span: The spaCy `Span` containing the contraction.

    Returns:
        tuple[str, int] | None: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The end index of the expanded contraction; otherwise `None`.
    """
    if span.text.lower() != 'gotta':
        return None

    suffix = disambiguate_gotta(span)
    prefix = ''

    if suffix == 'to':
        doc = span.doc

        has_aux = False
        curr_idx = span.start - 1
        while curr_idx >= 0:
            prev_token = doc[curr_idx]
            if (prev_token.lower_ in HAVE_AUXILIARIES
                or prev_token.lower_ == "'s"):
                has_aux = True
                break
            elif prev_token.pos_ == 'ADV':
                curr_idx -= 1
            else:
                break

        if not has_aux:
            subject = find_subject_token(span[0])
            if subject and (
                subject.text.lower() in THIRD_PERSON_SINGULAR_PRONOUNS
                or subject.tag_ in SINGULAR_NOUN_TAGS
            ):
                prefix = 'has '
            else:
                prefix = 'have '

    expanded_text: str = f'{prefix}got {suffix}'
    cased_text: str = apply_expansion_casing(span.text, expanded_text)

    return cased_text, span.end_char


def handle_negation(span: Span) -> tuple[str, int] | None:
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
    if not WarpingPatterns.get_n_t_suffix().search(span.text.lower()):
        return None

    doc = span.doc
    suffix_token = span[-1]

    prev_token = (
        doc[suffix_token.i - 1] if suffix_token.i > 0 else None
    )

    if not prev_token:
        return span.text, span.end_char

    base_verb: str | None = None

    if (prev_token and prev_token.lower_ == 'ai'
            and suffix_token.lower_ in AIN_T_SUFFIX_VARIANTS):
        base_verb = disambiguate_ain_t(span)
    else:
        base_verb = get_negative_contraction_base_verb(span.text)

    if base_verb is None:
        return span.text, span.end_char

    verb_token = prev_token
    subject_token = find_subject_token(verb_token)

    # Verb comes before the subject (e.g., "Don't I").
    if subject_token and subject_token.i > verb_token.i:
        subject_end_token = subject_token.right_edge
        subject_phrase_end_idx = (
            subject_end_token.idx + len(subject_end_token)
        )
        # Everything between the end of the contraction and the end
        # of the subject phrase.
        intermediate_text = doc.text[
            span.end_char : subject_phrase_end_idx
        ]

        expanded_text: str = f'{base_verb}{intermediate_text} not'
        cased_text: str = apply_expansion_casing(span.text, expanded_text)

        return cased_text, subject_phrase_end_idx

    # Verb comes after the subject (e.g., "I don't").
    else:
        if base_verb == 'can':
            expanded_text = 'cannot'
        else:
            expanded_text = f'{base_verb} not'
        cased_text = (
            apply_expansion_casing(span.text, expanded_text)
        )
        return cased_text, span.end_char


def handle_s(span: Span) -> tuple[str, int] | None:
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
    if not any(
        span.text.lower().endswith(suffix) for suffix in APOSTROPHE_S_VARIANTS
    ):
        return None

    doc = span.doc
    suffix_token = span[-1]

    if suffix_token.i == 0:
        return span.text, span.end_char

    base_verb: str = disambiguate_s(span)

    subject_token = doc[suffix_token.i - 1]
    expanded_text: str = f'{subject_token.text} {base_verb}'
    cased_text: str = apply_expansion_casing(span.text, expanded_text)

    return cased_text, span.end_char


def handle_wanna(span: Span) -> tuple[str, int] | None:
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

    base_verb = disambiguate_wanna(span)

    expanded_text: str = f'want {base_verb}'
    cased_text: str = apply_expansion_casing(span.text, expanded_text)
    return cased_text, span.end_char


def handle_whatcha(span: Span) -> tuple[str, int] | None:
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

    base_verb: str = disambiguate_whatcha(span)
    expanded_text: str = f'what {base_verb} you'
    cased_text: str = apply_expansion_casing(span.text, expanded_text)

    return cased_text, span.end_char
