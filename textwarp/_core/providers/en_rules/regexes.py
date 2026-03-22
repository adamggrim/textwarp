"""English-specific regular expressions."""

from functools import lru_cache

import regex as re

from textwarp._core.decorators import non_instantiable
from textwarp._core.constants.regexes import WarpingPatterns
from textwarp._core.providers.en_rules.data import (
    EnContractionExpansion,
    EnEntityCasing,
    EnPunctuation,
    EnStringCasing
)
from textwarp._core.enums import RegexBoundary

__all__ = ['EnWarpingPatterns']

@non_instantiable
class EnWarpingPatterns:
    """
    A namespace for compiled regular expressions used for English text
    warping.
    """

    @staticmethod
    @lru_cache(maxsize=1)
    def get_apostrophe_in_word() -> re.Pattern[str]:
        """
        Get a regular expression matching a straight apostrophe within a
        word or English elision.

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        elisions: str = '|'.join(EnPunctuation.get_elision_words())
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
                \d{{2}}s    # An abbreviation for a
            )               # decade.
            ''',
            re.VERBOSE | re.IGNORECASE
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_ambiguous_contraction() -> re.Pattern[str]:
        """
        Get a regular expression matching any contraction that can
        expand to multiple phrases.

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        return WarpingPatterns._create_words_regex(
            EnContractionExpansion.get_ambiguous_map()
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_cardinal() -> re.Pattern[str]:
        """
        Get a regular expression that matches a cardinal number.

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        return re.compile(rf'''
            ({WarpingPatterns._NUMBER_BASE_PATTERN})
            \b              # A word boundary.
            (?!             # Not followed by...
                \.\d        # A period and a digit.
                |           # OR
                \d          # A digit
                |           # OR
                /           # A forward slash
                |           # OR
                \s+         # One or more spaces.
                # Followed by a number...
                {WarpingPatterns._NUMBER_BASE_PATTERN}
                /           # Followed by a forward slash.
            )
        ''', re.VERBOSE)

    @staticmethod
    @lru_cache(maxsize=1)
    def get_contraction() -> re.Pattern[str]:
        """
        Get a regular expression matching any expandable contraction.

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        return WarpingPatterns._create_words_regex(
            list(EnContractionExpansion.get_unambiguous_map().keys())
            + list(EnContractionExpansion.get_ambiguous_map())
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_contraction_suffixes_pattern() -> re.Pattern[str]:
        """
        Get a regular expression matching any contraction suffix (e.g.,
        "'s", "'ll", etc.).

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        return WarpingPatterns._create_words_regex(
            EnEntityCasing.get_contraction_suffixes()
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_common_stateless_participles() -> re.Pattern[str]:
        """
        Get a regular expression matching common stateless participles
        (e.g., "doin", "makin", etc.).

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        return WarpingPatterns._create_words_regex(
            EnContractionExpansion.get_common_stateless_participles()
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_idiomatic_phrases() -> re.Pattern[str]:
        """
        Get a regular expression matching idiomatic phrases with their
        corresponding expansion.

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        return WarpingPatterns._create_words_regex(
            EnContractionExpansion.get_idiomatic_map().keys()
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_map_suffix_exceptions_pattern() -> re.Pattern[str]:
        """
        Get a regular expression matching suffix exceptions.

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        return WarpingPatterns._create_words_regex(
            EnStringCasing.get_map_suffix_exceptions(),
            boundary=RegexBoundary.END_ANCHOR
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_name_prefix_exception_pattern() -> re.Pattern[str]:
        """
        Get a regular expression matching prefix exceptions.

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        return WarpingPatterns._create_words_regex(
            EnStringCasing.get_surname_prefix_exceptions(),
            boundary=RegexBoundary.START_ANCHOR
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_n_t_suffix() -> re.Pattern[str]:
        """
        Get a regular expression matching negative contraction suffixes.

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        return re.compile(r"n['’‘]t$", re.IGNORECASE)

    @staticmethod
    @lru_cache(maxsize=1)
    def get_ordinal() -> re.Pattern[str]:
        """
        Get a regular expression matching an ordinal number.

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        return re.compile(rf'''
            ({WarpingPatterns._NUMBER_BASE_PATTERN})
            (?:st|nd|rd|th)s?
            \b
        ''', re.VERBOSE)

    @staticmethod
    @lru_cache(maxsize=1)
    def get_surname_prefix_pattern() -> re.Pattern[str]:
        """
        Get a regular expression matching any surname prefix.

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        return WarpingPatterns._create_words_regex(
            EnStringCasing.get_surname_prefixes(),
            boundary=RegexBoundary.START_ANCHOR
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_whatcha_are_words() -> re.Pattern[str]:
        """
        Get a regular expression matching words where "whatcha" expands
        to "what are you".

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        return WarpingPatterns._create_words_regex(
            EnContractionExpansion.get_whatcha_are_words()
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_whatcha_have_words() -> re.Pattern[str]:
        """
        Get a regular expression matching words where "whatcha" expands
        to "what have you".

        Returns:
            re.Pattern[str]: A compiled regular expression pattern.
        """
        return WarpingPatterns._create_words_regex(
            EnContractionExpansion.get_whatcha_have_words()
        )
