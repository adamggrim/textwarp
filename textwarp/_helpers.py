from typing import Callable

import regex as re
from spacy.tokens import Doc, Span, Token

from textwarp.config import (
    CAPITALIZED_ABBREVIATIONS_MAP,
    INITIALISMS_MAP,
    LOWERCASE_ABBREVIATIONS,
    LOWERCASE_PARTICLES,
    MIXED_CASE_WORDS_MAP,
    OTHER_PREFIXED_NAMES_MAP
)
from textwarp.constants import (
    PROPER_NOUN_ENTITIES,
    TITLE_CASE_TAG_EXCEPTIONS
)
from textwarp.enums import CaseSeparator, Casing
from textwarp.regexes import (
    ProgrammingCasePatterns,
    WarpingPatterns
)


def _change_first_letter_case(
    word: str,
    casing_func: Callable[[str], str]
) -> str:
    """
    Change the case of the first letter of a string without modifying
    any other letters.

    Args:
        text: The string to convert.
        casing_func: The function to apply to the first letter
            (i.e., str.upper or str.lower).

    Returns:
        str: The converted text.
    """
    for i, char in enumerate(word):
        if char.isalpha():
            # Modify the first letter and return the new text.
            return word[:i] + casing_func(char) + word[i+1:]

    # Return the original text if there are no letters in the string.
    return word


def _locate_sentence_start_indices(text_container: Doc | Span) -> set[int]:
    """
    Find the indices of tokens that should be capitalized for sentence
    case.

    Args:
        text_container: The spaCy Doc or Span to analyze.

    Returns:
        set[int]: A set containing the indices of the first word of each
            sentence.
    """
    position_indices: set[int] = set()

    for i, token in enumerate(text_container):
        # Find the first word token in each sentence.
        if token.is_sent_start:
            for j in range(i, len(text_container)):
                candidate_token = text_container[j]
                if (not candidate_token.is_space and
                    not candidate_token.is_punct):
                    position_indices.add(j)
                    break

    return position_indices


def _locate_title_case_indices(text_container: Doc | Span) -> set[int]:
    """
    Find the indices of tokens that should be capitalized for title
    case.

    This includes tokens at the start of a sentence, after a colon or at
    the end of the Doc.

    Args:
        text_container: The spaCy Doc or Span to analyze.

    Returns:
        set[int]: A set containing the set of first word indices and the
            last word index.
    """
    position_indices: set[int] = set()
    last_word_index: int = -1

    for i, token in enumerate(text_container):
        # Find the first word token in each sentence.
        if token.is_sent_start:
            for j in range(i, len(text_container)):
                candidate_token = text_container[j]
                if (not candidate_token.is_space and
                    not candidate_token.is_punct):
                    position_indices.add(j)
                    break
        # Find the first word token after a colon.
        if token.text == ':' and token.i + 1 < len(text_container):
            for j in range(token.i + 1, len(text_container)):
                if (not text_container[j].is_space and
                    not text_container[j].is_punct):
                    position_indices.add(j)
                    break
        # Find the most recent word token to determine the last word.
        if not token.is_space and not token.is_punct:
            last_word_index = token.i

    # Add the index of the last word.
    if last_word_index != -1:
        position_indices.add(last_word_index)

    return position_indices


def _map_proper_noun_entities(doc: Doc) -> dict[int, tuple[Span, int]]:
    """
    Create a map of specific proper noun entities from a spaCy Doc.

    Args:
        doc: The spaCy Doc to convert.

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


def _remove_apostrophes(text: str) -> str:
    """
    Remove apostrophes from a string without removing single quotes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return WarpingPatterns.APOSTROPHE_IN_WORD.sub('', text)


def _replace_opening_quote(match: re.Match[str]) -> str:
    """
    Convert a sequence of straight quotes to opening curly quotes in a
    given match.

    Args:
        match: A match object where the first captured group is a
            string of one or more consecutive straight quote
            characters.

    Returns:
        str: A string of opening curly quotes.
    """
    quote_chars: str | None = match.group(1) or match.group(2)
    if quote_chars.startswith("'"):
        return '‘' * len(quote_chars)
    else:
        return '“' * len(quote_chars)


def _should_capitalize_pos_or_length(token: Token) -> bool:
    """
    Determine whether a spaCy token should be capitalized for title
    case based on its part of speech or length.

    Args:
        token: The spaCy token to check.

    Returns:
        bool: True if the tag should be capitalized, otherwise
            False.
    """
    if token.text.lower() in LOWERCASE_PARTICLES:
        return False
    # Capitalize long words regardless of POS tag.
    if len(token.text) >= 5:
        return True

    return token.tag_ not in TITLE_CASE_TAG_EXCEPTIONS


def _to_separator_case(
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
    no_apostrophes_text: str = _remove_apostrophes(text)
    parts: list[str] = (
        ProgrammingCasePatterns.SPLIT_FOR_SEPARATOR_CONVERSION.split(
            no_apostrophes_text
        )
    )
    processed_parts: list[str] = []

    separator_pattern_name: str = f'{separator.name}_WORD'
    separator_pattern = getattr(
        ProgrammingCasePatterns,
        separator_pattern_name
    )
    other_separators = [s for s in CaseSeparator if s != separator]

    for i, part in enumerate(parts):
        processed_part: str
        # Part contains no alphabetical characters and is not a single
        # space.
        if not any(char.isalpha() for char in part) and part != ' ':
            processed_parts.append(part)
            continue
        # Part is a single space.
        elif part == ' ':
            # Default to keeping the space.
            processed_part = part
            # Check if the space is surrounded by lowercase parts.
            if i > 0 and i < len(parts) - 1:
                prev_part = parts[i - 1]
                next_part = parts[i + 1]
                if (prev_part.isalpha() and prev_part.islower() and
                        next_part.isalpha() and next_part.islower()):
                    processed_part = separator.value
        # Part is already in the given separator case.
        elif separator_pattern.match(part):
            processed_part = part
        # Part is in another separator case.
        elif any(
            getattr(ProgrammingCasePatterns, f'{s.name}_WORD').match(part)
            for s in other_separators
        ):
            processed_part = (
                ProgrammingCasePatterns.ANY_SEPARATOR.sub(
                    separator.value,
                    part
                )
            )
        # Part is in camel or Pascal case.
        elif (ProgrammingCasePatterns.CAMEL_WORD.match(part)
              or ProgrammingCasePatterns.PASCAL_WORD.match(part)):
            # Break camel case and Pascal case into constituent words.
            broken_words: list[str] = (
                ProgrammingCasePatterns.SPLIT_CAMEL_OR_PASCAL.split(part)
            )
            lower_words = [word.lower() for word in broken_words]
            processed_part = separator.value.join(lower_words)
        # Part is not in any of the above cases.
        else:
            processed_part = part.lower()
        processed_parts.append(processed_part)

    return ''.join(processed_parts)


def _to_title_case_from_doc(text_container: Doc | Span) -> str:
    """
    Convert a spaCy Doc or Span to a title case string, handling special
    name prefixes and preserving other mid-word capitalizations.

    Args:
        text_container: The spaCy Doc or Span to convert.

    Returns:
        str: The converted Doc or Span text.
    """
    # Find the indices of tokens that should always be capitalized based
    # on their position.
    position_indices = _locate_title_case_indices(text_container)

    processed_parts: list[str] = []

    for token in text_container:
        # Preserve the token if it contains only whitespace or is in
        # the contraction suffixes list.
        if token.is_space or (
            WarpingPatterns.CONTRACTION_SUFFIX_TOKENS_PATTERN
            .fullmatch(token.text)
        ):
            title_case_token = token.text
        # Capitalize the token based on position or part of speech.
        elif (token.i in position_indices
            or _should_capitalize_pos(token)
        ):
            title_case_token = _capitalize_from_string(token.text)
        # Otherwise, lowercase the token.
        else:
            title_case_token = token.text.lower()

        # Add back trailing whitespace.
        title_case_tokens.append(title_case_token + token.whitespace_)

    return ''.join(title_case_tokens)
