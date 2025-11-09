from typing import Callable

import regex as re
from spacy.tokens import Doc, Span, Token

from .._enums import CaseSeparator, Casing
from .._regexes import ProgrammingCasePatterns

from ._entity_capitalization import (
    locate_sentence_start_indices,
    locate_start_case_indices,
    locate_title_case_indices,
    map_proper_noun_entities,
    to_title_case_from_doc
)
from ._punctuation import remove_apostrophes
from ._string_capitalization import capitalize_from_string


def change_first_letter_case(
    word: str,
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
    for i, char in enumerate(word):
        if char.isalpha():
            # Modify the first letter and return the new text.
            return word[:i] + casing_func(char) + word[i+1:]

    # Return the original text if there are no letters in the string.
    return word


def doc_to_case(doc: Doc, casing: Casing) -> str:
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
    entity_map: dict[int, tuple[Span, int]] = (
        map_proper_noun_entities(doc)
    )

    processed_parts: list[str] = []
    token_indices: set[int] = set()
    lowercase_by_default: bool = True
    i: int = 0

    if casing == Casing.SENTENCE:
        token_indices = locate_sentence_start_indices(doc)
    elif casing == Casing.START:
        token_indices = locate_start_case_indices(doc)
        lowercase_by_default = False
    elif casing == Casing.TITLE:
        token_indices = locate_title_case_indices(doc)

    # Loop through each token in the `Doc` to look for indices that
    # should be cased.
    while i < len(doc):
        # Check if the current token is part of a proper noun entity.
        if i in entity_map and casing in {Casing.SENTENCE, Casing.TITLE}:
            entity_span: Span
            end_index: int
            entity_span, end_index = entity_map[i]
            lower_entity_text: str = entity_span.text.lower()
            title_cased_entity_text: str

            title_cased_entity_text: str = to_title_case_from_doc(
                entity_span
            )
            processed_parts.append(title_cased_entity_text)
            # Jump the index to the end of the entity.
            i = end_index
            continue

        # If the curent token is not part of a proper noun entity,
        # process it as a normal string.
        token: Token = doc[i]
        token_text: str = doc[i].text

        if i in token_indices:
            processed_parts.append(
                capitalize_from_string(token_text)
            )
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
    no_apostrophes_text: str = remove_apostrophes(text)
    parts: list[str] = (
        ProgrammingCasePatterns.SPLIT_FOR_SEPARATOR_CONVERSION.split(
            no_apostrophes_text
        )
    )
    processed_parts: list[str] = []

    separator_pattern_name: str = f'{separator.name}_WORD'
    separator_pattern: re.Pattern = getattr(
        ProgrammingCasePatterns,
        separator_pattern_name
    )
    other_separators: list[CaseSeparator] = [
        s for s in CaseSeparator if s != separator
    ]

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
            lower_words: list[str] = [word.lower() for word in broken_words]
            processed_part = separator.value.join(lower_words)
        # Part is not in any of the above cases.
        else:
            processed_part = part.lower()
        processed_parts.append(processed_part)

    return ''.join(processed_parts)
