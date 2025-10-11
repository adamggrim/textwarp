import regex as re

from textwarp.regexes import WarpingPatterns


def remove_apostrophes(text: str) -> str:
    """
    Remove apostrophes from a string without removing single quotes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return WarpingPatterns.APOSTROPHE_IN_WORD.sub('', text)


def replace_opening_quote(match: re.Match[str]) -> str:
    """
    Convert a sequence of straight quotes to opening curly quotes in a
    given match.

    Args:
        match: A match object where the first captured group is a
            string of one or more consecutive straight quote
            characters.

    Returns:
        str: A string of opening curly quotes.
    """
    quote_chars: str | None = match.group(1) or match.group(2)
    if quote_chars.startswith("'"):
        return '‘' * len(quote_chars)
    else:
        return '“' * len(quote_chars)
