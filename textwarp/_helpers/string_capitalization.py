from typing import Callable

from .._config import (
    CAPITALIZED_ABBREVIATIONS_MAP,
    INITIALISMS_MAP,
    LOWERCASE_ABBREVIATIONS,
    MIXED_CASE_WORDS_MAP,
    OTHER_PREFIXED_NAMES_MAP
)
from .._constants import WarpingPatterns

__all__ = ['capitalize_from_string']


def _capitalize_from_map(
    lower_word: str,
    capitalization_map: dict[str, str]
) -> str | None:
    """
    Handle word capitalization through dictionary lookup, lowercasing
    any suffix.

    Args:
        lower_word: The lowercase word.
        capitalization_map: A dictionary with lowercase words as keys
            and their capitalized versions as values.

    Returns:
        str | None: The capitalized initialism, or ``None`` if
            ``lower_word`` is not in the map.
    """
    match = (WarpingPatterns.MAP_SUFFIX_EXCEPTIONS_PATTERN.search(lower_word))

    if match:
        start_of_split = match.start()
        base = lower_word[:start_of_split]
        suffix = lower_word[start_of_split:]

        capitalized_base = capitalization_map.get(base)

        if capitalized_base:
            # If the base is in the map, recombine it with the
            # lowercase suffix.
            return capitalized_base + suffix.lower()
        return None
    else:
        return capitalization_map.get(lower_word)


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
        str | None: The capitalized abbreviation, or ``None`` if
            ``lower_word`` is not in ``CAPITALIZED_ABBREVIATIONS_MAP``.
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
        str | None: The capitalized initialism, or ``None`` if
            ``lower_word`` is not in ``INITIALISMS_MAP``.
    """
    return _capitalize_from_map(lower_word, INITIALISMS_MAP)


def _handle_i_pronoun(_word: str, lower_word: str) -> str | None:
    """
    Handle the capitalization of the "I" pronoun.

    Args:
        _word: The word to capitalize (unused).
        lower_word: The lowercase word.

    Returns:
        str | None: The capitalized pronoun "I", or ``None`` if the
            input is not "i".
    """
    if lower_word == 'i':
        return 'I'
    return None


def _handle_lowercase_abbreviation(_word: str, lower_word: str) -> str | None:
    """
    Preserve the capitalization of a lowercase abbreviation.

    Args:
        _word: The word to capitalize (unused).
        lower_word: The lowercase word.

    Returns:
        str | None: The lowercase abbreviation, or ``None`` if
            ``lower_word`` is not in ``LOWERCASE_ABBREVIATIONS``.
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
        str | None: The mixed-case word, or ``None`` if ``lower_word``
            is not in ``MIXED_CASE_WORDS_MAP``.
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
        str | None: The capitalized initialism, or ``None`` if the
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
        str | None: The capitalized name, or ``None`` if the
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


def _preserve_existing_capitalization(
    word: str,
    _lower_word: str
) -> str | None:
    """
    Preserve the capitalization of a word that is already mixed-case.

    Args:
        word: The word to check.
        _lower_word: The lowercase word (unused).

    Returns:
        str | None : The original word, or ``None`` if the word is all
            lowercase or uppercase.
    """
    if not word.islower() and not word.isupper():
        return word
    return None


def capitalize_from_string(
    word: str,
    lowercase_by_default: bool = False
) -> str:
    """
    Capitalize a word, handling special name prefixes and preserving
    other mid-word capitalizations.

    Args:
        word: The word to capitalize.
        lowercase_by_default: Whether to lowercase the word if no
            capitalization strategy applies. Defaults to ``False``.

    Returns:
        str: The capitalized word.
    """
    if not word or not word[0].isalpha():
        return word

    lower_word = word.lower()

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
        word_result = strategy(word, lower_word)
        if word_result is not None:
            return word_result

    return word.capitalize() if not lowercase_by_default else lower_word
