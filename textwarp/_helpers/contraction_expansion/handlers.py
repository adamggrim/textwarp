from spacy.tokens import Span

from ..._constants import AIN_T_SUFFIX_VARIANTS
from ..._regexes import WarpingPatterns
from .disambiguation import (
    disambiguate_ain_t,
    disambiguate_whatcha,
    disambiguate_s_or_d
)
from .utils import (
    apply_expansion_casing,
    find_subject_token,
    negative_contraction_to_base_verb
)


def handle_negation(span: Span) -> tuple[str, int]:
    """
    Replace a matched negative contraction with its
    expanded version.

    This function handles "ain't", standard-order contractions and
    inversion contractions.

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        tuple[str, int]: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The index at the end of the expanded contraction.
    """
    # Verify a span exists.
    if not span:
        return span.text, span.end_char

    doc = span.doc
    suffix_token = span[-1]

    # Check the bounds.
    prev_token = (
        doc[suffix_token.i - 1] if suffix_token.i > 0 else None
    )

    if not prev_token:
        return span.text, span.end_char

    base_verb: str | None = None

    if WarpingPatterns.N_T_SUFFIX.match(suffix_token.text):

        # --- "AIN'T" ---
        if (prev_token and prev_token.lower_ == 'ai' and
                suffix_token.lower_ in AIN_T_SUFFIX_VARIANTS):
            base_verb = disambiguate_ain_t(span)

        # --- STANDARD NEGATION ---
        # (e.g., "couldn't", "wouldn't", "shouldn't")
        else:
            # The token before "n't" is the base verb.
            base_verb = negative_contraction_to_base_verb(span.text)

    # Handle a failed disambiguation.
    if base_verb is None:
        return span.text, span.end_char

    verb_token = prev_token
    subject_token = find_subject_token(verb_token)

    # --- INVERSION CHECK ---
    # Verb comes before the subject (e.g., "Don't I").
    if subject_token and subject_token.i > verb_token.i:
        subject_end_token = subject_token.right_edge
        subject_phrase_end_idx = (
            subject_end_token.idx + len(subject_end_token)
        )
        # Everything between the end of the contraction and the end of the
        # subject phrase.
        intermediate_text = doc.text[span.end_char : subject_phrase_end_idx]

        expanded_text: str = f'{base_verb}{intermediate_text} not'
        cased_text: str = apply_expansion_casing(span.text, expanded_text)

        return cased_text, subject_phrase_end_idx

    # --- STANDARD ORDER (NO INVERSION) ---
    # Verb comes after the subject (e.g., "I don't").
    else:
        expanded_text = f'{base_verb} not'
        cased_text = (
            apply_expansion_casing(span.text, expanded_text)
        )
        return cased_text, span.end_char


def handle_s_or_d(span: Span) -> tuple[str, int]:
    """
    Replace a matched "'s" or "'d" contraction with its expanded
    version.

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        tuple[str, int]: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The index at the end of the expanded contraction.
    """
    # Verify a span exists.
    if not span:
        return span.text, span.end_char

    doc = span.doc
    suffix_token = span[-1]

    # Check the bounds.
    if suffix_token.i == 0:
        return span.text, span.end_char

    base_verb: str | None = disambiguate_s_or_d(span)

    # Handle a failed disambiguation.
    if not base_verb:
        return span.text, span.end_char

    subject_token = doc[suffix_token.i - 1]

    expanded_text: str = f'{subject_token.text} {base_verb}'
    cased_text: str = apply_expansion_casing(span.text, expanded_text)

    return cased_text, span.end_char


def handle_whatcha(span: Span) -> tuple[str, int]:
    """
    Replace a matched "whatcha" contraction with its expanded version.

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        tuple[str, int]: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The index at the end of the expanded contraction.
    """
    # Verify a span exists.
    if not span:
        return span.text, span.end_char

    doc = span.doc
    suffix_token = span[-1]

    base_verb: str | None = disambiguate_whatcha(span)

    # Handle a failed disambiguation.
    if not base_verb:
        return span.text, span.end_char

    expanded_text: str = f'what {base_verb} you'
    cased_text: str = apply_expansion_casing(span.text, expanded_text)

    return cased_text, span.end_char
