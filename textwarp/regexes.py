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
        APOSTROPHE_IN_WORD: Compiled regular expression object that
            captures a straight apostrophe surrounded by alphabetical
            letter characters. Also captures a straight apostrophe that
            is part of an elision.
        CAMEL_SPLIT: Compiled regular expression object for splitting
            strings before converting substrings to camel case.
        CARDINAL: Compiled regular expression object that captures a
            cardinal number.
        CLOSING_STRAIGHT_DOUBLE: Compiled regular expression object
            that captures closing straight double quotes.
        CLOSING_STRAIGHT_SINGLE: Compiled regular expression object
            that captures closing straight single quotes.
        DOUBLE_HYPHENS: Compiled regular expression object that
            captures hyphens that function as an em dash.
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
        SENTENCE_START: Compiled regular expression object for
            capturing the first letter of a string or the first letter
            after a sentence-ending punctuation character.
        WORD_INCLUDING_PUNCTUATION: Compiled regular expression object
            that captures a sequence of word characters, apostrophes or
            hyphens.
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
        compiled_regex = re.compile(final_pattern, re.IGNORECASE)
        return compiled_regex

    def _create_contraction_token_regex(
        CONTRACTION_TOKENS: set[str]
    ) -> re.Pattern:
        """
        Create a compiled regular expression object that matches any
        contraction token in the given set.

        Args:
            CONTRACTION_TOKENS: A set of contraction tokens.

        Returns:
            A compiled regular expression object.
        """
        # Replace straight apostrophes with a regex character class that
        # matches both straight and curly apostrophes.
        escaped_patterns = [
            re.escape(t).replace("'", "['’‘]") for t in CONTRACTION_TOKENS
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

    APOSTROPHE_IN_WORD: re.Pattern = re.compile(rf"""
        (?<=[a-z])'(?=[a-z])                # A straight apostrophe
                                            # inside a word.
        |                                   # OR
        '                                   # A straight apostrophe
        (?=                                 # followed by...
            {'|'.join(ELISION_WORDS)}\b     # An elision.
            |                               # OR
            \d{{2}}s\b                      # An abbreviation for a
        )                                   # decade.
        """, re.VERBOSE | re.IGNORECASE
    )
    CAMEL_SPLIT: re.Pattern[str] = re.compile(r'(?<=[\s—–\-])')
    CARDINAL: re.Pattern[str] = re.compile(
        r'(?<!\d\.)\b(\d{1,3}(?:,\d{3})+|\d+)\b(?!\.\d)'
    )
    CONTRACTION: re.Pattern[str] = _create_contraction_regex(CONTRACTIONS_MAP)
    CONTRACTION_TOKENS: re.Pattern[str] = _create_contraction_token_regex(
        CONTRACTION_TOKENS
    )
    DOUBLE_HYPHENS: re.Pattern[str] = re.compile(r'\s?--?\s?')
    MULTIPLE_SPACES: re.Pattern[str] = re.compile(r'(?<=\S) {2,}')
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
    SENTENCE_START: re.Pattern[str] = re.compile(rf"""
        ^                   # The start of a line (see re.MULTILINE).
        |                   # OR
        (?<=                # Preceded by...
            (?:             # A non-capturing group for...
                # A period not preceded by an abbreviation.
                (?<!{'|'.join(ABBREVIATIONS)})\.
                |           # OR
                [!?]        # A question mark or exclamation mark.
            )
            ["”“'’‘)\]]*    # Followed by any number of quotes,
                            # brackets or closing parentheses.
            \s+             # Followed by one or more whitespace
                            # characters.
        )
        """, re.VERBOSE | re.MULTILINE
    )
    WORD_INCLUDING_PUNCTUATION: re.Pattern[str] = re.compile(
        r"[a-zA-Z][\w'‘’\-]*")
