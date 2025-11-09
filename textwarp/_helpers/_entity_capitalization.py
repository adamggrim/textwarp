from spacy.tokens import Doc, Span, Token

from .._config import LOWERCASE_PARTICLES
from .._constants import (
    OPEN_QUOTES,
    PROPER_NOUN_ENTITIES,
    TITLE_CASE_TAG_EXCEPTIONS
)
from .._enums import Casing
from .._regexes import WarpingPatterns

from ._string_capitalization import capitalize_from_string


def _find_next_word_token_index(
    start_index: int,
    text_container: Doc | Span
) -> int | None:
    """
    Find the index of the next non-space, non-punctuation token in a
    spaCy ``Doc`` or ``Span``.

    Args:
        start_index: The relative index in the text container to
            start the search from.

    Returns:
        int | None: The doc index of the next word token, or
            ``None`` if no non-space, non-punctuation token is
            found.
    """
    for i in range(start_index, len(text_container)):
        token: Token = text_container[i]
        if not token.is_space and not token.is_punct:
            return token.i
    return None


def _should_always_lowercase(token: Token) -> bool:
    """
    Determine if a token should always be lowercase.

    This occurs when it is a lowercase particle (e.g., "de", "von") or a
    contraction suffix (e.g., "'ve", "n't").

    Args:
        token: The spaCy token to check.

    Returns:
        bool: ``True`` if the token should always be lowercase, otherwise
            ``False``.
    """
    return (token.text.lower() in LOWERCASE_PARTICLES or
        WarpingPatterns.CONTRACTION_SUFFIX_TOKENS_PATTERN
        .fullmatch(token.text))


def _should_capitalize_pos_or_length(token: Token) -> bool:
    """
    Determine whether a spaCy token should be capitalized for title
    case based on its part of speech or length.

    Args:
        token: The spaCy token to check.

    Returns:
        bool: ``True`` if the tag should be capitalized, otherwise
            ``False``.
    """
    if _should_always_lowercase(token):
        return False
    # Capitalize long words regardless of POS tag.
    if len(token.text) >= 5:
        return True

    return token.tag_ not in TITLE_CASE_TAG_EXCEPTIONS


def _to_title_case_from_token(token: Token, should_capitalize: bool) -> str:
    """
    Convert a spaCy token to title case, handling special name prefixes
    and preserving other mid-word capitalizations.

    Args:
        token: The spaCy token to convert.
        should_capitalize: A flag indicating if the token should be
            capitalized.

    Returns:
        str: The converted token.
    """
    # Preserve the token if it contains only whitespace or is a
    # contraction suffix.
    if token.is_space or (
        WarpingPatterns.CONTRACTION_SUFFIX_TOKENS_PATTERN
        .fullmatch(token.text)
    ):
        return token.text
    elif should_capitalize:
        return capitalize_from_string(token.text)
    else:
        return token.text.lower()


def locate_sentence_start_indices(text_container: Doc | Span) -> set[int]:
    """
    Find the indices of tokens that should be capitalized for sentence
    case.

    Args:
        text_container: The spaCy ``Doc`` or ``Span`` to analyze.

    Returns:
        set[int]: A set containing the indices of the first token of
            each sentence.
    """
    position_indices: set[int] = set()

    for i, token in enumerate(text_container):
        # Find the first word token in each sentence.
        if token.is_sent_start:
            next_word_index = _find_next_word_token_index(i, text_container)
            if next_word_index is not None:
                position_indices.add(next_word_index)

    return position_indices


def locate_start_case_indices(text_container: Doc | Span) -> set[int]:
    """
    Find the indices of tokens that should be capitalized for start
    case (i.e., all word tokens).

    Args:
        text_container: The spaCy ``Doc`` or ``Span`` to analyze.

    Returns:
        set[int]: A set containing the indices of all word tokens.
    """
    word_indices: set[int] = set()

    for token in text_container:
        if not token.is_space and not token.is_punct:
            word_indices.add(token.i)

    return word_indices


def locate_title_case_indices(text_container: Doc | Span) -> set[int]:
    """
    Find the indices of tokens that should be capitalized for title
    case.

    This includes tokens at the start of a sentence, after a colon, at
    the end of the ``Doc`` or that should be capitalized based on their part
    of speech or length.

    Args:
        text_container: The spaCy ``Doc`` or ``Span`` to analyze.

    Returns:
        set[int]: A set containing the set of first word indices and the
            last word index.
    """
    position_indices: set[int] = set()

    for i, token in enumerate(text_container):
        # Find the first word token in each sentence, `Doc` or `Span`.
        if i == 0 or token.is_sent_start:
            next_word_index = _find_next_word_token_index(i, text_container)
            if next_word_index is not None:
                position_indices.add(next_word_index)
        # Find the first word token after a colon or opening quote.
        elif (token.text in {':'} | OPEN_QUOTES
              and token.i + 1 < len(text_container)):
            next_word_index = _find_next_word_token_index(
                i + 1, text_container
            )
            if next_word_index is not None:
                position_indices.add(next_word_index)
        # Find tokens that should be capitalized based on POS or length.
        elif _should_capitalize_pos_or_length(token):
            position_indices.add(token.i)

    # Find the index of the last word.
    for token in reversed(text_container):
        if not token.is_space and not token.is_punct:
            position_indices.add(token.i)
            break

    return position_indices


def map_proper_noun_entities(doc: Doc) -> dict[int, tuple[Span, int]]:
    """
    Create a map of specific proper noun entity indices and Span objects
    from a spaCy ``Doc``.

    Args:
        doc: The spaCy ``Doc`` to convert.

    Returns:
        dict[int, tuple[Span, int]]: A dictionary where each key is an
            entity's start token index and each value is a tuple
            containing the entity's spaCy Span object and its end token
            index.
    """
    return {
        ent.start: (ent, ent.end) for ent in doc.ents
        if ent.label_ in PROPER_NOUN_ENTITIES
    }


def to_title_case_from_doc(text_container: Doc | Span) -> str:
    """
    Convert a spaCy ``Doc`` or ``Span`` to a title case string, handling special
    name prefixes and preserving other mid-word capitalizations.

    Args:
        text_container: The spaCy ``Doc`` or ``Span`` to convert.

    Returns:
        str: The converted ``Doc`` or ``Span`` text.
    """
    # Find the indices of tokens that should always be capitalized based
    # on their position.
    position_indices: set[int] = locate_title_case_indices(text_container)
    processed_parts: list[str] = []

    for token in text_container:
        should_capitalize: bool = token.i in position_indices
        processed_token: str = _to_title_case_from_token(
            token, should_capitalize=should_capitalize
        )
        processed_parts.append(processed_token + token.whitespace_)

    return ''.join(processed_parts)
