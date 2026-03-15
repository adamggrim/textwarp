"""Regular expressions used across the package."""

from functools import lru_cache
from typing import Final, Iterable, final

import regex as re

from textwarp._core.config import (
    ContractionExpansion,
    EntityCasing,
    Punctuation,
    StringCasing
)
from textwarp._core.decorators import non_instantiable
from textwarp._core.enums import RegexBoundary

__all__ = [
    'CaseConversionPatterns',
    'CasePatterns',
    'WarpingPatterns'
]


@final
@non_instantiable
class CaseConversionPatterns:
    """
    A namespace for compiled regular expressions that convert between
    cases.
    """

    @staticmethod
    @lru_cache(maxsize=1)
    def get_any_separator() -> re.Pattern[str]:
        """Matches any separator used in dot, kebab or snake case."""
        return re.compile(r'[.\-_]')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_split_camel_or_pascal() -> re.Pattern[str]:
        """Splits camel or Pascal case strings into constituent words."""
        return re.compile(r'''
        # PART 1: POSITION BETWEEN AN UPPERCASE AND LOWERCASE LETTER
        (?<=            # Preceded by...
            \p{Ll}      # A lowercase letter.
        )
        (?=             # Followed by...
            \p{Lu}      # An uppercase letter.
        )
        |               # OR
        # PART 2: POSITION AFTER AN ACRYONYM
        (?<=            # Preceded by...
            \p{Lu}      # An uppercase letter.
        )
        (?=             # Followed by...
            \p{Lu}\p{Ll} # An uppercase letter followed by a lowercase
                        # letter.
        )
        |               # OR
        # PART 3: POSITION BETWEEN A LETTER AND A DIGIT
        (?<=            # Preceded by...
            \p{L}       # A letter.
        )
        (?=             # Followed by...
            \d          # A digit.
        )
        |               # OR
        # PART 4: POSITION BETWEEN A DIGIT AND A LETTER
        (?<=            # Preceded by...
            \d          # A digit.
        )
        (?=             # Followed by...
            \p{L}       # A letter.
        )
        ''', re.VERBOSE)

    @staticmethod
    @lru_cache(maxsize=1)
    def get_split_for_pascal_conversion() -> re.Pattern[str]:
        """Removes select characters before conversion to Pascal case."""
        return re.compile(rf'''
        # PART 1: SPACE NOT PRECEDED OR FOLLOWED BY A SPACE OR
        # PUNCTUATION
        (?<!                            # Not preceded by...
            [\s.!?—–\-,:;"”“\'’‘)\]}}]  # A space character or select
                                        # closing punctuation.
        )
        [ ]                             # A single space.
        (?!                             # Not followed by...
            [\s—–\-"“”\'‘‘(\[{{]        # A space character or select
                                        # opening punctuation.
        )
        |                               # OR
        # PART 2: DOT OR KEBAB CASE SEPARATOR
        (?<=                            # Preceded by...
            \p{{L}}[\p{{L}}\d]* # A letter followed by zero or
                                        # more letters or digits.
        )
        [.\-]                           # A hyphen or period.
        (?=                             # Followed by...
            [\p{{L}}\d]                 # A letter or digit.
        )
        |                               # OR
        # PART 3: SNAKE CASE SEPARATOR
        _                               # An underscore.
        |                               # OR
        # PART 4: WORD BOUNDARY
        \b                              # A word boundary.
        ''', re.VERBOSE)

    @staticmethod
    @lru_cache(maxsize=1)
    def get_split_for_separator_conversion() -> re.Pattern[str]:
        """Splits strings on non-separator word boundaries."""
        return re.compile(r'''
        # WORD BOUNDARY NOT PRECEDED OR FOLLOWED BY A PERIOD OR HYPHEN
        (?<!        # Not preceded by...
            [.\-]   # A period or hyphen.
        )
        \b          # A word boundary.
        (?!         # Not followed by...
            [.\-]   # A period or hyphen.
        )
        ''', re.VERBOSE)


@final
@non_instantiable
class CasePatterns:
    """
    A namespace for compiled regular expressions that identify cases.
    """

    @staticmethod
    @lru_cache(maxsize=1)
    def get_camel_word() -> re.Pattern[str]:
        """Matches a camel case word (e.g., ``camelWord``)."""
        return re.compile(r'\b\p{Ll}[\p{Ll}\d]*\p{Lu}[\p{L}\d]*\b')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_dot_word() -> re.Pattern[str]:
        """Matches a dot case word (e.g., ``dot.word``)."""
        return re.compile(r'\b\p{L}[\p{L}\d]*(?:\.[\p{L}\d]+)+\b')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_kebab_word() -> re.Pattern[str]:
        """Matches a kebab case word (e.g., ``kebab-word``)."""
        return re.compile(r'\b\p{L}[\p{L}\d]*(?:\-[\p{L}\d]+)+\b')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_lower_word() -> re.Pattern[str]:
        """Matches a lowercase word and any optional separators."""
        return re.compile(r'''
        \b                      # A word boundary.
        (?=                     # Followed by...
            [\d.\-_]* # Zero or more digits or separators.
            \p{Ll}              # And a lowercase letter.
        )
        [\p{Ll}\d.\-_]+         # One or more lowercase letters, digits
                                # or separators.
        \b                      # Followed by a word boundary.
        ''', re.VERBOSE)

    @staticmethod
    @lru_cache(maxsize=1)
    def get_pascal_word() -> re.Pattern[str]:
        """Matches a Pascal case word (e.g., ``PascalWord``)."""
        return re.compile(r'\b\p{Lu}[\p{Lu}\d]*\p{Ll}[\p{L}\d]*\b')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_snake_word() -> re.Pattern[str]:
        """Matches a snake case word (e.g., ``snake_word``)."""
        return re.compile(r'\b_?\p{L}[\p{L}\d]*(?:_[\p{L}\d]+)+\b')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_upper_word() -> re.Pattern[str]:
        """Matches an uppercase word and any optional separators."""
        return re.compile(r'''
        \b                      # A word boundary.
        (?=                     # Followed by...
            [\d.\-_]* # Zero or more digits or separators.
            \p{Lu}              # And an uppercase letter.
        )
        [\p{Lu}\d.\-_]+         # One or more uppercase letters, digits or
                                # separators.
        \b                      # Followed by a word boundary.
        ''', re.VERBOSE)


@final
@non_instantiable
class WarpingPatterns:
    """
    A namespace for compiled regular expressions used for warping text.
    """
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

    @staticmethod
    def _create_words_regex(
        words: str | Iterable[str],
        boundary: RegexBoundary = RegexBoundary.WORD_BOUNDARY
    ) -> re.Pattern[str]:
        """
        Create a compiled regular expression object that matches any
        word in the given list.
        """
        def _add_escaped_apostrophes(word: str) -> str:
            """Add escaped apostrophes to a word."""
            return re.escape(word).replace("'", "['’‘]")

        if isinstance(words, str):
            pattern_string = _add_escaped_apostrophes(words)
        else:
            # Sort words by length in descending order, so that longer
            # words containing other words from the set are matched
            # first (e.g., "can't've" before "can't").
            sorted_words: list[str] = sorted(
                words,
                key=len,
                reverse=True
            )
            escaped_patterns: list[str] = [
                _add_escaped_apostrophes(w) for w in sorted_words
            ]
            pattern_string = '|'.join(escaped_patterns)

        match boundary:
            case RegexBoundary.WORD_BOUNDARY:
                final_pattern = rf'(?<!\w)(?:{pattern_string})(?!\w)'
            case RegexBoundary.START_ANCHOR:
                final_pattern = rf'(?<!\w)(?:{pattern_string})'
            case RegexBoundary.END_ANCHOR:
                final_pattern = rf'(?:{pattern_string})$'

        return re.compile(final_pattern, re.IGNORECASE)

    @staticmethod
    @lru_cache(maxsize=1)
    def get_any_apostrophe() -> re.Pattern[str]:
        """Matches any straight or curly apostrophe."""
        return re.compile(r"['’‘]")

    @staticmethod
    @lru_cache(maxsize=1)
    def get_apostrophe_in_word() -> re.Pattern[str]:
        """Matches a straight apostrophe within a word."""
        elisions: str = '|'.join(Punctuation.get_elision_words())
        return re.compile(rf'''
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
        ''', re.VERBOSE | re.IGNORECASE)

    @staticmethod
    @lru_cache(maxsize=1)
    def get_ambiguous_contraction() -> re.Pattern[str]:
        """Matches any contraction that can expand to multiple phrases."""
        return WarpingPatterns._create_words_regex(
            ContractionExpansion.get_ambiguous_map()
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_cardinal() -> re.Pattern[str]:
        """Matches a cardinal number."""
        return re.compile(rf'''
        {WarpingPatterns._NUMBER_BASE_PATTERN}  # A number with or without thousands
                                                # separators.
        \b                                      # Followed by a word boundary.
        (?!                                     # Not followed by...
            \.                                  # A period.
            \d                                  # Followed by a digit.
        )
        ''', re.VERBOSE)

    @staticmethod
    @lru_cache(maxsize=1)
    def get_contraction() -> re.Pattern[str]:
        """Matches any expandable contraction."""
        return WarpingPatterns._create_words_regex(
            list(ContractionExpansion.get_unambiguous_map().keys())
            + list(ContractionExpansion.get_ambiguous_map())
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_contraction_suffixes_pattern() -> re.Pattern[str]:
        """Matches any contraction suffix (e.g., "'s", "'ll")."""
        return WarpingPatterns._create_words_regex(
            EntityCasing.get_contraction_suffixes()
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_common_stateless_participles() -> re.Pattern[str]:
        """Matches common participles like "doin" or "makin"."""
        return WarpingPatterns._create_words_regex(
            ContractionExpansion.get_common_stateless_participles()
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_dash() -> re.Pattern[str]:
        """Matches an en (–) or em (—) dash."""
        return re.compile(r'[–—]')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_em_dash_stand_in() -> re.Pattern[str]:
        """Matches characters that function as an em dash (e.g., --)."""
        return re.compile(r'\s?--?\s?')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_idiomatic_phrases() -> re.Pattern[str]:
        """Matches any idiomatic phrase with a corresponding expansion."""
        return WarpingPatterns._create_words_regex(
            ContractionExpansion.get_idiomatic_map().keys()
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_map_suffix_exceptions_pattern() -> re.Pattern[str]:
        """Matches exception suffixes tied to the end of words."""
        return WarpingPatterns._create_words_regex(
            StringCasing.get_map_suffix_exceptions(),
            boundary=RegexBoundary.END_ANCHOR
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_multiple_spaces() -> re.Pattern[str]:
        """Matches two or more consecutive spaces."""
        return re.compile(r'(?<=\S) {2,}')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_name_prefix_exception_pattern() -> re.Pattern[str]:
        """Matches strings acting as prefix exceptions."""
        return WarpingPatterns._create_words_regex(
            StringCasing.get_surname_prefix_exceptions(),
            boundary=RegexBoundary.START_ANCHOR
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_n_t_suffix() -> re.Pattern[str]:
        """Matches negative contraction suffixes."""
        return re.compile(r"n['’‘]t$", re.IGNORECASE)

    @staticmethod
    @lru_cache(maxsize=1)
    def get_opening_straight_quotes() -> re.Pattern[str]:
        """Matches opening straight quotes."""
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

    @staticmethod
    @lru_cache(maxsize=1)
    def get_ordinal() -> re.Pattern[str]:
        """Matches an ordinal number."""
        return re.compile(rf'''
        ({WarpingPatterns._NUMBER_BASE_PATTERN})    # GROUP 1 (NUMBER WITH OR WITHOUT
                                                    # SEPARATORS)
        (?:st|nd|rd|th)                             # Followed by an ordinal suffix.
        \b                                          # Followed by a word boundary.
        ''', re.VERBOSE)

    @staticmethod
    @lru_cache(maxsize=1)
    def get_period_separated_initialism() -> re.Pattern[str]:
        """Matches a period-separated initialism (e.g., U.S.A.)."""
        return re.compile(r'\b(?:\p{L}\.){2,}')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_punct_inside() -> re.Pattern[str]:
        """Matches punctuation inside quotes (e.g., .")."""
        return re.compile(r'([.,])(["”\'’]?["”\'’])')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_punct_outside() -> re.Pattern[str]:
        """Matches punctuation outside quotes (e.g., ".)."""
        return re.compile(r'(["”\'’]?["”\'’])([.,])')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_surname_prefix_pattern() -> re.Pattern[str]:
        """Matches any surname prefix."""
        return WarpingPatterns._create_words_regex(
            StringCasing.get_surname_prefixes(),
            boundary=RegexBoundary.START_ANCHOR
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_whatcha_are_words() -> re.Pattern[str]:
        """Matches words that expand 'whatcha' to 'what are you'."""
        return WarpingPatterns._create_words_regex(
            ContractionExpansion.get_whatcha_are_words()
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_whatcha_have_words() -> re.Pattern[str]:
        """Matches words that expand 'whatcha' to 'what have you'."""
        return WarpingPatterns._create_words_regex(
            ContractionExpansion.get_whatcha_have_words()
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_word_character() -> re.Pattern[str]:
        """Matches any word character."""
        return re.compile(r'\w')