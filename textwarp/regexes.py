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
    Compiled regular expressions for identifying different types
    of words.

    Attributes:
        CAMEL_WORD: Compiled regular expression object that
            captures a camel case string.
        DOT_WORD: Compiled regular expression object that
            captures a dot case string.
        KEBAB_WORD: Compiled regular expression object that
            captures a kebab case string.
        LOWERCASE_WORD: Compiled regular expression object that
            captures a lowercase word.
        PASCAL_WORD: Compiled regular expression object that
            captures a Pascal case word.
        SNAKE_WORD: Compiled regular expression object that
            captures a snake case string.
    """
    CAMEL_WORD: re.Pattern = re.compile(
        r'\b[a-z][a-z0-9]*[A-Z][a-zA-Z0-9]*\b'
    )
    DOT_WORD: re.Pattern[str] = re.compile(
        r'\b[a-z0-9]+(?:\.[a-z0-9]+)+\b'
    )
    KEBAB_WORD: re.Pattern[str] = re.compile(
        r'\b[a-z0-9]+(?:\-[a-z0-9]+)+\b'
    )
    LOWERCASE_WORD: re.Pattern = re.compile(r'\b[a-z][a-z0-9]*\b')
    PASCAL_WORD: re.Pattern[str] = re.compile(
        r'\b(?:[A-Z][a-zA-Z0-9]*){2,}\b'
    )
    SNAKE_WORD: re.Pattern[str] = re.compile(
        r'\b_?[a-z0-9]+(?:_[a-z0-9]+)+\b'
    )


class SeparatorPatterns:
    """
    Compiled regular expressions for parsing and warping text before
    conversion to kebab case or snake case.

    Attributes:
        APOSTROPHE_IN_WORD: Compiled regular expression object that
            captures a straight apostrophe surrounded by alphabetical
            letter characters. Also captures a straight apostrophe that
            is part of a decade abbreviation or elision.
        CAMEL_WORD: Compiled regular expression object that captures a
            camel case string.
        CAMEL_PASCAL_SPLIT: Compiled regular expression object for
            splitting on the boundary between words in camel case and
            Pascal case.
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
    APOSTROPHE_IN_WORD: re.Pattern = re.compile(rf"""
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
        """, re.VERBOSE | re.IGNORECASE
    )
    CAMEL_PASCAL_SPLIT: re.Pattern[str] = re.compile(r'''
        (?<=[a-z0-9])   # Positive lookbehind to split after a lowercase
                        # letter or digit
        (?=[A-Z])       # Positive lookahead to split before an uppercase
                        # letter
        |               # OR
        (?<=[a-zA-Z])   # Positive lookbehind to split after a lowercase or
                        # uppercase letter
        (?=[0-9])       # Positive lookahead to split before a digit
        ''', re.VERBOSE
    )
    LETTER: re.Pattern = re.compile(r'[A-Za-z]')
    SEPARATOR_SPLIT: re.Pattern[str] = re.compile(r'''
        (?<=\W\s)               # Positive lookbehind to split after a
                                # non-word character followed by a space
                                # character
        |                       # OR
        (?<=["“\'‘(\[{])        # Positive lookbehind to split after opening
                                # quotes and brackets
        |                       # OR
        (?<=—\b)                # Postive lookbehind to split after an em dash
                                # followed by a word boundary character
        |                       # OR
        (?<=\t)                 # Positive lookbehind to split after a tab
                                # character
        |                       # OR
        (?=[.!?—,:;"”\'’)\]}])  # Positive lookahead to split before
                                # punctuation or an em dash or bracket
        |                       # OR
        (?=\s+[–"”(\[{])        # Positive lookahead to split before spacing
                                # followed by an en dash, quote or bracket
        |                       # OR
        (?=--)                  # Positive lookahead to split before two
                                # consecutive hyphens
        |                       # OR
        (?=-\s+)                # Positive lookahead to split before a hyphen
                                # followed by one or more whitespace characters
        |                       # OR
        (?=\s{2,})              # Positive lookahead to split before
                                # consecutive spaces
        |                       # OR
        (?=\t)                  # Positive lookahead to split on a tab
                                # character
        ''', re.VERBOSE
    )
    SPLIT_FOR_PASCAL: re.Pattern[str] = re.compile(rf'''
        # PART 1: SPACE NOT PRECEDED OR FOLLOWED BY A SPACE, PUNCTUATION
        # OR ANOTHER CASE
        (?<!                            # Not preceded by...
            [ .!?—–\-,:;"”\'’\)\]}}]    # A space or select punctuation.
            |                           # OR
            {_ANY_CASE_WORD_PATTERN}       # A Pascal case word.
            |                           # OR
            {CAMEL_WORD.pattern}        # A camel case word.
            |                           # OR
            {DOT_WORD.pattern}          # A dot case word.
            |                           # OR
            {KEBAB_WORD.pattern}        # A kebab case word.
            |                           # OR
            {SNAKE_WORD.pattern}        # A snake case word.
            |                           # OR
            {LOWERCASE_WORD.pattern}    # A lowercase word.
        )
        [ ]                             # A single space.
        (?!                             # Not followed by...
            [ —–\-"“\'‘\(\[{{]          # A space, select punctuation
                                        # or an opening parenthesis,
                                        # bracket or brace.
            |                           # OR
            {PASCAL_WORD.pattern}       # A Pascal case word.
            |                           # OR
            {CAMEL_WORD.pattern}        # A camel case word.
            |                           # OR
            {DOT_WORD.pattern}          # A dot case word.
            |                           # OR
            {KEBAB_WORD.pattern}        # A kebab case word.
            |                           # OR
            {SNAKE_WORD.pattern}        # A snake case word.
            |                           # OR
            {LOWERCASE_WORD.pattern}    # A lowercase word.
        )
        |                               # OR
        # PART 2: DOT OR KEBAB CASE SEPARATOR
        (?<=                            # Preceded by...
            [A-Za-z0-9]                 # A letter or digit.
        )
        [.\-]                           # A hyphen or period.
        (?=                             # Followed by...
            [A-Za-z0-9]                 # A letter or digit.
        )
        |                               # OR
        # PART 3: SNAKE CASE SEPARATOR
        _                               # An underscore.
        |                               # OR
        # PART 3: POSITION FOLLOWED BY ENDING PUNCTUATION
        (?=                             # Followed by...
            [.!?—–\-,:;"”\'’\)\]}}]     # Select punctuation or a
                                        # closing parenthesis, bracket
                                        # or brace.
            [ \t]+                      # One or more space or tab
                                        # characters.
        )
        |                               # OR
        # PART 4: POSITION PRECEDED BY ENDING PUNCTUATION
        (?<=                            # Preceded by...
            [.!?—–\-,:;"”\'’\)\]}}]     # Select punctuation or a
                                        # closing parenthesis, bracket
                                        # or brace.
            [ \t]+                      # One or more space or tab
                                        # characters.
        )
        |                               # OR
        # PART 5: POSITION PRECEDED BY ANOTHER CASE
        (?<=                            # Preceded by...
            {PASCAL_WORD.pattern}       # A Pascal case word.
            |                           # OR
            {CAMEL_WORD.pattern}        # A camel case word.
            |                           # OR
            {DOT_WORD.pattern}          # A dot case word.
            |                           # OR
            {KEBAB_WORD.pattern}        # A kebab case word.
            |                           # OR
            {SNAKE_WORD.pattern}        # A snake case word.
            |                           # OR
            {LOWERCASE_WORD.pattern}    # A lowercase word.
        )
        |                               # OR
        # PART 6: POSITION FOLLOWED BY ANOTHER CASE
        (?=                             # Followed by...
            {PASCAL_WORD.pattern}       # A Pascal case word.
            |                           # OR
            {CAMEL_WORD.pattern}        # A camel case word.
            |                           # OR
            {DOT_WORD.pattern}          # A dot case word.
            |                           # OR
            {KEBAB_WORD.pattern}        # A kebab case word.
            |                           # OR
            {SNAKE_WORD.pattern}        # A snake case word.
            |                           # OR
            {LOWERCASE_WORD.pattern}    # A lowercase word.
        )
        |                               # OR
        # PART 6: NEWLINE CHARACTER
        (?=                             # Followed by...
            \n                          # A newline character.
        )
        ''', re.VERBOSE
    )


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
        # Sort the contractions by length in descending order, so that
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
        \.          # A period.
        [a-z]+      # Followed by one or more word characters.
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

    AMBIGUOUS_CONTRACTION_PATTERN: re.Pattern = _create_contraction_regex(
        AMBIGUOUS_CONTRACTIONS
    )
    CARDINAL: re.Pattern[str] = re.compile(
        r'(?<!\d\.)\b(\d{1,3}(?:,\d{3})+|\d+)\b(?!\.\d)'
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
        # TARGET: THE ACTUAL WORD TO MATCH
        {WORD_INCLUDING_PUNCTUATION.pattern}
        """, re.VERBOSE | re.MULTILINE | re.IGNORECASE
    )
    MULTIPLE_SPACES: re.Pattern[str] = re.compile(r'(?<=\S) {2,}')
    NAME_PREFIX_PATTERN: re.Pattern[str] = _create_name_prefix_regex(
        NAME_PREFIXES
    )
    OPENING_STRAIGHT_QUOTES: re.Pattern[str] = re.compile(r"""
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
            (?<=[\s([{])    # Preceded by a whitespace character,
                            # opening parenthesis, opening square
                            # bracket or opening curly brace.
        )
        (                   # GROUP 2 (DOUBLE QUOTES)
        (?<!['’]\s)         # Not preceded by a straight or closing
                            # single quote followed by a space.
        "+                  # One or more straight double quotes.
        )
        """, re.VERBOSE
    )
    ORDINAL: re.Pattern[str] = re.compile(r'\b\d+(?:st|nd|rd|th)\b')
    PUNCT_INSIDE: re.Pattern[str] = re.compile(r'([.,])(["”\'’]?["”\'’])')
    PUNCT_OUTSIDE: re.Pattern[str] = re.compile(r'(["”\'’]?["”\'’])([.,])')
    WORD_CHARACTER: re.Pattern[str] = re.compile(r'\w')
    WORD_CHARACTERS: re.Pattern[str] = re.compile(r'\w+')
