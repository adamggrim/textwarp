"""Universal regular expressions for converting between cases."""

from functools import lru_cache

import regex as re

__all__ = [
    'get_any_separator',
    'get_split_camel_or_pascal',
    'get_split_for_pascal_conversion',
    'get_split_for_separator_conversion'
]

@lru_cache(maxsize=1)
def get_any_separator() -> re.Pattern[str]:
    """
    Get a regular expression matching any separator used in dot, kebab
    or snake case.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'[.\-_]')


@lru_cache(maxsize=1)
def get_split_camel_or_pascal() -> re.Pattern[str]:
    """
    Get a regular expression for splitting camel or Pascal case strings
    into constituent words.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(
        r'''
        # PART 1: POSITION BETWEEN AN UPPERCASE AND LOWERCASE LETTER
        (?<=                # Preceded by...
            \p{Ll}          # A lowercase letter.
        )
        (?=                 # Followed by...
            \p{Lu}          # An uppercase letter.
        )
        |                   # OR
        # PART 2: POSITION AFTER AN ACRYONYM
        (?<=                # Preceded by...
            \p{Lu}          # An uppercase letter.
        )
        (?=                 # Followed by...
            \p{Lu}\p{Ll}    # An uppercase letter followed by a
                            # lowercase letter.
        )
        |                   # OR
        # PART 3: POSITION BETWEEN A LETTER AND A DIGIT
        (?<=                # Preceded by...
            \p{L}           # A letter.
        )
        (?=                 # Followed by...
            \d              # A digit.
        )
        |                   # OR
        # PART 4: POSITION BETWEEN A DIGIT AND A LETTER
        (?<=                # Preceded by...
            \d              # A digit.
        )
        (?=                 # Followed by...
            \p{L}           # A letter.
        )
        ''',
        re.VERBOSE
    )


@lru_cache(maxsize=1)
def get_split_for_pascal_conversion() -> re.Pattern[str]:
    """
    Get a regular expression for splitting strings into words before
    conversion to Pascal case.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(
        r'''
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
            \p{{L}}[\p{{L}}\d]*         # A letter followed by zero or
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
        ''',
        re.VERBOSE
    )


@lru_cache(maxsize=1)
def get_split_for_separator_conversion() -> re.Pattern[str]:
    """
    Get a regular expression for splitting strings on non-separator word
    boundaries.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(
        r'''
        # WORD BOUNDARY NOT PRECEDED OR FOLLOWED BY A PERIOD OR HYPHEN
        (?<!        # Not preceded by...
            [.\-]   # A period or hyphen.
        )
        \b          # A word boundary.
        (?!         # Not followed by...
            [.\-]   # A period or hyphen.
        )
        ''',
        re.VERBOSE
    )
