"""English-specific regular expression patterns for text warping."""

from functools import lru_cache
from typing import Final

import regex as re

from textwarp._core.constants import patterns
from textwarp._core.providers import en
from textwarp._core.enums import RegexBoundary

__all__ = [
    'get_any_apostrophe',
    'get_apostrophe_in_word',
    'get_ambiguous_contraction',
    'get_cardinal',
    'get_contraction',
    'get_contraction_suffixes_pattern',
    'get_common_stateless_participles',
    'get_idiomatic_phrases',
    'get_map_suffix_exceptions_pattern',
    'get_name_prefix_exception_pattern',
    'get_n_t_suffix',
    'get_opening_straight_quotes',
    'get_ordinal',
    'get_punct_inside',
    'get_punct_outside',
    'get_surname_prefix_pattern',
    'get_whatcha_are_words',
    'get_whatcha_have_words'
]

_NUMBER_BASE_PATTERN: Final[str] = r'''
    (?<!            # Not preceded by...
        \d          # A digit.
        \.          # Followed by a period.
    )
    \b              # A word boundary.
    (?:             # A non-capturing group for...
        # A NUMBER WITH THOUSANDS SEPARATORS
        \d{1,3}     # One to three digits.
        (?:         # A non-capturing group for...
            ,\d{3}  # A comma followed by exactly three digits.
        )+          # One or more times.
        |           # OR
        # A NUMBER WITHOUT THOUSANDS SEPARATORS
        \d+         # One or more digits.
    )
'''


@lru_cache(maxsize=1)
def get_apostrophe_in_word() -> re.Pattern[str]:
    """
    Get a regular expression matching a straight apostrophe within a
    word or English elision.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    elisions: str = '|'.join(en.data.punctuation.get_elision_words())
    return re.compile(
        rf'''
        # PART 1: APOSTROPHE SURROUNDED BY LETTERS
        (?<=            # Preceded by...
            \p{{L}}     # An alphabetical letter.
        )
        ['’‘]           # An apostrophe.
        (?=             # Followed by...
            \p{{L}}     # An alphabetical letter.
        )
        |               # OR
        # PART 2: APOSTROPHE IN ELISION OR DECADE ABBREVIATION
        ['’‘]           # An apostrophe.
        (?=             # Followed by...
            {elisions}  # An elision.
            |           # OR
            \d{{2}}s    # An abbreviation for a decade.
        )
        ''',
        re.VERBOSE | re.IGNORECASE
    )


@lru_cache(maxsize=1)
def get_ambiguous_contraction() -> re.Pattern[str]:
    """
    Get a regular expression matching any contraction that can
    expand to multiple phrases.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return patterns.warping.create_words_regex(
        en.data.contraction_expansion.get_ambiguous_map()
    )


@lru_cache(maxsize=1)
def get_any_apostrophe() -> re.Pattern[str]:
    """
    Get a regular expression matching any straight or curly apostrophe.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r"['’‘]")


@lru_cache(maxsize=1)
def get_cardinal() -> re.Pattern[str]:
    """
    Get a regular expression that matches a cardinal number.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(rf'''
        ({_NUMBER_BASE_PATTERN})
        \b                          # A word boundary.
        (?!                         # Not followed by...
            \.\d                    # A period and a digit.
            |                       # OR
            \d                      # A digit
            |                       # OR
            /                       # A forward slash
            |                       # OR
            \s+                     # One or more spaces.
            {_NUMBER_BASE_PATTERN}  # Followed by a number...
            /                       # Followed by a forward slash.
        )
    ''', re.VERBOSE)


@lru_cache(maxsize=1)
def get_contraction() -> re.Pattern[str]:
    """
    Get a regular expression matching any expandable contraction.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return patterns.warping.create_words_regex(
        list(en.data.contraction_expansion.get_unambiguous_map().keys())
        + list(en.data.contraction_expansion.get_ambiguous_map())
    )


@lru_cache(maxsize=1)
def get_contraction_suffixes_pattern() -> re.Pattern[str]:
    """
    Get a regular expression matching any contraction suffix (e.g.,
    "'s", "'ll", etc.).

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return patterns.warping.create_words_regex(
        en.data.entity_casing.get_contraction_suffixes()
    )


@lru_cache(maxsize=1)
def get_common_stateless_participles() -> re.Pattern[str]:
    """
    Get a regular expression matching common stateless participles
    (e.g., "doin", "makin", etc.).

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return patterns.warping.create_words_regex(
        en.data.contraction_expansion.get_common_stateless_participles()
    )


@lru_cache(maxsize=1)
def get_idiomatic_phrases() -> re.Pattern[str]:
    """
    Get a regular expression matching idiomatic phrases with their
    corresponding expansion.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return patterns.warping.create_words_regex(
        en.data.contraction_expansion.get_idiomatic_map().keys()
    )


@lru_cache(maxsize=1)
def get_map_suffix_exceptions_pattern() -> re.Pattern[str]:
    """
    Get a regular expression matching suffix exceptions.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return patterns.warping.create_words_regex(
        en.data.string_casing.get_map_suffix_exceptions(),
        boundary=RegexBoundary.END_ANCHOR
    )


@lru_cache(maxsize=1)
def get_name_prefix_exception_pattern() -> re.Pattern[str]:
    """
    Get a regular expression matching prefix exceptions.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return patterns.warping.create_words_regex(
        en.data.string_casing.get_surname_prefix_exceptions(),
        boundary=RegexBoundary.START_ANCHOR
    )


@lru_cache(maxsize=1)
def get_n_t_suffix() -> re.Pattern[str]:
    """
    Get a regular expression matching negative contraction suffixes.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r"n['’‘]t$", re.IGNORECASE)


@lru_cache(maxsize=1)
def get_opening_straight_quotes() -> re.Pattern[str]:
    """
    Get a regular expression matching opening straight quotes.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'''
        # PART 1: SINGLE QUOTES
        (?:                 # OPENING CONTEXT (SINGLE QUOTES)
            ^               # The start of a string.
            |               # OR
            (?<=            # Preceded by...
                [\s([{"“]   # A whitespace character, opening
                            # parenthesis, opening square bracket,
                            # opening curly brace or straight or
                            # opening double quote.
                |           # OR
                ["“]\s      # Preceded by a straight or opening double
                            # quote followed by a space.
            )
        )
        (                   # GROUP 1 (SINGLE QUOTES)
        '+                  # One or more straight single quotes.
        )
        |                   # OR
        # PART 2: DOUBLE QUOTES
        (?:                 # OPENING CONTEXT (DOUBLE QUOTES)
            ^               # The start of a string.
            |               # OR
            (?<=            # Preceded by...
                [\s([{]     # A whitespace character,
                            # opening parenthesis, opening square
                            # bracket or opening curly brace.
            )
        )
        (                   # GROUP 2 (DOUBLE QUOTES)
            (?<!            # Not preceded by...
                ['’]\s      # A straight or closing single quote
                            # followed by a space.
            )
        "+                  # One or more straight double quotes.
        )
    ''', re.VERBOSE)


@lru_cache(maxsize=1)
def get_ordinal() -> re.Pattern[str]:
    """
    Get a regular expression matching an ordinal number.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(rf'''
        ({_NUMBER_BASE_PATTERN})
        (?:st|nd|rd|th)s?
        \b
    ''', re.VERBOSE)


@lru_cache(maxsize=1)
def get_punct_inside() -> re.Pattern[str]:
    """
    Get a regular expression matching punctuation inside quotation
    marks.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'([.,])(["”\'’]?["”\'’])')


@lru_cache(maxsize=1)
def get_punct_outside() -> re.Pattern[str]:
    """
    Get a regular expression matching punctuation outside quotation
    marks.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'(["”\'’]?["”\'’])([.,])')


@lru_cache(maxsize=1)
def get_surname_prefix_pattern() -> re.Pattern[str]:
    """
    Get a regular expression matching any surname prefix.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return patterns.warping.create_words_regex(
        en.data.string_casing.get_surname_prefixes(),
        boundary=RegexBoundary.START_ANCHOR
    )


@lru_cache(maxsize=1)
def get_whatcha_are_words() -> re.Pattern[str]:
    """
    Get a regular expression matching words where "whatcha" expands to
    "what are you".

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return patterns.warping.create_words_regex(
        en.data.contraction_expansion.get_whatcha_are_words()
    )


@lru_cache(maxsize=1)
def get_whatcha_have_words() -> re.Pattern[str]:
    """
    Get a regular expression matching words where "whatcha" expands to
    "what have you".

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return patterns.warping.create_words_regex(
        en.data.contraction_expansion.get_whatcha_have_words()
    )
