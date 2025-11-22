import regex as re
from spacy.tokens import (
    Doc,
    Token
)

from .._constants import (
    AIN_T_SUFFIX_VARIANTS,
    APOSTROPHE_D_VARIANTS,
    APOSTROPHE_S_VARIANTS,
    PAST_PARTICIPLE_TAGS
)
from ._quote_conversion import curly_to_straight


def apply_expansion_casing(original_word: str, expanded_word: str) -> str:
    """
    Apply the casing of the original word to the expanded word.

    Args:
        original_word: The original word.
        expanded_word: The cased word.

    Returns:
        str: The expanded word in the original word's casing.
    """
    if original_word.isupper():
        return expanded_word.upper()
    elif original_word.istitle():
        return expanded_word.capitalize()
    return expanded_word


def expand_ambiguous_contraction(
    contraction: str,
    suffix_token: Token,
    doc: Doc,
) -> str:
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
        str: The expanded version of the matched contraction.
    """
    full_expansion: str = contraction

    if suffix_token and suffix_token.i > 0:
        previous_token: Token = doc[suffix_token.i - 1]
        next_token: Token | None = (
            doc[suffix_token.i + 1]
            if suffix_token.i < len(doc) - 1
            else None
        )
        # Disambiguate ain't: "am not," "is not," "are not," "has
        # not" or "have not"
        if (previous_token.lower_ == 'ai' and
                suffix_token.lower_ in AIN_T_SUFFIX_VARIANTS):
            if suffix_token.i >= 2:
                subject_token: Token = doc[suffix_token.i - 2]
                # Default expansion
                full_expansion = 'am not'
                # 1. Check for "has"/"have not".
                if next_token and next_token.tag_ in PAST_PARTICIPLE_TAGS:
                    if subject_token.lower_ in ('he', 'she', 'it'):
                        full_expansion = 'has not'
                    else:
                        # Covers "I", "you", "we" and "they".
                        full_expansion = 'have not'
                # 2. Check for "is"/"am"/"are not".
                else:
                    if subject_token.lower_ == 'i':
                        full_expansion = 'am not'
                    elif subject_token.lower_ in ('he', 'she', 'it'):
                        full_expansion = 'is not'
                    else:
                        # Covers "you", "we" and "they".
                        full_expansion = 'are not'
            else:
                full_expansion = 'am not'

            return apply_expansion_casing(contraction, full_expansion)

        else:
            expanded_suffix = ''
            # Disambiguate 's: "is" vs. "has"
            if suffix_token.lower_ in APOSTROPHE_S_VARIANTS:
                if next_token and next_token.tag_ in PAST_PARTICIPLE_TAGS:
                    expanded_suffix = 'has'
                else:
                    expanded_suffix = 'is'
            # Disambiguate 'd: "would" vs. "had"
            elif suffix_token.lower_ in APOSTROPHE_D_VARIANTS:
                if next_token and next_token.tag_ in PAST_PARTICIPLE_TAGS:
                    expanded_suffix = 'had'
                else:
                    expanded_suffix = 'would'

            if expanded_suffix:
                subject_token: Token = doc[suffix_token.i - 1]
                # Combine the subject with the expanded suffix.
                full_expansion: str = f'{subject_token.text} {expanded_suffix}'

        return apply_expansion_casing(contraction, full_expansion)


def expand_unambiguous_contraction(
    contraction: str,
    contractions_map: dict[str, str]
) -> str:
    """
    Replace an unambiguous contraction using the contractions map.

    Args:
        contraction: The contraction to expand.

    Returns:
        str: The expanded contraction.
        contractions_map: A dictionary pairing each contraction with its
            expanded version.
    """
    normalized_contraction: str = curly_to_straight(contraction).lower()
    expanded_contraction: str = contractions_map.get(
        normalized_contraction, contraction
    )
    return apply_expansion_casing(contraction, expanded_contraction)

def expand_contractions(text: str) -> str:
    """
    Expand all contractions in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    # If there are no ambiguous contractions, spaCy isn't needed.
    if not WarpingPatterns.AMBIGUOUS_CONTRACTION.search(text):
        return WarpingPatterns.CONTRACTION.sub(
        # Replace each contraction using the unambiguous contractions
        # map.
        lambda match: expand_unambiguous_contraction(
            match.group(0),
            UNAMBIGUOUS_CONTRACTIONS_MAP
        ), text
    )

    doc: Doc = nlp(text)

    def _repl(match: re.Match[str]) -> str:
        """
        Helper function to replace a matched contraction with its
        expanded version.

        Args:
            match: A match object representing a contraction.

        Returns:
            str: The expanded version of the matched contraction.
        """
        contraction: str = match.group(0)
        start_char: int = match.start()
        end_char: int = match.end()

        span: Span | None = doc.char_span(start_char, end_char)
        suffix_token: Token | None = span[-1] if span else None

        # Handle cases where the regular expression identifies a
        # contraction, but the tokenizer fails to split it.
        if not suffix_token:
            return expand_unambiguous_contraction(
                contraction,
                UNAMBIGUOUS_CONTRACTIONS_MAP
            )

        return expand_ambiguous_contraction(
            contraction,
            suffix_token,
            doc
        )

    return WarpingPatterns.CONTRACTION.sub(_repl, text)
