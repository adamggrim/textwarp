"""Functions for converting between cases (title, Pascal, etc.)."""

from spacy.tokens import Token
from typing import Callable

import regex as re
from spacy.tokens import (
    Doc,
    Span
)

from .._constants.variants import OPEN_QUOTES
from .._constants.regexes import WarpingPatterns

from .._enums import (
    CaseSeparator,
    Casing
)
from .._constants import (
    CaseConversionPatterns,
    CasePatterns
)
from .apostrophes import remove_apostrophes
from .entity_capitalization import map_all_entities
from .string_capitalization import capitalize_from_string
from .token_capitalization import should_capitalize_pos_or_length

__all__ = [
    'change_first_letter_case',
    'doc_to_case',
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
        start_idx: The relative index in the text container to
            start the search from.

    Returns:
        int | None: The doc index of the first word token, or
            ``None`` if no non-space, non-punctuation token is
            found.
    """
    for i in range(start_idx, len(text_container)):
        token = text_container[i]
        if not token.is_space and not token.is_punct:
            return token.i
    return None


def _find_sentence_case_indices(
    text_container: Doc | Span
) -> tuple[set[int], set[int]]:
    """
    Find the indices of tokens that should be capitalized or lowercased
    for sentence case.

    Args:
        text_container: The spaCy ``Doc`` or ``Span`` to analyze.

    Returns:
        tuple[set[int], set[int]]:
            1. sent_start_indices: A list of the first token in each
                sentence.
            2. indices_to_lowercase: A list of words after the first
                word that are currently capitalized or uppercase, as
                long as all words in the text follow the same casing
                (i.e., all capitalized or all uppercase).
    """
    sent_start_indices: set[int] = set()
    indices_to_lowercase: set[int] = set()

    for sent in text_container.sents:
        first_word_idx = _find_first_word_token_idx(0, sent)

        if first_word_idx is None:
            continue

        sent_start_indices.add(first_word_idx)

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

    return sent_start_indices, indices_to_lowercase


def _find_start_case_indices(text_container: Doc | Span) -> set[int]:
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


def _find_title_case_indices(text_container: Doc | Span) -> set[int]:
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
            first_word_idx: int | None = _find_first_word_token_idx(
                i, text_container
            )
            if first_word_idx is not None:
                position_indices.add(first_word_idx)
        # Find the first word token after a colon or opening quote.
        elif (token.text in {':'} | OPEN_QUOTES
              and token.i + 1 < len(text_container)):
            first_word_idx = _find_first_word_token_idx(
                i + 1, text_container
            )
            if first_word_idx is not None:
                position_indices.add(first_word_idx)
        # Find tokens that should be capitalized based on POS or length.
        elif should_capitalize_pos_or_length(token):
            position_indices.add(token.i)

    # Find the index of the last word.
    for token in reversed(text_container):
        if not token.is_space and not token.is_punct:
            position_indices.add(token.i)
            break

    return position_indices


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
    position_indices = _find_title_case_indices(text_container)
    processed_parts: list[str] = []

    for token in text_container:
        should_capitalize_for_title = token.i in position_indices
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
        WarpingPatterns.CONTRACTION_SUFFIXES_PATTERN
        .fullmatch(token.text)
    ):
        return token.text
    elif should_capitalize_for_title:
        return capitalize_from_string(token.text)
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
    for i, char in enumerate(text):
        if char.isalpha():
            # Modify the first letter and return the new text.
            return text[:i] + casing_func(char) + text[i+1:]

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
    token_indices: set[int] = set()
    i = 0

    if casing == Casing.SENTENCE:
        token_indices, indices_to_lowercase = _find_sentence_case_indices(doc)
        lowercase_by_default = True
    elif casing == Casing.START:
        token_indices = _find_start_case_indices(doc)
        lowercase_by_default = False
    elif casing == Casing.TITLE:
        token_indices = _find_title_case_indices(doc)
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

        if i in token_indices:
            processed_parts.append(
                capitalize_from_string(token_text)
            )
        elif casing == Casing.SENTENCE and i in indices_to_lowercase:
            processed_parts.append(token_text.lower())
        else:
            processed_parts.append(
                capitalize_from_string(token_text, lowercase_by_default)
            )

        processed_parts.append(token.whitespace_)
        i += 1

    return ''.join(processed_parts)


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
        elif (CasePatterns.CAMEL_WORD.match(part)
              or CasePatterns.PASCAL_WORD.match(part)):
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
    return capitalize_from_string(word)
