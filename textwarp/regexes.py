import regex as re

from textwarp.config import (
    ABBREVIATIONS,
    CONTRACTIONS_MAP,
    CONTRACTION_SUFFIX_SET,
    ELISION_WORDS,
    NAME_PREFIXES
)


class SeparatorRegexes:
    """
    Compiled regular expressions for parsing and warping text before
    conversion to kebab case or snake case.

    Attributes:
        CAMEL_CASE: Compiled regular expression object that captures a
            camel case string.
        CAMEL_PASCAL_SPLIT: Compiled regular expression object for
            splitting on the boundary between words in camel case and
            Pascal case.
        FIRST_PASCAL_CHARACTER: Compiled regular expression object that
            captures the first character of a Pascal case word.
        KEBAB_CASE: Compiled regular expression object that captures a
            kebab case string.
        PASCAL_CASE: Compiled regular expression object that captures a
            Pascal case string.
        PASCAL_SPLIT: Compiled regular expression object for splitting
            strings before converting substrings to camel case or
            Pascal case.
        SEPARATOR_SPLIT: Compiled regular expression object for
            splitting strings before converting substrings to kebab
            case or snake case.
        SHORT_ACRONYM: Compiled regular expression object that captures
            a two-character acronym or initialism.
        SNAKE_CASE: Compiled regular expression object that captures a
            snake case string.
    """
    ALPHABETICAL: re.Pattern = re.compile(r'[A-Za-z]')
    CAMEL_CASE: re.Pattern = re.compile(
        r'[a-z][a-z0-9]*([A-Z][A-Z]?[a-z0-9]*)+'
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
        ''', re.VERBOSE)
    FIRST_PASCAL_CHARACTER: re.Pattern[str] = re.compile(
        r'[A-Z][a-z]+(?:[A-Z][a-z]+)*'
    )
    KEBAB_CASE: re.Pattern[str] = re.compile(
        r'([A-Za-z0-9]+\-[A-Za-z0-9]\-?)+'
    )
    PASCAL_CASE: re.Pattern[str] = re.compile(
        r'[A-Z][a-z0-9]+([A-Z][A-Z]?[a-z0-9]*)+'
    )
    PASCAL_SPLIT: re.Pattern[str] = re.compile(r'''
        (?<![ .!?—–\-,:;"”\'’]) # Negative lookbehind to preserve spacing
                                    # after spaces, punctuation and dashes
        [ ]                     # Character class to split on a single space
        (?![ —–\-"“\'‘\(\[{])   # Negative lookahead to preserve spacing
                                    # before dashes, quotes and brackets
        |                       # OR
        (?<=\w)-(?=\w)          # Positive lookbehind to split on a hyphen
                                    # between word characters and convert from
                                    # kebab case
        |                       # OR
        _                       # Split on an underscore to convert from snake
                                    # case
        |                       # OR
        \b                      # Split on a word boundary character to ensure
                                    # substrings begin and end with a word
                                    # character.
        ''', re.VERBOSE
    )
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
    SHORT_ACRONYM: re.Pattern[str] = re.compile(r'[A-Z]{2}\b')
    SNAKE_CASE: re.Pattern[str] = re.compile(r'([A-Za-z0-9]+_[A-Za-z0-9]+_?)+')


class WarpingRegexes:
    """
    Compiled regular expressions and strings for parsing and warping
    text.

    Attributes:
        WORD_INCLUDING_PUNCTUATION: Compiled regular expression object
            that captures a sequence of word characters, apostrophes,
            hyphens or period-separated initialisms.

        APOSTROPHE_IN_WORD: Compiled regular expression object that
            captures a straight apostrophe surrounded by alphabetical
            letter characters. Also captures a straight apostrophe that
            is part of a decade abbreviation or elision.
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
    def _create_contraction_regex(CONTRACTIONS_MAP: dict) -> re.Pattern:
        """
        Create a compiled regular expression object that matches any
        contraction in the given contractions map.

        Args:
            CONTRACTIONS_MAP: A dictionary mapping contractions to their
                expanded versions.

        Returns:
            A compiled regular expression object.
        """
        # Sort the contractions by length in descending order, so that
        # longer contractions containing contraction substrings are
        # matched first (e.g., "can't've" before "can't").
        sorted_contractions = sorted(
            CONTRACTIONS_MAP.keys(), key=len, reverse=True
        )
        # Replace straight apostrophes with a regex character class that
        # matches both straight and curly apostrophes.
        escaped_patterns = [
            re.escape(c).replace("'", "['’‘]") for c in sorted_contractions
        ]
        pattern_string = '|'.join(escaped_patterns)
        final_pattern = rf'\b{pattern_string}\b'
        return re.compile(final_pattern, re.IGNORECASE)

    def _create_contraction_suffix_regex(
        CONTRACTION_SUFFIX_SET: set[str]
    ) -> re.Pattern:
        """
        Create a compiled regular expression object that matches any
        contraction token in the given set.

        Args:
            CONTRACTION_SUFFIXES: A set of contraction tokens.

        Returns:
            A compiled regular expression object.
        """
        # Replace straight apostrophes with a regex character class that
        # matches both straight and curly apostrophes.
        escaped_patterns = [
            re.escape(t).replace("'", "['’‘]") for t in CONTRACTION_SUFFIX_SET
        ]
        pattern_string = '|'.join(escaped_patterns)
        final_pattern = rf'\b{pattern_string}\b'
        return re.compile(final_pattern, re.IGNORECASE)

    def _create_name_prefix_regex(NAME_PREFIXES: set[str]) -> re.Pattern:
        """
        Create a compiled regular expression object that matches any
        name prefix in the given set.

        Args:
            NAME_PREFIXES: A set of name prefixes.

        Returns:
            A compiled regular expression object.
        """
        # Replace straight apostrophes with a regex character class that
        # matches both straight and curly apostrophes.
        prefix_patterns = [
            re.escape(p).replace("'", "['’‘]") for p in NAME_PREFIXES
        ]
        pattern_string = '|'.join(prefix_patterns)
        final_pattern = rf'\b{pattern_string}\b'
        return re.compile(final_pattern)

    WORD_INCLUDING_PUNCTUATION: re.Pattern[str] = re.compile(r"""
        # PART 1: Period-separated initialisms (e.g., U.S.A.)
        \b          # The start of a word boundary.
        \w+         # One or more word characters.
        (?:         # A non-capturing group of...
        \.          # A period.
        [a-z]+      # Followed by one or more word characters.
        )+          # One or more repetitions of the group.
        \.?         # An optional final period.
        \b          # The end of the word boundary.
        |           # OR
        # PART 2: Words including other internal punctuation.
        \b          # The start of a word boundary.
        [a-z]       # A word character.
        [\w'‘’-]*   # Zero or more word characters, straight or curly
                    # apostrophes, straight or curly single quotes or
                    # hyphens.
        \b          # The end of the word boundary.
        """, re.VERBOSE | re.IGNORECASE
    )

    APOSTROPHE_IN_WORD: re.Pattern = re.compile(rf"""
        (?<=[a-z])'(?=[a-z])                # A straight apostrophe
                                            # inside a word.
        |                                   # OR
        '                                   # A straight apostrophe.
        (?=                                 # Followed by...
            {'|'.join(ELISION_WORDS)}\b     # An elision.
            |                               # OR
            \d{{2}}s\b                      # An abbreviation for a
        )                                   # decade.
        """, re.VERBOSE | re.IGNORECASE
    )
    CARDINAL: re.Pattern[str] = re.compile(
        r'(?<!\d\.)\b(\d{1,3}(?:,\d{3})+|\d+)\b(?!\.\d)'
    )
    CONTRACTION: re.Pattern[str] = _create_contraction_regex(CONTRACTIONS_MAP)
    CONTRACTION_SUFFIXES: re.Pattern[str] = _create_contraction_suffix_regex(
        CONTRACTION_SUFFIX_SET
    )
    DASH: re.Pattern[str] = re.compile(r'[–—]')
    DOUBLE_HYPHENS: re.Pattern[str] = re.compile(r'\s?--?\s?')
    FIRST_WORD_IN_SENTENCE: re.Pattern[str] = re.compile(rf"""
        (?:                     # CONTEXT FOR SENTENCE START
            ^                   # The start of a line (see re.MULTILINE).
            |                   # OR
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
        {WORD_INCLUDING_PUNCTUATION.pattern}
        """, re.VERBOSE | re.MULTILINE | re.IGNORECASE
    )
    MULTIPLE_SPACES: re.Pattern[str] = re.compile(r'(?<=\S) {2,}')
    NAME_PREFIXES: re.Pattern[str] = _create_name_prefix_regex(NAME_PREFIXES)
    OPENING_STRAIGHT_QUOTES: re.Pattern[str] = re.compile(r"""
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
