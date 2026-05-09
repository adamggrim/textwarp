"""
English-specific functions for converting between straight and curly
quotes.
"""

from textwarp._core.providers import en

__all__ = [
    'curly_to_straight',
    'remove_apostrophes',
    'straight_to_curly'
]


def curly_to_straight(text: str) -> str:
    """
    Convert curly quotes in a given string to straight quotes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    translation_table = str.maketrans({
        # Curly opening single quote to straight single quote
        '‘': "'",
        # Curly closing single quote (or apostrophe) to straight single
        # quote
        '’': "'",
        # Curly opening double quote to straight double quote
        '“': '"',
        # Curly closing double quote to straight double quote
        '”': '"'
    })
    return text.translate(translation_table)


def remove_apostrophes(text: str) -> str:
    """
    Remove apostrophes from a string without removing single quotes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return en.patterns.get_apostrophe_in_word().sub('', text)


def straight_to_curly(text: str) -> str:
    """
    Convert straight quotes in a given string to curly quotes.

    Args:
        text: The string to convert.

    Returns:
        curly_text: The converted string.
    """
    # Convert any straight apostrophes first (contractions, decades or
    # elisions).
    text = en.patterns.get_apostrophe_in_word().sub('’', text)

    chars = list(text)

    for i, char in enumerate(chars):
        if char not in "'\"":
            continue

        prev_char = chars[i - 1] if i else None
        prev_prev_char = chars[i - 2] if i > 1 else None

        is_opening_context = (
            prev_char is None or prev_char in ' \t\n\r([{—–"\u201c\u2018\''
        )
        is_preceded_by_whitespace = (
            prev_char is not None and prev_char in ' \t\n\r'
        )

        if char == "'":
            is_opener = (
                is_opening_context
                or (is_preceded_by_whitespace and prev_prev_char in ('"', '“'))
            )
            chars[i] = '‘' if is_opener else '’'

        elif char == '"':
            # Exception for double quotes preceded by a space and single
            # quote.
            is_opener = (
                is_opening_context
                and not (
                    is_preceded_by_whitespace
                    and prev_prev_char in ("'", '’', '‘')
                )
            )
            chars[i] = '“' if is_opener else '”'

    return ''.join(chars)
