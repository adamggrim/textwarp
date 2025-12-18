from spacy.tokens import Span

from ..._constants import (
    AIN_T_SUFFIX_VARIANTS,
    APOSTROPHE_D_VARIANTS,
    APOSTROPHE_S_VARIANTS
)
from .utils import find_subject_token


def disambiguate_ain_t(span: Span) -> str | None:
    """
    Disambiguate the base verb for a matched "ain't" contraction.

    This function assumes the "n't" span has already been identified as
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
        next_token and next_token.tag_ in ('VBN', 'VBD')
    )

    if not subject_token:
        return None

    if is_perfect_tense:
        # Disambiguate "has not" vs. "have not".
        if (subject_text in ('he', 'she', 'it') or
            subject_tag in ('NN', 'NNP')):
            return 'has'
        else:
            return 'have'
    else:
        # Disambiguate "am not" vs. "is not" vs. "are not".
        if subject_text == 'i':
            return 'am'
        elif (subject_text in ('he', 'she', 'it') or
            subject_tag in ('NN', 'NNP')):
            return 'is'
        else:
            # e.g., "You ain't", "We ain't", "They ain't".
            return 'are'


def disambiguate_s_or_d(span: Span) -> str | None:
    """
    Disambiguate the base verb for a matched "'s" or "'d" contraction.

    This function assumes the span has already been identified as an
    "'s" or "'d" contraction.

    Args:
        span: The spaCy ``Span`` containing the contraction.

    Returns:
        str | None: The expanded version of the matched contraction, otherwise
            ``None``.
    """
    doc = span.doc

    suffix_token = span[-1]

    next_token = (
        doc[suffix_token.i + 1]
        if suffix_token.i < len(doc) - 1
        else None
    )

    prev_token = doc[suffix_token.i - 1] if suffix_token.i > 0 else None
    if (prev_token and prev_token.lower_ == "let" and
            suffix_token.lower_ in APOSTROPHE_S_VARIANTS):
        return 'us'

    # Disambiguate "'s": "is" vs. "has".
    if suffix_token.lower_ in APOSTROPHE_S_VARIANTS:
        # If followed by a participle (VBN, sometimes tagged as
        # VBD), 's is "has". Otherwise, 's is "is".
        if next_token and next_token.tag_ in ('VBN', 'VBD'):
            return 'has'
        else:
            return 'is'

    # Disambiguate "'d": "would" vs. "had".
    elif suffix_token.lower_ in APOSTROPHE_D_VARIANTS:
        if next_token and next_token.lower_ == 'better':
            return 'had'
        elif next_token and next_token.tag_ in ('VBN', 'VBD'):
            return 'had'
        else:
            return 'would'

    return None


def disambiguate_whatcha(span: Span) -> str | None:
    """
    Disambiguate the base verb for a matched "whatcha" contraction.

    This function assumes the span has already been identified as a
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
        if (next_text_lower in ('gonna', 'tryna', 'goin', "goin'")
                or tag == 'VBG'):
            return 'are'
        elif next_text_lower == 'gotta' or tag in ('VBN', 'VBD'):
            return 'have'

        return 'do'

    return None
