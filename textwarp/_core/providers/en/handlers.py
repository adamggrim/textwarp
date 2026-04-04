"""Functions for handling specific types of contractions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from textwarp._core.providers import en
from textwarp._lib.contractions import apply_expansion_casing

if TYPE_CHECKING:
    from spacy.tokens import Span

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
    if not span.text.lower().endswith(
        tuple(en.contractions.APOSTROPHE_D_VARIANTS)
    ):
        return None

    doc = span.doc
    suffix_token = span[-1]

    if suffix_token.i == 0:
        return span.text, span.end_char

    base_verb: str = en.disambiguation.disambiguate_d(span)
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

    suffix = en.disambiguation.disambiguate_gotta(span)
    prefix = ''

    if suffix == 'to':
        doc = span.doc

        has_aux = False
        curr_idx = span.start - 1
        while curr_idx >= 0:
            prev_token = doc[curr_idx]
            if (prev_token.lower_ in en.constants.HAVE_AUXILIARIES
                    or prev_token.lower_ == "'s"):
                has_aux = True
                break
            elif prev_token.pos_ == 'ADV':
                curr_idx -= 1
            else:
                break

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
    if not en.patterns.get_n_t_suffix().search(span.text.lower()):
        return None

    suffix_token = span[-1]

    if suffix_token.i == 0:
        return span.text, span.end_char

    doc = span.doc
    prev_token = doc[suffix_token.i - 1]

    base_verb: str | None = None

    if (prev_token.lower_ == 'ai'
            and suffix_token.lower_ in en.contractions.AIN_T_SUFFIX_VARIANTS):
        base_verb = en.disambiguation.disambiguate_ain_t(span)
    else:
        base_verb = en.utils.get_negative_contraction_base_verb(span.text)

    if base_verb is None:
        return span.text, span.end_char

    verb_token = prev_token
    subject_token = en.utils.find_subject_token(verb_token)

    # Verb comes before the subject (e.g., "Don't I").
    if subject_token and subject_token.i > prev_token.i:
        subject_end_token = subject_token.right_edge
        return_idx = subject_end_token.idx + len(subject_end_token)

        # Everything between the end of the contraction and the end
        # of the subject phrase.
        intermediate_text = doc.text[span.end_char : return_idx]
        expanded_text = f'{base_verb}{intermediate_text} not'

    # Verb comes after the subject (e.g., "I don't").
    else:
        return_idx = span.end_char
        expanded_text = 'cannot' if base_verb == 'can' else f'{base_verb} not'

    cased_text = apply_expansion_casing(span.text, expanded_text)
    return cased_text, return_idx


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
    if not span.text.lower().endswith(
        tuple(en.contractions.APOSTROPHE_S_VARIANTS)
    ):
        return None

    doc = span.doc
    suffix_token = span[-1]

    if suffix_token.i == 0:
        return span.text, span.end_char

    base_verb: str = en.disambiguation.disambiguate_s(span)

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

    base_verb = en.disambiguation.disambiguate_wanna(span)

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

    base_verb: str = en.disambiguation.disambiguate_whatcha(span)
    expanded_text: str = f'what {base_verb} you'
    cased_text: str = apply_expansion_casing(span.text, expanded_text)

    return cased_text, span.end_char
