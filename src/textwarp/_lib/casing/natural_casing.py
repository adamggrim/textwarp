"""Functions for converting between natural cases."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import (
        Doc,
        Span,
        Token
    )

from textwarp._core.context import ctx
from textwarp._core.enums import Casing
from textwarp._core.utils import change_first_letter_case
from textwarp._lib.casing.entity_casing import map_all_entities
from textwarp._lib.casing.string_casing import case_from_string
from textwarp._lib.casing.token_casing import should_capitalize_pos_or_length

__all__ = ['to_natural_case']


def _find_first_word_token_idx(
    start_idx: int,
    text_container: Doc | Span
) -> int | None:
    """
    Find the index of the first non-space, non-punctuation token in a
    spaCy `Doc` or `Span`.

    Args:
        start_idx: The relative index in the text container for
            starting the search.

    Returns:
        int | None: The index of the first word token, or `None` if
            there is no non-space, non-punctuation token.
    """
    for i in range(start_idx, len(text_container)):
        token = text_container[i]
        if not token.is_space and not token.is_punct:
            return token.i
    return None


def _find_force_lowercase_idxs(text_container: Doc | Span) -> set[int]:
    """
    Find indices of tokens to forcefully lowercase if the entire sentence
    shares the same casing (e.g., all uppercase or all capitalized).

    Args:
        text_container: The spaCy `Doc` or `Span` to search.

    Returns:
        set[int]: A set of token indices that should be lowercased.
    """
    def is_capitalized(word: str) -> bool:
        return word[0].isupper() and word[1:].islower()

    sentences = getattr(text_container, 'sents', [text_container])
    indices_to_lowercase: set[int] = set()

    for sent in sentences:
        words = [token for token in sent if token.is_alpha]
        if not words:
            continue

        all_upper = True
        all_capitalized = True

        for w in words:
            word_text = w.text
            if all_upper and not word_text.isupper():
                all_upper = False
            if all_capitalized and not is_capitalized(word_text):
                all_capitalized = False

            if not all_upper and not all_capitalized:
                break

        if all_upper or (all_capitalized and len(words) > 1):
            for token in sent:
                if token.is_alpha:
                    indices_to_lowercase.add(token.i)

    return indices_to_lowercase


def _find_sentence_start_idxs(text_container: Doc | Span) -> set[int]:
    """
    Find the index of the first word token in each sentence.

    Args:
        text_container: The spaCy `Doc` or `Span` to search.

    Returns:
        set[int]: A set containing the index of the first word token
            in each sentence.
    """
    sentences = getattr(text_container, 'sents', [text_container])
    sent_start_idxs: set[int] = set()

    for sent in sentences:
        first_word_idx = _find_first_word_token_idx(0, sent)
        if first_word_idx is not None:
            sent_start_idxs.add(first_word_idx)

    return sent_start_idxs


def _find_start_case_idxs(text_container: Doc | Span) -> set[int]:
    """
    Find the indices of tokens that should be capitalized for start
    case (i.e., all word tokens).

    Args:
        text_container: The spaCy `Doc` or `Span` to search.

    Returns:
        set[int]: A set of indices corresponding to word tokens.
    """
    word_idxs: set[int] = set()

    for token in text_container:
        if not token.is_space and not token.is_punct:
            word_idxs.add(token.i)

    return word_idxs


def _find_title_case_idxs(text_container: Doc | Span) -> set[int]:
    """
    Find the indices of tokens that should be capitalized for title
    case.

    This includes tokens at the start of a sentence, after a colon, at
    the end of the `Doc` or that should be capitalized based on their
    part of speech or length.

    Args:
        text_container: The spaCy `Doc` or `Span` to search.

    Returns:
        set[int]: A set of token indices that should be capitalized for
            title case.
    """
    position_idxs: set[int] = set()

    for i, token in enumerate(text_container):
        is_valid_punctuation_boundary = (
            (token.text == ':' or token.text in ctx.provider.open_quotes)
            and token.i + 1 < len(text_container)
        )

        if i == 0 or token.is_sent_start:
            first_word_idx: int | None = _find_first_word_token_idx(
                i, text_container
            )
            if first_word_idx is not None:
                position_idxs.add(first_word_idx)
        elif is_valid_punctuation_boundary:
            first_word_idx = _find_first_word_token_idx(
                i + 1, text_container
            )
            if first_word_idx is not None:
                position_idxs.add(first_word_idx)
        elif should_capitalize_pos_or_length(token):
            position_idxs.add(token.i)

    for token in reversed(text_container):
        if not token.is_space and not token.is_punct:
            position_idxs.add(token.i)
            break

    return position_idxs


def _to_title_case_from_doc(
    text_container: Doc | Span,
    indices_to_lowercase: set[int]
) -> str:
    """
    Convert a spaCy `Doc` or `Span` to a title case string, handling special
    name prefixes and preserving other mid-word capitalizations.

    Args:
        text_container: The spaCy `Doc` or `Span` to convert.
        indices_to_lowercase: A set of token indices to forcefully lowercase.

    Returns:
        str: The converted string.
    """
    position_idxs = _find_title_case_idxs(text_container)
    processed_parts: list[str] = []

    for token in text_container:
        token_text = token.text
        if token.i in indices_to_lowercase:
            token_text = token_text.lower()

        should_capitalize_for_title = token.i in position_idxs
        processed_token = _to_title_case_from_token(
            token,
            token_text,
            should_capitalize_for_title=should_capitalize_for_title
        )
        processed_parts.append(processed_token + token.whitespace_)

    return ''.join(processed_parts)


def _to_title_case_from_token(
    token: Token,
    token_text: str,
    should_capitalize_for_title: bool
) -> str:
    """
    Convert a spaCy `Token` to title case, handling special name prefixes
    and preserving other mid-word capitalizations.

    Args:
        token: The spaCy `Token` to convert.
        token_text: The normalized token text.
        should_capitalize_for_title: A flag indicating whether the
            token should be capitalized.

    Returns:
        str: The converted token.
    """
    if token.is_space or ctx.provider.should_always_lowercase(token_text):
        return token_text
    if token_text.isupper():
        return token_text
    if should_capitalize_for_title:
        return case_from_string(token_text)
    return token_text.lower()


def to_natural_case(doc: Doc, casing: Casing) -> str:
    """
    Apply sentence, start or title case to a spaCy `Doc`, capitalizing
    any proper noun entities.

    Args:
        doc (Doc): A spaCy `Doc`.
        casing (Casing): The target casing to apply, either
            `Casing.SENTENCE`, `Casing.START` or `Casing.TITLE`.

    Returns:
        str: The cased string.
    """
    entity_map: dict[int, tuple[Span, int, str | None]] = map_all_entities(doc)

    processed_parts: list[str] = []
    token_idxs: set[int] = set()
    indices_to_lowercase: set[int] = set()
    i = 0

    if casing == Casing.SENTENCE:
        token_idxs = _find_sentence_start_idxs(doc)
        indices_to_lowercase = _find_force_lowercase_idxs(doc)
    elif casing == Casing.START:
        token_idxs = _find_start_case_idxs(doc)
    elif casing == Casing.TITLE:
        token_idxs = _find_title_case_idxs(doc)
        indices_to_lowercase = _find_force_lowercase_idxs(doc)

    while i < len(doc):
        if i in entity_map and casing == Casing.TITLE:
            entity_span, end_idx, absolute_capitalization = entity_map[i]

            if absolute_capitalization:
                trailing_whitespace = entity_span[-1].whitespace_
                processed_parts.append(
                    absolute_capitalization + trailing_whitespace
                )
            else:
                title_cased_entity_text: str = _to_title_case_from_doc(
                    entity_span, indices_to_lowercase
                )
                processed_parts.append(title_cased_entity_text)

            i = end_idx
            continue

        token = doc[i]
        token_text = token.text

        if i in indices_to_lowercase:
            token_text = token_text.lower()

        is_capitalized_pos = i in token_idxs

        if casing == Casing.SENTENCE:
            if is_capitalized_pos:
                processed_parts.append(change_first_letter_case(
                    token_text, str.upper
                ))
            else:
                processed_parts.append(token_text)
        elif casing == Casing.TITLE:
            processed_parts.append(
                _to_title_case_from_token(
                    token,
                    token_text,
                    should_capitalize_for_title=is_capitalized_pos
                )
            )
        else:
            processed_parts.append(
                case_from_string(
                    token_text,
                    lowercase_by_default=False,
                    preserve_mixed_case=True
                )
            )

        processed_parts.append(token.whitespace_)
        i += 1

    return ''.join(processed_parts)
