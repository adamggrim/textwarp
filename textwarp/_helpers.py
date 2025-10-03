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


def _title_case_entities_from_doc(
    doc: Doc
) -> dict[int, tuple[str, int]]:
    """
    Convert the entities in a spaCy Doc to title case.

    Args:
        doc: The spaCy Doc to convert.

    Returns:
        dict[str, str]: A dictionary keyed by the entity start token
            index, with the value a tuple of the title-case entity text
            and end token index.
    """
    return {
        ent.start: (_to_title_case_from_doc(ent), ent.end)
        for ent in doc.ents
        if ent.label_ in PROPER_NOUN_ENTITIES
    }


def _capitalize_from_map(
    lower_word: str,
    capitalization_map: dict
) -> str | None:
    """
    Handle word capitalization through dictionary lookup, lowercasing
    any suffix.

    Args:
        lower_word: The lowercase word.
        capitalization_map: A dictionary with lowercase words as keys
            and their capitalized versions as values.

    Returns:
        str | None: The capitalized initialism, or None if lower_word is
            not in the map.
    """
    match = WarpingPatterns.MAP_SUFFIX_EXCEPTIONS.search(lower_word)

    if match:
        split_start = match.start()
        base = lower_word[:split_start]
        suffix = lower_word[split_start:]

        # Look up the base part in the map.
        capitalized_base = capitalization_map.get(base)

        if capitalized_base:
            # If the base is in the map, recombine it with the
            # lowercase suffix.
            return f'{capitalized_base}{suffix.lower()}'
        return None
    else:
        return capitalization_map.get(lower_word)


def _capitalize_from_string(
    word: str,
    lowercase_by_default: bool = False,
) -> str:
    """
    Capitalize a word, handling special name prefixes and preserving
    other mid-word capitalizations.

    Args:
        word: The word to capitalize.
        lowercase_by_default: Whether to lowercase the word if no
            capitalization strategy applies. Defaults to True.

    Returns:
        str: The capitalized word.
    """
    if not word or not word[0].isalpha():
        return word

    lower_word: str = word.lower()

    capitalization_strategies: list[Callable[[str, str], str | None]] = [
        _handle_i_pronoun,
        _handle_capitalized_abbreviation,
        _handle_initialism,
        _handle_mixed_case_word,
        _handle_period_separated_initialism,
        _handle_prefixed_name,
        _preserve_existing_capitalization
    ]

    if lowercase_by_default:
        capitalization_strategies.insert(4, _handle_lowercase_abbreviation)

    for strategy in capitalization_strategies:
        word_result: str | None = strategy(word, lower_word)
        if word_result is not None:
            return word_result

    return word.capitalize() if not lowercase_by_default else lower_word


def _capitalize_from_token(
    token: Token,
    lowercase_by_default: bool = False,
) -> str:
    """
    Capitalize a spaCy token, handling special name prefixes and
    preserving other mid-word capitalizations.

    Args:
        token: The spaCy token to capitalize.
        lowercase_by_default: Whether to lowercase the word if no
            capitalization strategy applies. Defaults to True.

    Returns:
        str: The capitalized word.
    """
    lower_token: str = token.text.lower()

    # Call with lowercase_by_default set to True to ensure a lowercase
    # function return if no capitalization occurs.
    string_result: str = _capitalize_from_string(
        token.text,
        lowercase_by_default=True
    )
    if string_result != token.text.lower():
        return string_result

    token_result: str | None = _handle_proper_noun(token)
    if token_result is not None:
        return token_result

    return token.text.capitalize() if not lowercase_by_default else lower_token


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


def _locate_title_case_indices(text_container: Doc | Span) -> set[int]:
    """
    Find the indices of tokens that should be capitalized in title case
    based on their position.

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
        # Find the first word token in a sentence.
        if token.is_sent_start:
            # Keep the range within a Doc's or Span's boundaries.
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
        # Find the most recent word token.
        if not token.is_space and not token.is_punct:
            last_word_index = token.i

    # Add the index of the last word found.
    if last_word_index != -1:
        position_indices.add(last_word_index)

    return position_indices


def _handle_capitalized_abbreviation(
    _word: str,
    lower_word: str
) -> str | None:
    """
    Handle the capitalization of an abbreviation that should be
    capitalized.

    Args:
        _word: The word to capitalize (unused).
        lower_word: The lowercase word.

    Returns:
        str | None: The capitalized abbreviation, or None if lower_word
            is not in CAPITALIZED_ABBREVIATIONS_MAP.
    """
    capitalized_word = _capitalize_from_map(
        lower_word.removesuffix('.'), CAPITALIZED_ABBREVIATIONS_MAP
    )
    return capitalized_word if capitalized_word else None


def _handle_initialism(_word: str, lower_word: str) -> str | None:
    """
    Handle the capitalization of an initialism without hyphens or periods.

    Args:
        _word: The word to capitalize (unused).
        lower_word: The lowercase word.

    Returns:
        str | None: The capitalized initialism, or None if lower_word is
            not in INITIALISMS_MAP.
    """
    return _capitalize_from_map(lower_word, INITIALISMS_MAP)


def _handle_i_pronoun(_word: str, lower_word: str) -> str | None:
    """
    Handle the capitalization of the "I" pronoun.

    Args:
        _word: The word to capitalize (unused).
        lower_word: The lowercase word.

    Returns:
        str | None: The capitalized pronoun "I", or None if the input is
            not "i".
    """
    if lower_word == 'i':
        return 'I'
    return None


def _handle_lowercase_abbreviation(_word: str, lower_word: str,) -> str | None:
    """
    Preserve the capitalization of a lowercase abbreviation.

    Args:
        _word: The word to capitalize (unused).
        lower_word: The lowercase word.

    Returns:
        str | None: The lowercase abbreviation, or None if lower_word is
            not in LOWERCASE_ABBREVIATIONS.
    """
    if lower_word.removesuffix('.') in LOWERCASE_ABBREVIATIONS:
        return lower_word
    return None


def _handle_mixed_case_word(_word: str, lower_word: str,) -> str | None:
    """
    Handle mixed-case capitalization.

    Args:
        _word: The word to capitalize (unused).
        lower_word: The lowercase word.

    Returns:
        str | None: The mixed-case word, or None if lower_word is
            not in MIXED_CASE_WORDS_MAP.
    """
    return _capitalize_from_map(lower_word, MIXED_CASE_WORDS_MAP)


def _handle_period_separated_initialism(
    _word: str,
    lower_word: str
) -> str | None:
    """
    Handle the capitalization of a period-separated initialism.

    Args:
        _word: The word to capitalize (unused).
        lower_word: The lowercase word.

    Returns:
        str | None: The capitalized initialism, or None if the
            word does not contain a period.
    """
    if WarpingPatterns.PERIOD_SEPARATED_INITIALISM.match(lower_word):
        parts = lower_word.split('.')
        return '.'.join(
            [part.upper() if not WarpingPatterns.ANY_APOSTROPHE.search(part)
             else part.lower() for part in parts]
        )
    return None


def _handle_prefixed_name(_word: str, lower_word: str) -> str | None:
    """
    Handle the capitalization of a prefixed name.

    Args:
        _word: The name to capitalize (unused).
        lower_word: The lowercase name.

    Returns:
        str | None: The capitalized name, or None if the
            string starts with a name prefix exception.
    """
    if WarpingPatterns.NAME_PREFIX_EXCEPTION_PATTERN.match(lower_word):
        return None
    elif (match := WarpingPatterns.NAME_PREFIX_PATTERN.match(lower_word)):
        prefix_len = len(match.group(0))
        return (lower_word[:prefix_len].capitalize() +
                lower_word[prefix_len:].capitalize())
    elif WarpingPatterns.OTHER_PREFIXED_NAMES_PATTERN.match(lower_word):
        return _capitalize_from_map(lower_word, OTHER_PREFIXED_NAMES_MAP)
    return None


def _preserve_existing_capitalization(word: str, _lower_word: str,) -> str:
    """
    Preserve the capitalization of a word that is already mixed-case.

    Args:
        word: The word to check.
        _lower_word: The lowercase word (unused).

    Returns:
        str: The original word, or None if the word is all
            lowercase or uppercase.
    """
    if not word.islower() and not word.isupper():
        return word
    return None


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


def _should_capitalize_pos(token: Token) -> bool:
    """
    Determine whether a token should be capitalized for title case
    based on its part of speech.

    Args:
        tag: The spaCy POS tag to check.

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
    converted_parts: list[str] = []

    separator_pattern_name: str = f'{separator.name}_WORD'
    separator_pattern = getattr(
        ProgrammingCasePatterns,
        separator_pattern_name
    )
    other_separators = [s for s in CaseSeparator if s != separator]

    for i, part in enumerate(parts):
        converted_part: str
        # Part contains no alphabetical characters and is not a single
        # space.
        if not any(char.isalpha() for char in part) and part != ' ':
            converted_parts.append(part)
            continue
        # Part is a single space.
        elif part == ' ':
            # Default to keeping the space.
            converted_part = part
            # Check if the space is surrounded by lowercase parts.
            if i > 0 and i < len(parts) - 1:
                prev_part = parts[i - 1]
                next_part = parts[i + 1]
                if (prev_part.isalpha() and prev_part.islower() and
                        next_part.isalpha() and next_part.islower()):
                    converted_part = separator.value
        # Part is already in the given separator case.
        elif separator_pattern.match(part):
            converted_part = part
        # Part is in another separator case.
        elif any(
            getattr(ProgrammingCasePatterns, f'{s.name}_WORD').match(part)
            for s in other_separators
        ):
            converted_part = (
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
            converted_part = separator.value.join(lower_words)
        # Part is not in any of the above cases.
        else:
            converted_part = part.lower()
        converted_parts.append(converted_part)

    return ''.join(converted_parts)


def _to_title_case_from_doc(text_container: Doc | Span) -> str:
    """
    Convert a spaCy Doc to a title-case string, handling special name
    prefixes and preserving other mid-word capitalizations.

    Args:
        text_container: The spaCy Doc or Span to convert.

    Returns:
        str: The converted Doc text.
    """
    # Find the indices of tokens that should always be capitalized based
    # on their position.
    position_indices = _locate_title_case_indices(text_container)

    title_case_tokens: list[str] = []

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
