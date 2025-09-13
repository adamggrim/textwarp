import regex as re

from textwarp.config import (
    ABBREVIATIONS,
    AMBIGUOUS_CONTRACTIONS,
    CONTRACTIONS_MAP,
    CONTRACTION_SUFFIXES,
    ELISION_WORDS,
    NAME_PREFIXES
)


class CasePatterns:
    """
    Compiled regular expressions for identifying select cases.

    Attributes:
        CAMEL_WORD: Compiled regular expression object that
            captures a camel case string.
        DOT_WORD: Compiled regular expression object that
            captures a dot case string.
        KEBAB_WORD: Compiled regular expression object that
            captures a kebab case string.
        PASCAL_WORD: Compiled regular expression object that
            captures a Pascal case word.
        SNAKE_WORD: Compiled regular expression object that
            captures a snake case string.
    """
    CAMEL_WORD: re.Pattern = re.compile(
        r'\b[a-z][a-z0-9]*[A-Z][a-zA-Z0-9]*\b'
    )
    DOT_WORD: re.Pattern[str] = re.compile(
        r'\b[a-z][a-z0-9]*(?:\.[a-z0-9]+)+\b'
    )
    KEBAB_WORD: re.Pattern[str] = re.compile(
        r'\b[a-z][a-z0-9]*(?:\-[a-z0-9]+)+\b'
    )
    PASCAL_WORD: re.Pattern[str] = re.compile(
        r'\b(?:[A-Z][A-Z0-9]*[a-z]+[A-Z0-9]*)+\b'
    )
    SNAKE_WORD: re.Pattern[str] = re.compile(
        r'\b_?[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b'
    )


class SeparatorCasePatterns:
    """
    Compiled regular expressions for conversion to and from separator
    cases.

    Attributes:
        CAMEL_WORD: Compiled regular expression object that captures a
            camel case string.
        KEBAB_CASE: Compiled regular expression object that captures a
            kebab case string.
        PASCAL_CASE: Compiled regular expression object that captures a
            Pascal case string.
        PASCAL_SPLIT: Compiled regular expression object for splitting
            strings before converting substrings to camel case or
            Pascal case.
        PASCAL_WORD: Compiled regular expression object that captures a
            Pascal case word, with capturing groups around the
            first letter and the rest of the word.
        SEPARATOR_SPLIT: Compiled regular expression object for
            splitting strings before converting substrings to kebab
            case or snake case.
        SNAKE_CASE: Compiled regular expression object that captures a
            snake case string.
    """
    _CASE_PATTERNS: list[re.Pattern] = [
        pattern for name, pattern in vars(CasePatterns).items()
        if not name.startswith('__') and isinstance(pattern, re.Pattern)
    ]
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
        # OR SELECT CASES
        (?<!                            # Not preceded by...
            [\s.!?—–\-,:;"”“\'’‘\)\]}}] # A space character or select
                                        # punctuation.
            |                           # OR
            {_CASE_WORD}                # Any Pascal, camel, dot,
                                        # kebab or snake case word.
        )
        [ ]                             # A single space.
        (?!                             # Not followed by...
            [\s—–\-"“”\'‘‘\(\[{{]       # A space, select punctuation
                                        # or an opening parenthesis,
                                        # bracket or brace.
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
        )
        )
        ''', re.VERBOSE
    )
    SPLIT_FOR_SEPARATOR_CASE: re.Pattern[str] = re.compile(rf'''


class WarpingPatterns:
    """
    Compiled regular expressions and strings for parsing and warping
    text.

    Attributes:
        WORD_INCLUDING_PUNCTUATION: Compiled regular expression object
            that captures a sequence of word characters, apostrophes,
            hyphens or period-separated initialisms.

        CARDINAL: Compiled regular expression object that captures a
            cardinal number.
        DOUBLE_HYPHENS: Compiled regular expression object that
            captures hyphens that function as an em dash.
        FIRST_WORD_IN_SENTENCE: Compiled regular expression object for
            capturing the first letter of a string or the first letter
            after a sentence-ending punctuation character.
        OPENING_STRAIGHT_QUOTES: Compiled regular expression object
            that captures opening straight quotes.
        ORDINAL: Compiled regular expression object that captures an
            ordinal number.
        PUNCT_INSIDE: Compiled regular expression object with capturing
            groups for punctuation inside quotes and quotes outside
            punctuation.
        PUNCT_OUTSIDE: Compiled regular expression object with
            capturing groups for quotes inside punctuation and
            punctuation outside quotes.
    """
    def _create_contraction_regex(contractions: set[str]) -> re.Pattern:
        """
        Create a compiled regular expression object that matches any
        contraction in the given contractions map.

        Args:
            contractions: An iterable of contractions.

        Returns:
            A compiled regular expression object.
        """
        # Sort contractions by length in descending order, so that
        # longer contractions containing contraction substrings are
        # matched first (e.g., "can't've" before "can't").
        sorted_contractions = sorted(
            contractions, key=len, reverse=True
        )
        # Replace straight apostrophes with a regex character class that
        # matches both straight and curly apostrophes.
        escaped_patterns = [
            re.escape(c).replace("'", "['’‘]") for c in sorted_contractions
        ]
        pattern_string = '|'.join(escaped_patterns)
        final_pattern = rf'\b{pattern_string}\b'
        return re.compile(final_pattern, re.IGNORECASE)

    def _create_name_prefix_regex(name_prefixes: set[str]) -> re.Pattern:
        """
        Create a compiled regular expression object that matches any
        name prefix in the given set.

        Args:
            name_prefixes: A set of name prefixes.

        Returns:
            A compiled regular expression object.
        """
        # Replace straight apostrophes with a regex character class that
        # matches both straight and curly apostrophes.
        prefix_patterns = [
            re.escape(p).replace("'", "['’‘]") for p in name_prefixes
        ]
        pattern_string = '|'.join(prefix_patterns)
        final_pattern = rf'\b{pattern_string}\b'
        return re.compile(final_pattern)

    WORD_INCLUDING_PUNCTUATION: re.Pattern[str] = re.compile(r"""
        # PART 1: PERIOD-SEPARATED INITIALISMS (e.g., U.S.A.)
        \b          # The start of a word boundary.
        \w+         # One or more word characters.
        (?:         # A non-capturing group of...
            \.      # A period.
            [a-z]+  # Followed by one or more word characters.
        )+          # One or more repetitions of the group.
        \.?         # An optional final period.
        \b          # The end of the word boundary.
        |           # OR
        # PART 2: WORDS INCLUDING OTHER INTERNAL PUNCTUATION
        \b          # The start of a word boundary.
        [a-z]       # A word character.
        [\w'‘’-]*   # Zero or more word characters, straight or curly
                    # apostrophes, straight or curly single quotes or
                    # hyphens.
        \b          # The end of the word boundary.
        """, re.VERBOSE | re.IGNORECASE
    )

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
            {'|'.join(ELISION_WORDS)}\b # An elision.
            |                           # OR
            \d{{2}}s\b                  # An abbreviation for a
        )                               # decade.
        ''', re.VERBOSE | re.IGNORECASE
    )
    AMBIGUOUS_CONTRACTION_PATTERN: re.Pattern = _create_contraction_regex(
        AMBIGUOUS_CONTRACTIONS
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
    CONTRACTION: re.Pattern[str] = _create_contraction_regex(
        set(CONTRACTIONS_MAP.keys())
    )
    CONTRACTION_SUFFIX_PATTERN: re.Pattern[str] = (
        _create_contraction_regex(CONTRACTION_SUFFIXES)
    )
    DASH: re.Pattern[str] = re.compile(r'[–—]')
    DOUBLE_HYPHENS: re.Pattern[str] = re.compile(r'\s?--?\s?')
    FIRST_WORD_IN_SENTENCE: re.Pattern[str] = re.compile(rf"""
        # CONTEXT FOR SENTENCE START (2 CONDITIONS)
        (?:
            # CONDITION 1: AT THE START OF A LINE
            ^
            |                   # OR
            # CONDITION 2: AFTER SENTENCE-ENDING PUNCTUATION
            (?<=                # Preceded by...
                (?:             # A non-capturing group for...
                    # A period not preceded by an abbreviation.
                    (?<!{'|'.join(ABBREVIATIONS)})\.
                    |           # OR
                    [?!]        # A question or exclamation mark.
                )
                ["”“'’‘)\]]*    # Followed by any number of quotes,
                                # brackets or closing parentheses.
                \s+             # Followed by one or more whitespace
                                # characters.
            )
        )
        # TARGET: THE WORD TO MATCH
        {WORD_INCLUDING_PUNCTUATION.pattern}
        """, re.VERBOSE | re.MULTILINE | re.IGNORECASE
    )
    MULTIPLE_SPACES: re.Pattern[str] = re.compile(r'(?<=\S) {2,}')
    NAME_PREFIX_PATTERN: re.Pattern[str] = _create_name_prefix_regex(
        NAME_PREFIXES
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
    PUNCT_INSIDE: re.Pattern[str] = re.compile(r'([.,])(["”\'’]?["”\'’])')
    PUNCT_OUTSIDE: re.Pattern[str] = re.compile(r'(["”\'’]?["”\'’])([.,])')
    WORD_CHARACTER: re.Pattern[str] = re.compile(r'\w')
    WORD_CHARACTERS: re.Pattern[str] = re.compile(r'\w+')
