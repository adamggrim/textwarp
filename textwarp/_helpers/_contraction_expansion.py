import regex as re
from spacy.tokens import (
    Doc,
    Span,
    Token
)

from .._config import UNAMBIGUOUS_CONTRACTIONS_MAP
from .._constants import (
    AIN_T_SUFFIX_VARIANTS,
    APOSTROPHE_D_VARIANTS,
    APOSTROPHE_S_VARIANTS,
    PAST_PARTICIPLE_TAGS
)
from .._nlp import nlp
from .._regexes import WarpingPatterns

from ._quote_conversion import curly_to_straight


def _apply_expansion_casing(original_word: str, expanded_word: str) -> str:
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


def _find_subject_token(verb_token: Token) -> Token | None:
    """
    Find the subject of a verb in a spaCy ``Doc``, handling both
    standard order (subject to the left: e.g., "I don't") and inverted
    order (subject to the right: e.g., "Don't I").

    This function attempts to use the dependency parser first. If the
    parser fails (common in questions or fragments), it falls back to
    positional heuristics.

    Args:
        verb_token: The token for the verb that predicates the subject.

    Returns:
        Token | None: The subject token, otherwise ``None``.
    """
    doc = verb_token.doc

    # Try to find the subject using the dependency parser.
    for child in verb_token.children:
        if child.dep_ in ('nsubj', 'nsubjpass'):
            return child

    # Fallback A: Look immediately before the verb (standard order).
    curr_index = verb_token.i - 1
    while curr_index >= 0:
        candidate = doc[curr_index]

        if candidate.pos_ in ('PRON', 'PROPN', 'NOUN'):
            return candidate
        # Stop if the loop hits a determiner, verb, or punctuation.
        if candidate.pos_ in ('DET', 'VERB', 'PUNCT'):
            break

        # Otherwise, move one step left to skip adverbs.
        curr_index -= 1

    # Fallback B: Look immediately after the suffix (inverted order).
    start_index = verb_token.i + 1
    if start_index < len(doc) and doc[start_index].lower_ == "n't":
        start_index += 1

    end_index = min(start_index + 6, len(doc))

    for j in range(start_index, end_index):
        candidate = doc[j]

        if candidate.pos_ in ('PRON', 'PROPN', 'NOUN'):
            return candidate
        # Stop if the loop hits a verb or punctuation.
        if candidate.pos_ in ('VERB', 'PUNCT'):
            break

    return None


def _expand_ambiguous_contraction(
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

    if not suffix_token or suffix_token.i == 0:
        return contraction

    previous_token: Token = doc[suffix_token.i - 1]
    next_token: Token | None = (
        doc[suffix_token.i + 1]
        if suffix_token.i < len(doc) - 1
        else None
    )

# --- HANDLE "AIN'T" ---
    if (previous_token.lower_ == 'ai' and
            suffix_token.lower_ in AIN_T_SUFFIX_VARIANTS):

        # Default fallback
        expansion_phrase = 'am not'

        verb_token = previous_token
        subject_token = _find_subject_token(verb_token)

        subject_text = subject_token.lower_ if subject_token else ''
        subject_tag = subject_token.tag_ if subject_token else ''

        # If "ain't" is followed by a participle (VBN) or past tense
        # (VBD), it functions as "have/has not". Otherwise, it functions
        # as "am/is/are not".
        is_perfect_tense = (next_token and next_token.tag_ in ('VBN', 'VBD'))

        if is_perfect_tense:
            # Disambiguate "has not" vs. "have not".
            if (subject_text in ('he', 'she', 'it') or
                subject_tag in ('NN', 'NNP')):
                expansion_phrase = 'has not'
            else:
                expansion_phrase = 'have not'
        else:
            # Disambiguate "am not" vs. "is not" vs. "are not".
            if subject_text == 'i':
                expansion_phrase = 'am not'
            elif (subject_text in ('he', 'she', 'it') or
                  subject_tag in ('NN', 'NNP')):
                expansion_phrase = 'is not'
            else:
                expansion_phrase = 'are not'

        return _apply_expansion_casing(contraction, expansion_phrase)

    # --- HANDLE 'S AND 'D ---
    else:
        expanded_suffix = ''

        # Disambiguate "is" vs. "has".
        if suffix_token.lower_ in APOSTROPHE_S_VARIANTS:
            # If followed by a participle (VBN, sometimes tagged as
            # VBD), 's is "has". Otherwise, 's is "is".
            if next_token and next_token.tag_ in ('VBN', 'VBD'):
                expanded_suffix = 'has'
            else:
                expanded_suffix = 'is'

        # Disambiguate "would" vs. "had".
        elif suffix_token.lower_ in APOSTROPHE_D_VARIANTS:
            if next_token and next_token.tag_ in ('VBN', 'VBD'):
                expanded_suffix = 'had'
            else:
                expanded_suffix = 'would'

        if expanded_suffix:
            # Keep the host word and append the suffix.
            host_token = doc[suffix_token.i - 1]
            full_expansion = f'{host_token.text} {expanded_suffix}'
            return _apply_expansion_casing(contraction, full_expansion)

    return contraction


def _expand_unambiguous_contraction(
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
    return _apply_expansion_casing(contraction, expanded_contraction)


def expand_contractions_from_doc(doc: Doc) -> str:
    """
    Expand all contractions in a given spaCy ``Doc``.

    Args:
        doc: A spaCy ``Doc``.

    Returns:
        str: The converted ``Doc`` text.
    """
    # If there are no ambiguous contractions, spaCy isn't needed.
    if not WarpingPatterns.AMBIGUOUS_CONTRACTION.search(doc.text):
        return WarpingPatterns.CONTRACTION.sub(
        # Replace each contraction using the unambiguous contractions
        # map.
        lambda match: _expand_unambiguous_contraction(
            match.group(0),
            UNAMBIGUOUS_CONTRACTIONS_MAP
        ), doc.text
    )

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

        # If the contraction always expands the same phrase, skip the
        # spaCy logic and go directly to the map.
        if not WarpingPatterns.AMBIGUOUS_CONTRACTION.match(contraction):
             return _expand_unambiguous_contraction(
                contraction,
                UNAMBIGUOUS_CONTRACTIONS_MAP
            )

        start_char: int = match.start()
        end_char: int = match.end()
        span: Span | None = doc.char_span(start_char, end_char)
        suffix_token: Token | None = span[-1] if span else None

        # Handle cases where the regular expression identifies a
        # contraction, but the tokenizer fails to split it.
        if not suffix_token:
            return _expand_unambiguous_contraction(
                contraction,
                UNAMBIGUOUS_CONTRACTIONS_MAP
            )

        return _expand_ambiguous_contraction(
            contraction,
            suffix_token,
            doc
        )

    return WarpingPatterns.CONTRACTION.sub(_repl, doc.text)
