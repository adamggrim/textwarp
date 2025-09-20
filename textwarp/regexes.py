import regex as re

from textwarp.config import (
    AMBIGUOUS_CONTRACTIONS,
    COMBINED_ABBREVIATIONS,
    CONTRACTIONS_MAP,
    CONTRACTION_SUFFIX_TOKENS,
    ELISION_WORDS,
    NAME_PREFIXES,
    MAP_SUFFIX_EXCEPTIONS,
    OTHER_PREFIXED_NAMES_MAP
)


class ProgrammingCasePatterns:
    """
    A namespace for compiled regular expressions for identifying and
    converting to and from programming cases.

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
                matches any separator character used in dot case, kebab
                case or snake case.
            SPLIT_CAMEL_OR_PASCAL: Compiled regular expression object
                for splitting camel or Pascal case strings before
                converting broken words to another programming case.
            SPLIT_FOR_PASCAL_CONVERSION: Compiled regular expression
                object for splitting strings before converting to Pascal
                case.
            SPLIT_FOR_SEPARATOR_CONVERSION: Compiled regular expression
                object for splitting strings before converting to kebab
                or snake case.
    """
    CAMEL_WORD: re.Pattern = re.compile(
        r'\b[a-z][a-z0-9]*[A-Z][A-Za-z0-9]*\b'
    )
    DOT_WORD: re.Pattern[str] = re.compile(
        r'\b[a-z][a-z0-9]*(?:\.[a-z0-9]+)+\b'
    )
    KEBAB_WORD: re.Pattern[str] = re.compile(
        r'\b[a-z][a-z0-9]*(?:\-[a-z0-9]+)+\b'
    )
    PASCAL_WORD: re.Pattern[str] = re.compile(
        r'\b[A-Z][A-Z0-9]*[a-z][A-Za-z0-9]*\b'
    )
    SNAKE_WORD: re.Pattern[str] = re.compile(
        r'\b_?[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b'
    )

    _CASE_PATTERNS: tuple[re.Pattern] = (
        CAMEL_WORD,
        DOT_WORD,
        KEBAB_WORD,
        PASCAL_WORD,
        SNAKE_WORD
    )
    _CASE_WORD: str = '|'.join(p.pattern for p in _CASE_PATTERNS)

    ANY_SEPARATOR: re.Pattern = re.compile(r'[.\-_]')
    SPLIT_CAMEL_OR_PASCAL: re.Pattern[str] = re.compile(r'''
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
    SPLIT_FOR_PASCAL_CONVERSION: re.Pattern[str] = re.compile(rf'''
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
    SPLIT_FOR_SEPARATOR_CONVERSION: re.Pattern[str] = re.compile(r'''
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
        DOUBLE_HYPHENS: Compiled regular expression object that
            matches double hyphens that function as an em dash.
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
        WORD_INCLUDING_PUNCTUATION: Compiled regular expression
            object that matches any word with or without internal
            punctuation.
    """
    @staticmethod
    def _create_words_regex(
        words: set[str],
        sort_by_length: bool = False
    ) -> re.Pattern:
        """
        Create a compiled regular expression object that matches any
        word in the given set.

        Args:
            words: A set of words.

        Returns:
            A compiled regular expression object.
        """
        sorted_words = words
        if sort_by_length:
            # Sort words by length in descending order, so that longer
            # words containing other words from the set are matched
            # first (e.g., "can't've" before "can't").
            sorted_words = sorted(
                sorted_words, key=len, reverse=True
            )
        escaped_patterns = [
            re.escape(w).replace("'", "['’‘]") for w in sorted_words
        ]
        pattern_string = '|'.join(escaped_patterns)
        final_pattern = rf'\b{pattern_string}\b'
        return re.compile(final_pattern, re.IGNORECASE)

    WORD_INCLUDING_PUNCTUATION: re.Pattern[str] = re.compile(r'''
        # PART 1: PERIOD-SEPARATED INITIALISMS (e.g., U.S.A.)
        \b          # A word boundary.
        \w+         # One or more word characters.
        (?:         # A non-capturing group for...
            \.      # A period.
            [a-z]+  # Followed by one or more alphabetical letters.
        )+          # One or more repetitions of the group.
        \.?         # An optional final period.
        [\w'‘’-]*   # Zero or more word characters, straight or curly
                    # apostrophes, straight or curly single quotes or
                    # hyphens.
        \b          # A word boundary.
        |           # OR
        # PART 2: WORDS INCLUDING OTHER INTERNAL PUNCTUATION
        \b          # A word boundary.
        [a-z]       # An alphabetical letter.
        [\w'‘’-]*   # Zero or more word characters, straight or curly
                    # apostrophes, straight or curly single quotes or
                    # hyphens.
        \b          # A word boundary.
        ''', re.VERBOSE | re.IGNORECASE
    )

    ANY_APOSTROPHE: re.Pattern = re.compile(r"['’‘]")
    ANY_APOSTROPHE_LOOKAHEAD: re.Pattern = re.compile(r"(?=['’‘])")
    APOSTROPHE_IN_WORD: re.Pattern = re.compile(rf'''
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
    AMBIGUOUS_CONTRACTION_PATTERN: re.Pattern = _create_words_regex(
        AMBIGUOUS_CONTRACTIONS,
        sort_by_length=True
    )
    CARDINAL: re.Pattern[str] = re.compile(r'''
        # A CARDINAL INTEGER WITH OPTIONAL THOUSANDS SEPARATORS
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
        \b              # A word boundary.
        (?!             # Not followed by...
            \.          # A period.
            \d          # Followed by a digit.
        )
        ''', re.VERBOSE
    )
    CONTRACTION: re.Pattern[str] = _create_words_regex(
        set(CONTRACTIONS_MAP.keys()),
        sort_by_length=True
    )
    CONTRACTION_SUFFIX_TOKENS_PATTERN: re.Pattern[str] = (
        _create_words_regex(CONTRACTION_SUFFIX_TOKENS, sort_by_length=True)
    )
    DASH: re.Pattern[str] = re.compile(r'[–—]')
    DOUBLE_HYPHENS: re.Pattern[str] = re.compile(r'\s?--?\s?')
    MAP_SUFFIX_EXCEPTIONS: re.Pattern = _create_words_regex(
        set(MAP_SUFFIX_EXCEPTIONS),
        sort_by_length=True
    )
    MULTIPLE_SPACES: re.Pattern[str] = re.compile(r'(?<=\S) {2,}')
    NAME_PREFIX_PATTERN: re.Pattern[str] = _create_words_regex(
        NAME_PREFIXES,
        sort_by_length=True
    )
    OPENING_STRAIGHT_QUOTES: re.Pattern[str] = re.compile(r'''
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
    ORDINAL: re.Pattern[str] = re.compile(r'\b\d+(?:st|nd|rd|th)\b')
    OTHER_PREFIXED_NAMES_PATTERN: re.Pattern = _create_words_regex(
        set(OTHER_PREFIXED_NAMES_MAP.keys())
    )
    PERIOD_SEPARATED_INITIALISM: re.Pattern[str] = re.compile(
        r'\b(?:[A-Za-z]\.){2,}'
    )
    PUNCT_INSIDE: re.Pattern[str] = re.compile(r'([.,])(["”\'’]?["”\'’])')
    PUNCT_OUTSIDE: re.Pattern[str] = re.compile(r'(["”\'’]?["”\'’])([.,])')
    WORD_CHARACTER: re.Pattern[str] = re.compile(r'\w')
