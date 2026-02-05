"""Regular expressions used across the package."""

import regex as re
from typing import Final, final

from textwarp._core.config import (
    ContractionExpansion,
    EntityCasing,
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

    Attributes:
        ANY_SEPARATOR: Matches any separator used in dot, kebab or
            snake case (i.e., ``.``, ``-`` or ``_``).
        SPLIT_CAMEL_OR_PASCAL: Splits camel or Pascal case strings
            into constituent words, correctly handling initialisms
            (e.g., ``URLSuffix -> ['URL', 'Suffix']``).
        SPLIT_FOR_PASCAL_CONVERSION: Removes select characters
            (i.e., a single space, ``.``, ``-``, ``_`` or a word
            boundary) before conversion to Pascal case.
        SPLIT_FOR_SEPARATOR_CONVERSION: Splits strings on non-
            separator word boundaries before converting to dot,
            kebab or snake case.
    """
    ANY_SEPARATOR: Final[re.Pattern[str]] = re.compile(r'[.\-_]')
    SPLIT_CAMEL_OR_PASCAL: Final[re.Pattern[str]] = re.compile(r'''
        # PART 1: POSITION BETWEEN AN UPPERCASE AND LOWERCASE LETTER
        (?<=            # Preceded by...
            [a-z]       # A lowercase letter.
        )
        (?=             # Followed by...
            [A-Z]       # An uppercase letter.
        )
        |               # OR
        # PART 2: POSITION AFTER AN ACRYONYM
        (?<=            # Preceded by...
            [A-Z]       # An uppercase letter.
        )
        (?=             # Followed by...
            [A-Z][a-z]  # An uppercase letter followed by a lowercase
                        # letter.
        )
        |               # OR
        # PART 3: POSITION BETWEEN A LETTER AND A DIGIT
        (?<=            # Preceded by...
            [A-Za-z]    # A letter.
        )
        (?=             # Followed by...
            [0-9]       # A digit.
        )
        |               # OR
        # PART 4: POSITION BETWEEN A DIGIT AND A LETTER
        (?<=            # Preceded by...
            [0-9]       # A digit.
        )
        (?=             # Followed by...
            [A-Za-z]    # A letter.
        )
        ''', re.VERBOSE
    )
    SPLIT_FOR_PASCAL_CONVERSION: Final[re.Pattern[str]] = re.compile(rf'''
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
            [a-zA-Z][a-zA-Z0-9]*        # A letter followed by zero or
                                        # more letters or digits.
        )
        [.\-]                           # A hyphen or period.
        (?=                             # Followed by...
            [A-Za-z0-9]                 # A letter or digit.
        )
        |                               # OR
        # PART 3: SNAKE CASE SEPARATOR
        _                               # An underscore.
        |                               # OR
        # PART 4: WORD BOUNDARY
        \b                              # A word boundary.
        ''', re.VERBOSE
    )
    SPLIT_FOR_SEPARATOR_CONVERSION: Final[re.Pattern[str]] = re.compile(r'''
        # WORD BOUNDARY NOT PRECEDED OR FOLLOWED BY A PERIOD OR HYPHEN
        (?<!        # Not preceded by...
            [.\-]   # A period or hyphen.
        )
        \b          # A word boundary.
        (?!         # Not followed by...
            [.\-]   # A period or hyphen.
        )
        ''', re.VERBOSE
    )


@final
@non_instantiable
class CasePatterns:
    """
    A namespace for compiled regular expressions that identify cases.

    Attributes:
        CAMEL_WORD: Matches a camel case word (e.g., ``camelWord``).
        DOT_WORD: Matches a dot case word (e.g., ``dot.word``).
        KEBAB_WORD: Matches a kebab case word (e.g.,
            ``kebab-word``).
        LOWER_WORD: Matches a lowercase word (e.g., ``lowercase``) and
            any optional separators (i.e., ``.``, ``-`` or ``_``).
        PASCAL_WORD: Matches a Pascal case word (e.g.,
            ``PascalWord``).
        SNAKE_WORD: Matches a snake case word (e.g.,
            ``snake_word``).
        UPPER_WORD: Matches an uppercase word (e.g., ``UPPERCASE``) and
            any optional separators (i.e., ``.``, ``-`` or ``_``).
    """
    CAMEL_WORD: Final[re.Pattern[str]] = re.compile(
        r'\b[a-z][a-z0-9]*[A-Z][A-Za-z0-9]*\b'
    )
    DOT_WORD: Final[re.Pattern[str]] = re.compile(
        r'\b[a-zA-Z][a-zA-Z0-9]*(?:\.[a-zA-Z0-9]+)+\b'
    )
    KEBAB_WORD: Final[re.Pattern[str]] = re.compile(
        r'\b[a-zA-Z][a-zA-Z0-9]*(?:\-[a-zA-Z0-9]+)+\b'
    )
    LOWER_WORD: Final[re.Pattern[str]] = re.compile(r'''
        \b                      # A word boundary.
        (?=                     # Followed by...
            [0-9.\-_]*          # Zero or more digits or separators.
            [a-z]               # And a lowercase letter.
        )
        [a-z0-9.\-_]+           # One or more lowercase letters, digits
                                # or separators.
        \b                      # Followed by a word boundary.
        ''', re.VERBOSE
    )
    PASCAL_WORD: Final[re.Pattern[str]] = re.compile(
        r'\b[A-Z][A-Z0-9]*[a-z][A-Za-z0-9]*\b'
    )
    SNAKE_WORD: Final[re.Pattern[str]] = re.compile(
        r'\b_?[a-zA-Z][a-zA-Z0-9]*(?:_[a-zA-Z0-9]+)+\b'
    )
    UPPER_WORD: Final[re.Pattern[str]] = re.compile(r'''
        \b                      # A word boundary.
        (?=                     # Followed by...
            [0-9.\-_]*          # Zero or more digits or separators.
            [A-Z]               # And an uppercase letter.
        )
        [A-Z0-9.\-_]+           # One or more uppercase letters, digits or
                                # separators.
        \b                      # Followed by a word boundary.
        ''', re.VERBOSE
    )


@final
@non_instantiable
class WarpingPatterns:
    """
    A namespace for compiled regular expressions used for warping text.

    Attributes:
        ANY_APOSTROPHE: Matches any straight (``'``) or curly (``’`` or
            ``‘``) apostrophe.
        APOSTROPHE_IN_WORD: Matches a straight apostrophe within a word
            (e.g., "it's", "'twas").
        AMBIGUOUS_CONTRACTION: Matches any contraction that can expand
            to multiple phrases (e.g., "it's" -> "it is" or "it has").
        CARDINAL: Matches a cardinal number (e.g., "525,600" or "13").
        CONTRACTION: Matches any expandable contraction (e.g., "don't").
        CONTRACTION_SUFFIXES_PATTERN: Matches any contraction suffix
            (e.g., "'s", "'ll").
        DASH: Matches an en (``–``) or em (``—``) dash.
        EM_DASH_STAND_IN: Matches characters that function as an em
            dash (e.g., ``--``).
        MULTIPLE_SPACES: Matches two or more consecutive spaces.
        SURNAME_PREFIX_PATTERN: Matches any surname prefix (e.g., "Mac",
            "O'").
        OPENING_STRAIGHT_QUOTES: Matches opening straight quotes.
        ORDINAL: Matches an ordinal number (e.g., "19th").
        PERIOD_SEPARATED_INITIALISM: Matches a period-separated
            initialism (e.g., ``U.S.A.``).
        PUNCT_INSIDE: Matches punctuation inside quotes (e.g., ``."``).
        PUNCT_OUTSIDE: Matches punctuation outside quotes (e.g.,
            ``".``).
        WORD_CHARACTER: Matches any word character.
    """
    @staticmethod
    def _create_words_regex(
        words: str | list[str],
        boundary: RegexBoundary = RegexBoundary.WORD_BOUNDARY
    ) -> re.Pattern[str]:
        """
        Create a compiled regular expression object that matches any
        word in the given list.

        Args:
            words: A word or list of words.
            boundary: The boundary-matching strategy to use. Defaults to
                ``RegexBoundary.WORD_BOUNDARY``.

        Returns:
            A compiled regular expression object.
        """
        def _add_escaped_apostrophes(word: str) -> str:
            """
            Add escaped apostrophes to a word.

            Args:
                word: The word to process.
            """
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
            case RegexBoundary.END_ANCHOR:
                final_pattern = rf'(?:{pattern_string})$'

        return re.compile(final_pattern, re.IGNORECASE)

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
    elisions: Final[str] = '|'.join(ContractionExpansion.get_elision_words())

    ANY_APOSTROPHE: Final[re.Pattern[str]] = re.compile(r"['’‘]")
    APOSTROPHE_IN_WORD: Final[re.Pattern[str]] = re.compile(rf'''
        # PART 1: APOSTROPHE SURROUNDED BY LETTERS
        (?<=            # Preceded by...
            [a-z]       # An alphabetical letter.
        )
        ['’‘]           # An apostrophe.
        (?=             # Followed by...
            [a-z]       # An alphabetical letter.
        )
        |               # OR
        # PART 2: APOSTROPHE IN ELISION OR DECADE ABBREVIATION
        ['’‘]           # An apostrophe.
        (?=             # Followed by...
            {elisions}  # An elision.
            |           # OR
            \d{{2}}s    # An abbreviation for a
        )               # decade.
        ''', re.VERBOSE | re.IGNORECASE
    )
    AMBIGUOUS_CONTRACTION: Final[re.Pattern[str]] = (
        _create_words_regex(ContractionExpansion.get_ambiguous_map())
    )
    CARDINAL: Final[re.Pattern[str]] = re.compile(rf'''
        {_NUMBER_BASE_PATTERN}  # A number with or without thousands
                                # separators.
        \b                      # Followed by a word boundary.
        (?!                     # Not followed by...
            \.                  # A period.
            \d                  # Followed by a digit.
        )
        ''', re.VERBOSE
    )
    CONTRACTION: Final[re.Pattern[str]] = _create_words_regex(
        list(ContractionExpansion.get_unambiguous_map().keys())
        + ContractionExpansion.get_ambiguous_map()
    )
    CONTRACTION_SUFFIXES_PATTERN: Final[re.Pattern[str]] = (
        _create_words_regex(EntityCasing.get_contraction_suffixes())
    )
    DASH: Final[re.Pattern[str]] = re.compile(r'[–—]')
    EM_DASH_STAND_IN: Final[re.Pattern[str]] = re.compile(r'\s?--?\s?')
    MAP_SUFFIX_EXCEPTIONS_PATTERN: Final[re.Pattern[str]] = (
        _create_words_regex(
            StringCasing.get_map_suffix_exceptions(),
            boundary=RegexBoundary.END_ANCHOR
        )
    )
    MULTIPLE_SPACES: Final[re.Pattern[str]] = re.compile(r'(?<=\S) {2,}')
    NAME_PREFIX_EXCEPTION_PATTERN: Final[re.Pattern[str]] = (
        _create_words_regex(StringCasing.get_surname_prefix_exceptions())
    )
    N_T_SUFFIX: Final[re.Pattern[str]]  = re.compile(
        r"n['’‘]t$", re.IGNORECASE
    )
    OPENING_STRAIGHT_QUOTES: Final[re.Pattern[str]] = re.compile(r'''
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
        ''', re.VERBOSE
    )
    ORDINAL: Final[re.Pattern[str]] = re.compile(rf'''
        ({_NUMBER_BASE_PATTERN})    # GROUP 1 (NUMBER WITH OR WITHOUT
                                    # SEPARATORS)
        (?:st|nd|rd|th)             # Followed by an ordinal suffix.
        \b                          # Followed by a word boundary.
        ''', re.VERBOSE
    )
    PERIOD_SEPARATED_INITIALISM: Final[re.Pattern[str]] = re.compile(
        r'\b(?:[A-Za-z]\.){2,}'
    )
    PUNCT_INSIDE: Final[re.Pattern[str]] = re.compile(
        r'([.,])(["”\'’]?["”\'’])'
    )
    PUNCT_OUTSIDE: Final[re.Pattern[str]] = re.compile(
        r'(["”\'’]?["”\'’])([.,])'
    )
    SURNAME_PREFIX_PATTERN: Final[re.Pattern[str]] = _create_words_regex(
        StringCasing.get_surname_prefixes()
    )
    WHATCHA_ARE_WORDS: Final[list[str]] = _create_words_regex(
        ContractionExpansion.get_whatcha_are_words()
    )
    WHATCHA_HAVE_WORDS: Final[list[str]] = _create_words_regex(
        ContractionExpansion.get_whatcha_have_words()
    )
    WORD_CHARACTER: Final[re.Pattern[str]] = re.compile(r'\w')
