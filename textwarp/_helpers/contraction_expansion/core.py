from spacy.tokens import (
    Doc,
    Span
)

from ..._regexes import WarpingPatterns

from ..._config import UNAMBIGUOUS_CONTRACTIONS_MAP
from ..._constants import (
    APOSTROPHE_D_VARIANTS,
    APOSTROPHE_S_VARIANTS
)
from ..quote_conversion import curly_to_straight
from .handlers import (
    handle_negation,
    handle_s_or_d,
    handle_whatcha,
)
from .utils import apply_expansion_casing


def _expand_ambiguous_contraction(
    contraction: str,
    span: Span
) -> tuple[str, int]:
    """
    Helper function to replace a matched ambiguous contraction with its
    expanded version.

    This function uses spaCy to disambiguate contractions based on
    context.

    Args:
        contraction: The contraction to expand.
        suffix_token: The token containing the contraction suffix
            (e.g., "'s", "n't").
        doc: The spaCy ``Doc`` containing the contraction.

    Returns:
        tuple[str, int]: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The index where the next search should begin.
    """
    original_end_char_index = span.end_char

    # --- HANDLE "WHATCHA" ---
    if "whatcha" in contraction.lower():
        return handle_whatcha(span)

    suffix_token = span[-1] if span else None
    if not suffix_token:
        return contraction, original_end_char_index

    # --- HANDLE NEGATION ---
    if WarpingPatterns.N_T_SUFFIX.match(suffix_token.text):
        return handle_negation(span)

    # --- HANDLE "'S" OR "'D" ---
    if (suffix_token.lower_ in APOSTROPHE_S_VARIANTS or
            suffix_token.lower_ in APOSTROPHE_D_VARIANTS):
        return handle_s_or_d(span)

    return contraction, original_end_char_index


def _expand_unambiguous_contraction(
    contraction: str,
    contractions_map: dict[str, str]
) -> str:
    """
    Replace an unambiguous contraction with its expanded version using
    the contractions map.

    Args:
        contraction: The contraction to expand.

    Returns:
        str: The expanded contraction.
    """
    straight_contraction: str = curly_to_straight(contraction).lower()
    expanded_contraction: str = contractions_map.get(
        straight_contraction, contraction
    )
    return apply_expansion_casing(contraction, expanded_contraction)


def expand_contractions_from_doc(doc: Doc) -> str:
    """
    Expand all contractions in a given spaCy ``Doc``.

    Args:
        doc: A spaCy ``Doc``.

    Returns:
        str: The converted ``Doc`` text.
    """
    matches = list(WarpingPatterns.CONTRACTION.finditer(doc.text))
    if not matches:
        return doc.text

    expanded_parts: list[str] = []
    last_idx = 0
    skip_until_idx = -1

    for match in matches:
        start_idx, end_idx = match.span()

        # If a previous inverted expansion already consumed this token,
        # skip it.
        if start_idx < skip_until_idx:
            continue

        # Append all text from the previous contraction (or beginning)
        # to the current contraction.
        expanded_parts.append(doc.text[last_idx:start_idx])
        contraction: str = match.group(0)

        # Check if complex negation/ambiguity logic is needed.
        is_negation: bool = bool(WarpingPatterns.N_T_SUFFIX.search(contraction))
        is_ambiguous: bool = bool(
            WarpingPatterns.AMBIGUOUS_CONTRACTION.match(contraction)
        )

        if is_negation or is_ambiguous:
            span: Span | None = doc.char_span(start_idx, end_idx)
            if span:
                expanded_text: str
                new_end_idx: int

                expanded_text, new_end_idx = _expand_ambiguous_contraction(
                    contraction, span
                )
                expanded_parts.append(expanded_text)
                last_idx = new_end_idx
                skip_until_idx = new_end_idx
                continue

        # For unambiguous contractions, use the unambiguous contractions
        # map.
        cased_expansion: str = _expand_unambiguous_contraction(
            contraction,
            UNAMBIGUOUS_CONTRACTIONS_MAP
        )

        expanded_parts.append(cased_expansion)
        last_idx = end_idx

    expanded_parts.append(doc.text[last_idx:])
    return ''.join(expanded_parts)
