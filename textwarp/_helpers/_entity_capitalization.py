from spacy.tokens import Doc, Span, Token

from textwarp.config import LOWERCASE_PARTICLES
from textwarp.constants import (
    PROPER_NOUN_ENTITIES,
    TITLE_CASE_TAG_EXCEPTIONS
)
from textwarp.enums import Casing
from textwarp._helpers import _capitalize_from_string
from textwarp.regexes import (
    WarpingPatterns
)


def _locate_sentence_start_indices(text_container: Doc | Span) -> set[int]:
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


def _locate_title_case_indices(text_container: Doc | Span) -> set[int]:
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
        # Find the first word token after a colon.
        elif token.text == ':' and token.i + 1 < len(text_container):
            next_word_index = _find_next_word_token_index(i + 1, text_container)
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
        token = text_container[i]
        if not token.is_space and not token.is_punct:
            return token.i
    return None


def _map_proper_noun_entities(doc: Doc) -> dict[int, tuple[Span, int]]:
    """
    Create a map of specific proper noun entities from a spaCy ``Doc``.

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
    if token.text.lower() in LOWERCASE_PARTICLES:
        return False
    # Capitalize long words regardless of POS tag.
    if len(token.text) >= 5:
        return True

    return token.tag_ not in TITLE_CASE_TAG_EXCEPTIONS


def _to_case_from_doc(doc: Doc, casing: Casing) -> str:
    """
    Apply title or sentence case to a spaCy ``Doc``, capitalizing any
    proper noun entities.

    Args:
        doc (Doc): A spaCy ``Doc``.
        casing (Casing): The target casing to apply, either
            ``Casing.SENTENCE`` or ``Casing.TITLE``.

    Returns:
        str: The cased string.
    """
    entity_indices: dict[int, tuple[Span, int]] = (
        _map_proper_noun_entities(doc)
    )

    processed_parts: list[str] = []
    token_indices: set[int] = set()
    i: int = 0

    if casing == Casing.SENTENCE:
        token_indices = _locate_sentence_start_indices(doc)
    elif casing == Casing.TITLE:
        token_indices = _locate_title_case_indices(doc)

    # Loop through each token in the `Doc` to look for indices that
    # should be cased.
    while i < len(doc):
        # Check if the current token is part of a proper noun entity.
        if i in entity_indices:
            cased_entity_text: str
            end_index: int
            entity_span, end_index = entity_indices[i]

            # Always title-case proper noun entities.
            cased_entity_text: str = _to_title_case_from_doc(entity_span)
            processed_parts.append(cased_entity_text)
            # Jump the index to the end of the entity.
            i = end_index
            continue

        # If the curent token is not part of a proper noun entity,
        # process it as a normal string, handling special name prefixes
        # and preserving other mid-word capitalizations.
        token = doc[i]
        token_text: str = doc[i].text

        if i in token_indices:
            processed_parts.append(_capitalize_from_string(token_text))
        else:
            processed_parts.append(token_text.lower())

        processed_parts.append(token.whitespace_)
        i += 1

    return ''.join(processed_parts)


def _to_title_case_from_doc(text_container: Doc | Span) -> str:
    """
    Convert a spaCy ``Doc`` or ``Span`` to a title case string, handling special
    name prefixes and preserving other mid-word capitalizations.

    This function does not capitalize proper noun entities.

    Args:
        text_container: The spaCy ``Doc`` or ``Span`` to convert.

    Returns:
        str: The converted ``Doc`` or ``Span`` text.
    """
    # Find the indices of tokens that should always be capitalized based
    # on their position.
    position_indices: set[int] = _locate_title_case_indices(text_container)
    processed_parts: list[str] = []

    for token in text_container:
        should_capitalize: bool = token.i in position_indices
        processed_token: str = _to_title_case_from_token(
            token, should_capitalize=should_capitalize
        )
        processed_parts.append(f'{processed_token}{token.whitespace_}')

    return ''.join(processed_parts)


def _to_title_case_from_token(token: Token, should_capitalize: bool) -> str:
    """
    Convert a spaCy token to a title case string, handling special name
    prefixes and preserving other mid-word capitalizations.

    Args:
        token: The token to convert.
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
        return _capitalize_from_string(token.text)
    else:
        return token.text.lower()
