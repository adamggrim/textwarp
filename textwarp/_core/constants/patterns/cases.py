"""Universal regular expressions for identifying cases."""

from functools import lru_cache

import regex as re

__all__ = [
    'get_camel_word',
    'get_dot_word',
    'get_kebab_word',
    'get_lower_word',
    'get_pascal_word',
    'get_snake_word',
    'get_upper_word'
]


@lru_cache(maxsize=1)
def get_camel_word() -> re.Pattern[str]:
    """
    Get a regular expression matching any camel case word.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'\b\p{Ll}[\p{Ll}\d]*\p{Lu}[\p{L}\d]*\b')


@lru_cache(maxsize=1)
def get_dot_word() -> re.Pattern[str]:
    """
    Get a regular expression matching a dot case word.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'\b\p{L}[\p{L}\d]*(?:\.[\p{L}\d]+)+\b')


@lru_cache(maxsize=1)
def get_kebab_word() -> re.Pattern[str]:
    """
    Get a regular expression matching a kebab case word.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'\b\p{L}[\p{L}\d]*(?:\-[\p{L}\d]+)+\b')


@lru_cache(maxsize=1)
def get_lower_word() -> re.Pattern[str]:
    """
    Get a regular expression matching a lowercase word and any optional
    separators.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(
        r'''
        \b                  # A word boundary.
        (?=                 # Followed by...
            [\d.\-_]*       # Zero or more digits or separators.
            \p{Ll}          # And a lowercase letter.
        )
        [\p{Ll}\d.\-_]+     # One or more lowercase letters, digits or
                            # separators.
        \b                  # Followed by a word boundary.
        ''',
        re.VERBOSE
    )


@lru_cache(maxsize=1)
def get_pascal_word() -> re.Pattern[str]:
    """
    Get a regular expression matching a Pascal case word.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'\b\p{Lu}[\p{Lu}\d]*\p{Ll}[\p{L}\d]*\b')


@lru_cache(maxsize=1)
def get_snake_word() -> re.Pattern[str]:
    """
    Get a regular expression matching a snake case word.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(r'\b_?\p{L}[\p{L}\d]*(?:_[\p{L}\d]+)+\b')


@lru_cache(maxsize=1)
def get_upper_word() -> re.Pattern[str]:
    """
    Get a regular expression matching an uppercase word and any optional
    separators.

    Returns:
        re.Pattern[str]: A compiled regular expression pattern.
    """
    return re.compile(
        r'''
        \b                  # A word boundary.
        (?=                 # Followed by...
            [\d.\-_]*       # Zero or more digits or separators.
            \p{Lu}          # And an uppercase letter.
        )
        [\p{Lu}\d.\-_]+     # One or more uppercase letters, digits or
                            # separators.
        \b                  # Followed by a word boundary.
        ''',
        re.VERBOSE
    )
