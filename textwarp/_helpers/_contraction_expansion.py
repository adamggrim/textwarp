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
    APOSTROPHE_S_VARIANTS
)
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
    doc: Doc = verb_token.doc

    # Try to find the subject using the dependency parser.
    for child in verb_token.children:
        if child.dep_ in ('nsubj', 'nsubjpass'):
            return child

    # Fallback A: Look immediately before the verb (standard order).
    curr_idx: int = verb_token.i - 1
    while curr_idx >= 0:
        candidate: Token = doc[curr_idx]

        if candidate.pos_ in ('PRON', 'PROPN', 'NOUN'):
            return candidate
        # Stop if the loop hits a determiner, verb, or punctuation.
        if candidate.pos_ in ('DET', 'VERB', 'PUNCT'):
            break

        # Otherwise, move one step left to skip adverbs.
        curr_idx -= 1

    # Fallback B: Look immediately after the suffix (inverted order).
    start_idx: int = verb_token.i + 1
    if start_idx < len(doc) and doc[start_idx].lower_ == "n't":
        start_idx += 1

    end_idx: int = min(start_idx + 6, len(doc))

    for j in range(start_idx, end_idx):
        candidate: Token = doc[j]

        if candidate.pos_ in ('PRON', 'PROPN', 'NOUN'):
            return candidate
        # Stop if the loop hits a verb or punctuation.
        if candidate.pos_ in ('VERB', 'PUNCT'):
            break

    return None


def _expand_ambiguous_contraction(
    contraction: str,
    span: Span,
    doc: Doc,
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
            2. The index (character offset) where the next search should
            begin.
    """
    original_end_char: int = span.end_char
    suffix_token: Token | None = span[-1] if span else None

    if not suffix_token or suffix_token.i == 0:
        return contraction, original_end_char

    previous_token: Token = doc[suffix_token.i - 1]

    # --- HANDLE "N'T" CONTRACTIONS ---
    if WarpingPatterns.N_T_SUFFIX.match(suffix_token.text):
        base_verb: str = ''

        # --- HANDLE "AIN'T" ---
        if (previous_token.lower_ == 'ai' and
                suffix_token.lower_ in AIN_T_SUFFIX_VARIANTS):

            verb_token: Token = previous_token
            subject_token: Token | None = _find_subject_token(verb_token)

            subject_text: str = subject_token.lower_ if subject_token else ''
            subject_tag: str = subject_token.tag_ if subject_token else ''

            next_token: Token | None = (
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

            if is_perfect_tense:
                # Disambiguate "has not" vs. "have not".
                if (subject_text in ('he', 'she', 'it') or
                    subject_tag in ('NN', 'NNP')):
                    base_verb = 'has'
                else:
                    base_verb = 'have'
            else:
                # Disambiguate "am not" vs. "is not" vs. "are not".
                if subject_text == 'i':
                    base_verb = 'am'
                elif (subject_text in ('he', 'she', 'it') or
                    subject_tag in ('NN', 'NNP')):
                    base_verb = 'is'
                else:
                    base_verb = 'are'

        # --- HANDLE STANDARD NEGATION ---
        # (e.g., "couldn't", "wouldn't", "shouldn't")
        else:
            # The token before "n't" is the base verb.
            verb_token = previous_token
            subject_token = _find_subject_token(verb_token)
            base_verb = _negative_contraction_to_base_verb(contraction)

        # --- INVERSION CHECK ---
        # Verb comes before subject (e.g., "Don't I").
        if subject_token and subject_token.i > verb_token.i:
            cased_base: str = _apply_expansion_casing(
                verb_token.text, base_verb
            )
            subject_text: str = subject_token.text
            expanded_text: str = f'{cased_base} {subject_text} not'

            # New end index to skip over the subject in the main loop.
            new_end_idx: int = subject_token.idx + len(subject_token)

            return expanded_text, new_end_idx

        # --- NO INVERSION ---
        # Verb comes after subject (e.g., "I do not").
        else:
            expanded_text = f'{base_verb} not'
            cased_text: str = (
                _apply_expansion_casing(
                    verb_token.text, expanded_text
                ), original_end_char
            )
            return cased_text, original_end_char

    # --- HANDLE "'S" AND "'D" ---
    next_token: Token | None = (
        doc[suffix_token.i + 1]
        if suffix_token.i < len(doc) - 1
        else None
    )
    expanded_suffix: str = ''

    # Disambiguate "'s": "is" vs. "has".
    if suffix_token.lower_ in APOSTROPHE_S_VARIANTS:
        # If followed by a participle (VBN, sometimes tagged as
        # VBD), 's is "has". Otherwise, 's is "is".
        if next_token and next_token.tag_ in ('VBN', 'VBD'):
            expanded_suffix = 'has'
        else:
            expanded_suffix = 'is'

    # Disambiguate "'d": "would" vs. "had".
    elif suffix_token.lower_ in APOSTROPHE_D_VARIANTS:
        if next_token and next_token.tag_ in ('VBN', 'VBD'):
            expanded_suffix = 'had'
        else:
            expanded_suffix = 'would'

    if expanded_suffix:
        # Keep the base word and append the suffix.
        base_token: Token = doc[suffix_token.i - 1]
        full_expansion: str = f'{base_token.text} {expanded_suffix}'
        cased_expansion: str = _apply_expansion_casing(
            contraction, full_expansion
        )
        return cased_expansion, original_end_char

    return contraction, original_end_char


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
    """
    straight_contraction: str = curly_to_straight(contraction).lower()
    expanded_contraction: str = contractions_map.get(
        straight_contraction, contraction
    )
    return _apply_expansion_casing(contraction, expanded_contraction)


def _negative_contraction_to_base_verb(contraction: str) -> str:
    """
    Determine the base verb from a given negative contraction (e.g.,
    "won't" -> "will").

    Args:
        contraction: The contraction to analyze.

    Returns:
        str: The base verb corresponding to the contraction.
    """
    straight_contraction: str = curly_to_straight(contraction).lower()

    # Look for the contraction in the unambiguous contractions map.
    expanded_contraction: str = UNAMBIGUOUS_CONTRACTIONS_MAP.get(
        straight_contraction, ''
    )

    if not expanded_contraction:
        # Fallback for edge cases: strip n't
        return straight_contraction.replace("n't", '')

    # "Cannot" is a special case.
    if expanded_contraction == 'cannot':
        return 'can'

    # Return the first word of the expansion.
    return expanded_contraction.split()[0]


def expand_contractions_from_doc(doc: Doc) -> str:
    """
    Expand all contractions in a given spaCy ``Doc``.

    Args:
        doc: A spaCy ``Doc``.

    Returns:
        str: The converted ``Doc`` text.
    """
    matches:list[re.Match[str]] = list(
        WarpingPatterns.CONTRACTION.finditer(doc.text)
    )
    if not matches:
        return doc.text

    expanded_parts: list[str] = []
    last_idx: int = 0
    skip_until_idx: int = -1

    for match in matches:
        start_char: int
        end_char: int

        start_char, end_char = match.span()

        # If a previous inverted expansion already consumed this token,
        # skip it.
        if start_char < skip_until_idx:
            continue

        # Append all text from the previous contraction (or beginning)
        # to the current contraction.
        expanded_parts.append(doc.text[last_idx:start_char])
        contraction: str = match.group(0)

        # Check if complex negation/ambiguity logic is needed.
        is_negation: bool = bool(WarpingPatterns.N_T_SUFFIX.search(contraction))
        is_ambiguous: bool = bool(
            WarpingPatterns.AMBIGUOUS_CONTRACTION.match(contraction)
        )

        if is_negation or is_ambiguous:
            span: Span | None = doc.char_span(start_char, end_char)
            if span:
                expanded_text: str
                new_end_char: int

                expanded_text, new_end_char = _expand_ambiguous_contraction(
                    contraction, span, doc
                )
                expanded_parts.append(expanded_text)
                last_idx = new_end_char
                skip_until_idx = new_end_char
                continue

        # For unambiguous contractions, use the unambiguous contractions
        # map.
        cased_expansion: str = _expand_unambiguous_contraction(
            contraction,
            UNAMBIGUOUS_CONTRACTIONS_MAP
        )

        expanded_parts.append(cased_expansion)
        last_idx = end_char

    expanded_parts.append(doc.text[last_idx:])
    return ''.join(expanded_parts)
