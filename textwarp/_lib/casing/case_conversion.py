"""Functions for converting between cases (title, Pascal, etc.)."""

from __future__ import annotations

from typing import Callable, TYPE_CHECKING

import regex as re
if TYPE_CHECKING:
    from spacy.tokens import (
        Doc,
        Span,
        Token
    )

from textwarp._core.constants.regexes import (
    CaseConversionPatterns,
    CasePatterns,
    WarpingPatterns
)
from textwarp._core.constants.apostrophes import OPEN_QUOTES
from textwarp._core.enums import CaseSeparator, Casing
from textwarp._lib.casing.entity_casing import map_all_entities
from textwarp._lib.casing.string_casing import case_from_string
from textwarp._lib.casing.token_casing import should_capitalize_pos_or_length
from textwarp._lib.punctuation import remove_apostrophes

__all__ = [
    'change_first_letter_case',
    'doc_to_case',
    'find_first_alphabetical_idx',
    'to_separator_case',
    'word_to_pascal'
]


def _find_first_word_token_idx(
    start_idx: int,
    text_container: Doc | Span
) -> int | None:
    """
    Find the index of the first non-space, non-punctuation token in a
    spaCy ``Doc`` or ``Span``.

    Args:
        start_idx: The relative index in the text container for
            starting the search.

    Returns:
        int | None: The index of the first word token, or ``None`` if
            there is no non-space, non-punctuation token.
    """
    for i in range(start_idx, len(text_container)):
        token = text_container[i]
        if not token.is_space and not token.is_punct:
            return token.i
    return None


def _find_sentence_case_idxs(
    text_container: Doc | Span
) -> tuple[set[int], set[int]]:
    """
    Find the indices of tokens that should be capitalized or lowercased
    for sentence case.

    Args:
        text_container: The spaCy ``Doc`` or ``Span`` to search.

    Returns:
        tuple[set[int], set[int]]:
            1. sent_start_idxs: A list of the first token in each
                sentence.
            2. indices_to_lowercase: A list of words after the first
                word that are currently capitalized or uppercase, as
                long as all words in the text follow the same casing
                (i.e., all capitalized or all uppercase).
    """
    sent_start_idxs: set[int] = set()
    indices_to_lowercase: set[int] = set()

    for sent in text_container.sents:
        first_word_idx = _find_first_word_token_idx(0, sent)

        if first_word_idx is None:
            continue

        sent_start_idxs.add(first_word_idx)

        words = [token for token in sent if token.is_alpha]

        if not words:
            continue

        is_all_upper = all(w.text.isupper() for w in words)
        is_all_title = len(words) > 1 and all(
            w.text.istitle() for w in words
        )

        if is_all_upper or is_all_title:
            for token in sent:
                # The first word token of each sentence is always
                # capitalized.
                if token.i != first_word_idx and token.is_alpha:
                    indices_to_lowercase.add(token.i)

    return sent_start_idxs, indices_to_lowercase


def _find_start_case_idxs(text_container: Doc | Span) -> set[int]:
    """
    Find the indices of tokens that should be capitalized for start
    case (i.e., all word tokens).

    Args:
        text_container: The spaCy ``Doc`` or ``Span`` to search.

    Returns:
        set[int]: A set containing the indices of all word tokens.
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
    the end of the ``Doc`` or that should be capitalized based on their part
    of speech or length.

    Args:
        text_container: The spaCy ``Doc`` or ``Span`` to search.

    Returns:
        set[int]: A set containing the set of first word indices and the
            last word index.
    """
    position_idxs: set[int] = set()

    for i, token in enumerate(text_container):
        # Find the first word token in each sentence, `Doc` or `Span`.
        if i == 0 or token.is_sent_start:
            first_word_idx: int | None = _find_first_word_token_idx(
                i, text_container
            )
            if first_word_idx is not None:
                position_idxs.add(first_word_idx)
        # Find the first word token after a colon or opening quote.
        elif (token.text in {':'} | OPEN_QUOTES
              and token.i + 1 < len(text_container)):
            first_word_idx = _find_first_word_token_idx(
                i + 1, text_container
            )
            if first_word_idx is not None:
                position_idxs.add(first_word_idx)
        # Find tokens that should be capitalized based on POS or length.
        elif should_capitalize_pos_or_length(token):
            position_idxs.add(token.i)

    # Find the index of the last word.
    for token in reversed(text_container):
        if not token.is_space and not token.is_punct:
            position_idxs.add(token.i)
            break

    return position_idxs


def _to_title_case_from_doc(text_container: Doc | Span) -> str:
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
    position_idxs = _find_title_case_idxs(text_container)
    processed_parts: list[str] = []

    for token in text_container:
        should_capitalize_for_title = token.i in position_idxs
        processed_token = _to_title_case_from_token(
            token, should_capitalize_for_title=should_capitalize_for_title
        )
        processed_parts.append(processed_token + token.whitespace_)

    return ''.join(processed_parts)


def _to_title_case_from_token(
    token: Token,
    should_capitalize_for_title: bool
) -> str:
    """
    Convert a spaCy ``Token`` to title case, handling special name prefixes
    and preserving other mid-word capitalizations.

    Args:
        token: The spaCy ``Token`` to convert.
        should_capitalize_for_title: A flag indicating whether the
            token should be capitalized.

    Returns:
        str: The converted token.
    """
    # Preserve the token if it contains only whitespace or is a
    # contraction suffix.
    if token.is_space or (
        WarpingPatterns.CONTRACTION_SUFFIXES_PATTERN
        .fullmatch(token.text)
    ):
        return token.text
    elif should_capitalize_for_title:
        return case_from_string(token.text)
    else:
        return token.text.lower()


def change_first_letter_case(
    text: str,
    casing_func: Callable[[str], str]
) -> str:
    """
    Change the case of the first letter of a string without modifying
    any other letters.

    Args:
        text: The string to convert.
        casing_func: The function to apply to the first letter
            (i.e., ``str.upper`` or ``str.lower``).

    Returns:
        str: The converted text.
    """
    idx = find_first_alphabetical_idx(text)

    if idx is not None:
        # Modify the first letter and return the new text.
        return text[:idx] + casing_func(text[idx]) + text[idx+1:]

    # Return the original text if there are no letters in the string.
    return text


def doc_to_case(doc: Doc, casing: Casing) -> str:
    """
    Apply title or sentence case to a spaCy ``Doc``, capitalizing any
    proper noun entities.

    Args:
        doc (Doc): A spaCy ``Doc``.
        casing (Casing): The target casing to apply, either
            ``Casing.SENTENCE``, ``Casing.START`` or ``Casing.TITLE``.

    Returns:
        str: The cased string.
    """
    entity_map: dict[int, tuple[Span, int, str | None]] = map_all_entities(doc)

    processed_parts: list[str] = []
    token_idxs: set[int] = set()
    i = 0

    if casing == Casing.SENTENCE:
        token_idxs, indices_to_lowercase = _find_sentence_case_idxs(doc)
        lowercase_by_default = True
    elif casing == Casing.START:
        token_idxs = _find_start_case_idxs(doc)
        lowercase_by_default = False
    elif casing == Casing.TITLE:
        token_idxs = _find_title_case_idxs(doc)
        lowercase_by_default = True

    # Loop through each token in the ``Doc`` to find any indices that
    # should be cased.
    while i < len(doc):
        # Check if the current token is part of a proper noun entity.
        if i in entity_map and casing in {Casing.SENTENCE, Casing.TITLE}:
            entity_span, end_idx, absolute_capitalization = entity_map[i]

            # If the entity has an absolute capitalization, use it
            # directly.
            if absolute_capitalization:
                trailing_whitespace = entity_span[-1].whitespace_
                processed_parts.append(
                    absolute_capitalization + trailing_whitespace
                )
            # Otherwise, convert the entity to title case.
            else:
                title_cased_entity_text: str = _to_title_case_from_doc(
                    entity_span
                )
                processed_parts.append(title_cased_entity_text)

            # Jump to the end index of the entity.
            i = end_idx
            continue

        # If the curent token is not part of a proper noun entity,
        # process it as a normal string.
        token = doc[i]
        token_text = doc[i].text

        preserve_mixed_case = (
            casing == Casing.SENTENCE and i in indices_to_lowercase
        )
        is_sentence_start = (i in token_idxs)
        should_lowercase = lowercase_by_default and not is_sentence_start

        processed_parts.append(
            case_from_string(
                token_text,
                lowercase_by_default=should_lowercase,
                preserve_mixed_case=preserve_mixed_case
            )
        )
        processed_parts.append(token.whitespace_)
        i += 1

    return ''.join(processed_parts)


def find_first_alphabetical_idx(text: str) -> int | None:
    """
    Find the index of the first alphabetical character in a string.

    Args:
        text: The string to search.

    Returns:
        int | None: The index of the first alphabetical character, or
            ``None`` if there are no alphabetical characters.
    """
    for i, char in enumerate(text):
        if char.isalpha():
            return i
    return None


def to_separator_case(
    text: str,
    separator: CaseSeparator
) -> str:
    """
    Convert a string to dot case, kebab case or snake case.

    Args:
        text: The string to convert.
        separator: The separator for the converted string.

    Returns:
        str: The converted string.
    """
    no_apostrophes_text = remove_apostrophes(text)
    parts: list[str] = (
        CaseConversionPatterns.SPLIT_FOR_SEPARATOR_CONVERSION.split(
            no_apostrophes_text
        )
    )
    processed_parts: list[str] = []

    separator_pattern_name = f'{separator.name}_WORD'
    separator_pattern: re.Pattern[str] = getattr(
        CasePatterns,
        separator_pattern_name
    )
    other_separators: list[CaseSeparator] = [
        s for s in CaseSeparator if s != separator
    ]

    for i, part in enumerate(parts):
        # Part contains no alphabetical characters and is not a single
        # space.
        if not any(char.isalpha() for char in part) and part != ' ':
            processed_parts.append(part)
            continue
        # Part is a single space.
        elif part == ' ':
            # Default to keeping the space.
            processed_part = part
            # Check if the space is surrounded by alphabetical parts.
            if i > 0 and i < len(parts) - 1:
                prev_part = parts[i - 1]
                next_part = parts[i + 1]
                if (prev_part.isalpha() and next_part.isalpha()):
                    processed_part = separator.value
        # Part is already in the given separator case.
        elif separator_pattern.match(part):
            processed_part = part
        # Part is in another separator case.
        elif any(
            getattr(CasePatterns, f'{s.name}_WORD').match(part)
            for s in other_separators
        ):
            processed_part = (
                CaseConversionPatterns.ANY_SEPARATOR.sub(
                    separator.value,
                    part
                )
            )
        # Part is in camel or Pascal case.
        elif (CasePatterns.CAMEL_WORD.fullmatch(part)
              or CasePatterns.PASCAL_WORD.fullmatch(part)):
            # Break camel case and Pascal case into constituent words.
            broken_words: list[str] = (
                CaseConversionPatterns.SPLIT_CAMEL_OR_PASCAL.split(part)
            )
            lower_words: list[str] = [word.lower() for word in broken_words]
            processed_part = separator.value.join(lower_words)
        # Part is not in any of the above cases.
        else:
            processed_part = part.lower()
        processed_parts.append(processed_part)

    return ''.join(processed_parts)


def word_to_pascal(word: str) -> str:
    """
    Convert a single word to Pascal case.

    This function applies to words split by the
    ``SPLIT_FOR_PASCAL_CONVERSION`` regular expression.

    Args:
        word: The word to convert.

    Returns:
        str: The converted word.
    """
    # Word contains no alphabetical characters.
    if not any(char.isalpha() for char in word):
        return word
    # Word is already in Pascal case.
    if CasePatterns.PASCAL_WORD.match(word):
        return word
    # Word is in camel case.
    if CasePatterns.CAMEL_WORD.match(word):
        return change_first_letter_case(word, str.upper)
    # Word is not in Pascal or camel case.
    return case_from_string(word)
