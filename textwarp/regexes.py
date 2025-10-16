import regex as re
from typing import Final, final

from .config import (
    AMBIGUOUS_CONTRACTIONS,
    CONTRACTIONS_MAP,
    CONTRACTION_SUFFIX_TOKENS,
    ELISION_WORDS,
    NAME_PREFIX_EXCEPTIONS,
    NAME_PREFIXES,
    MAP_SUFFIX_EXCEPTIONS,
    OTHER_PREFIXED_NAMES_MAP
)
from .decorators import non_instantiable
from .enums import RegexBoundary


@final
@non_instantiable
class ProgrammingCasePatterns:
    """
    A namespace for compiled regular expressions identifying and
    converting between programming cases.

    Attributes:
        Case-Matching Patterns:
            CAMEL_WORD: Compiled regular expression object that matches
                a camel case word.
            DOT_WORD: Compiled regular expression object that matches a
                dot case word.
            KEBAB_WORD: Compiled regular expression object that matches
                a kebab case word.
            PASCAL_WORD: Compiled regular expression object that
                matches a Pascal case word.
            SNAKE_WORD: Compiled regular expression object that matches
                a snake case word.

        Splitting Patterns:
            ANY_SEPARATOR: Compiled regular expression object that
                matches any separator used in dot, kebab or snake case.
            SPLIT_CAMEL_OR_PASCAL: Compiled regular expression object
                for splitting camel or Pascal case strings into
                constituent words, correctly handling initialisms (e.g.,
                ``URLSuffix -> ['URL', 'Suffix']``)
            SPLIT_FOR_PASCAL_CONVERSION: Compiled regular expression
                object for removing select characters before conversion
                to Pascal case.
            SPLIT_FOR_SEPARATOR_CONVERSION: Compiled regular expression
                object for splitting strings on non-separator word
                boundaries before converting to dot, kebab or snake
                case.
    """
    CAMEL_WORD: Final[re.Pattern[str]] = re.compile(
        r'\b[a-z][a-z0-9]*[A-Z][A-Za-z0-9]*\b'
    )
    DOT_WORD: Final[re.Pattern[str]] = re.compile(
        r'\b[a-z][a-z0-9]*(?:\.[a-z0-9]+)+\b'
    )
    KEBAB_WORD: Final[re.Pattern[str]] = re.compile(
        r'\b[a-z][a-z0-9]*(?:\-[a-z0-9]+)+\b'
    )
    PASCAL_WORD: Final[re.Pattern[str]] = re.compile(
        r'\b[A-Z][A-Z0-9]*[a-z][A-Za-z0-9]*\b'
    )
    SNAKE_WORD: Final[re.Pattern[str]] = re.compile(
        r'\b_?[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b'
    )

    _CASE_PATTERNS: Final[tuple[re.Pattern]] = (
        CAMEL_WORD,
        DOT_WORD,
        KEBAB_WORD,
        PASCAL_WORD,
        SNAKE_WORD
    )
    _CASE_WORD: Final[str] = '|'.join(p.pattern for p in _CASE_PATTERNS)

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
        # PART 1: SPACE NOT PRECEDED OR FOLLOWED BY A SPACE, PUNCTUATION
        # OR PROGRAMMING CASE
        (?<!                            # Not preceded by...
            [\s.!?—–\-,:;"”“\'’‘)\]}}]  # A space character or select
                                        # closing punctuation.
            |                           # OR
            {_CASE_WORD}                # Any Pascal, camel, dot,
                                        # kebab or snake case word.
        )
        [ ]                             # A single space.
        (?!                             # Not followed by...
            [\s—–\-"“”\'‘‘(\[{{]        # A space character or select
                                        # opening punctuation.
            |                           # OR
            {_CASE_WORD}                # Any Pascal, camel, dot,
                                        # kebab, snake case word.
        )
        |                               # OR
        # PART 2: DOT OR KEBAB CASE SEPARATOR
        (?<=                            # Preceded by...
            [a-z][a-z0-9]*              # A letter followed by zero or
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
class WarpingPatterns:
    """
    A namespace for compiled regular expressions for warping text.

    Attributes:
        ANY_APOSTROPHE: Compiled regular expression object that
            matches any straight or curly apostrophe.
        ANY_APOSTROPHE_LOOKAHEAD: Compiled regular expression object
            that matches the position before any straight or curly
            apostrophe.
        APOSTROPHE_IN_WORD: Compiled regular expression object that
            matches a straight apostrophe surrounded by alphabetical
            letter characters.
        AMBIGUOUS_CONTRACTION_PATTERN: Compiled regular expression
            object that matches any contraction that can expand to
            multiple phrases.
        CARDINAL: Compiled regular expression object that matches a
            cardinal number.
        CONTRACTION: Compiled regular expression object that matches
            any expandable contraction.
        CONTRACTION_SUFFIX_TOKENS_PATTERN: Compiled regular expression
            object that matches any contraction suffix.
        DASH: Compiled regular expression object that matches an en or
            em dash.
        EM_DASH_STAND_IN: Compiled regular expression object that
            matches characters that function as an em dash.
        MULTIPLE_SPACES: Compiled regular expression object that
            matches two or more consecutive spaces.
        NAME_PREFIX_PATTERN: Compiled regular expression object that
            matches any name prefix.
        OPENING_STRAIGHT_QUOTES: Compiled regular expression object
            that matches opening straight quotes.
        ORDINAL: Compiled regular expression object that matches an
            ordinal number.
        PERIOD_SEPARATED_INITIALISM: Compiled regular expression
            object that matches a period-separated initialism.
        PUNCT_INSIDE: Compiled regular expression object for punctuation
            inside quotes.
        PUNCT_OUTSIDE: Compiled regular expression object for
            punctuation outside quotes.
        WORD_CHARACTER: Compiled regular expression object that
            matches any word character.
    """
    @staticmethod
    def _create_words_regex(
        words: list[str],
        boundary: RegexBoundary = RegexBoundary.WORD_BOUNDARY,
        sort_by_length: bool = False
    ) -> re.Pattern[str]:
        """
        Create a compiled regular expression object that matches any
        word in the given set.

        Args:
            words: A set of words.
            boundary: The boundary-matching strategy to use. Defaults to
                ``RegexBoundary.WORD_BOUNDARY``.
            sort_by_length: A ``bool`` indicating whether the words
                should be sorted by length in descending order before
                building the pattern. Defaults to ``False``.

        Returns:
            A compiled regular expression object.
        """
        sorted_words: list[str] = words
        if sort_by_length:
            # Sort words by length in descending order, so that longer
            # words containing other words from the set are matched
            # first (e.g., "can't've" before "can't").
            sorted_words = sorted(
                sorted_words, key=len, reverse=True
            )

        escaped_patterns: list[str] = [
            re.escape(w).replace("'", "['’‘]") for w in sorted_words
        ]
        pattern_string: str = '|'.join(escaped_patterns)

        match boundary:
            case RegexBoundary.WORD_BOUNDARY:
                final_pattern: str = rf'\b{pattern_string}\b'
            case RegexBoundary.END_ANCHOR:
                final_pattern: str = rf'{pattern_string}$'
            case RegexBoundary.NONE:
                final_pattern: str = pattern_string

        return re.compile(final_pattern, re.IGNORECASE)

    _NUMBER_BASE_PATTERN: Final[str] = r'''
        (?<!            # Not preceded by...
            \d          # A digit.
            \.          # Followed by a period.
        )
        \b              # An opening word boundary.
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

    ANY_APOSTROPHE: Final[re.Pattern[str]] = re.compile(r"['’‘]")
    ANY_APOSTROPHE_LOOKAHEAD: Final[re.Pattern[str]] = re.compile(r"(?=['’‘])")
    APOSTROPHE_IN_WORD: Final[re.Pattern[str]] = re.compile(rf'''
        # PART 1: APOSTROPHE SURROUNDED BY LETTERS
        (?<=                            # Preceded by...
            [a-z]                       # An alphabetical letter.
        )
        ['’‘]                           # An apostrophe.
        (?=                             # Followed by...
            [a-z]                       # An alphabetical letter.
        )
        |                               # OR
        # PART 2: APOSTROPHE IN ELISION OR DECADE ABBREVIATION
        ['’‘]                           # An apostrophe.
        (?=                             # Followed by...
            {'|'.join(ELISION_WORDS)}   # An elision.
            |                           # OR
            \d{{2}}s                    # An abbreviation for a
        )                               # decade.
        ''', re.VERBOSE | re.IGNORECASE
    )
    AMBIGUOUS_CONTRACTION_PATTERN: Final[re.Pattern[str]] = (
        _create_words_regex(
            AMBIGUOUS_CONTRACTIONS,
            sort_by_length=True
        )
    )
    CARDINAL: Final[re.Pattern[str]] = re.compile(rf'''
        {_NUMBER_BASE_PATTERN}  # A number with or without thousands
                                # separators.
        \b                      # Followed by a closing word boundary.
        (?!                     # Not followed by...
            \.                  # A period.
            \d                  # Followed by a digit.
        )
        ''', re.VERBOSE
    )
    CONTRACTION: Final[re.Pattern[str]] = _create_words_regex(
        list(CONTRACTIONS_MAP.keys()),
        sort_by_length=True
    )
    CONTRACTION_SUFFIX_TOKENS_PATTERN: Final[re.Pattern[str]] = (
        _create_words_regex(CONTRACTION_SUFFIX_TOKENS, sort_by_length=True)
    )
    DASH: Final[re.Pattern[str]] = re.compile(r'[–—]')
    EM_DASH_STAND_IN: Final[re.Pattern[str]] = re.compile(r'\s?--?\s?')
    MAP_SUFFIX_EXCEPTIONS_PATTERN: Final[re.Pattern[str]] = (
        _create_words_regex(
            MAP_SUFFIX_EXCEPTIONS,
            boundary=RegexBoundary.END_ANCHOR,
            sort_by_length=True
        )
    )
    MULTIPLE_SPACES: Final[re.Pattern[str]] = re.compile(r'(?<=\S) {2,}')
    NAME_PREFIX_EXCEPTION_PATTERN: Final[re.Pattern[str]] = (
        _create_words_regex(
            NAME_PREFIX_EXCEPTIONS,
            sort_by_length=True
        )
    )
    NAME_PREFIX_PATTERN: Final[re.Pattern[str]] = _create_words_regex(
        NAME_PREFIXES,
        sort_by_length=True
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
        {_NUMBER_BASE_PATTERN}  # A number with or without thousands
                                # separators.
        (?:st|nd|rd|th)         # Followed by an ordinal suffix.
        \b                      # A closing word boundary.
        ''', re.VERBOSE
    )
    OTHER_PREFIXED_NAMES_PATTERN: Final[re.Pattern[str]] = _create_words_regex(
        list(OTHER_PREFIXED_NAMES_MAP.keys())
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
    WORD_CHARACTER: Final[re.Pattern[str]] = re.compile(r'\w')
