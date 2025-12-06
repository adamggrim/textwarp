from collections.abc import Generator
from random import (
    choice,
    shuffle
)

import regex as re
from spacy.tokens import Doc

from ._enums import Casing
from ._helpers import (
    capitalize_from_string,
    change_first_letter_case,
    curly_to_straight,
    expand_contractions_from_doc,
    doc_to_case,
    process_as_doc,
    remove_apostrophes,
    straight_to_curly,
    to_separator_case
)
from ._config import (
    MORSE_MAP,
    REVERSED_MORSE_MAP
)
from ._enums import CaseSeparator
from ._regexes import (
    ProgrammingCasePatterns,
    WarpingPatterns
)
from ._nlp import nlp

__all__ = [
    'capitalize',
    'cardinal_to_ordinal',
    'curly_to_straight',
    'expand_contractions',
    'from_binary',
    'from_hexadecimal',
    'from_morse',
    'hyphens_to_em',
    'hyphen_to_en',
    'ordinal_to_cardinal',
    'punct_to_inside',
    'punct_to_outside',
    'random_case',
    'randomize',
    'redact',
    'reverse',
    'straight_to_curly',
    'to_alternating_caps',
    'to_binary',
    'to_camel_case',
    'to_dot_case',
    'to_hexadecimal',
    'to_kebab_case',
    'to_morse',
    'to_pascal_case',
    'to_sentence_case',
    'to_single_spaces',
    'to_snake_case',
    'to_title_case',
    'widen'
]


def capitalize(content: str | Doc) -> str:
    """
    Capitalize the each word in a given string or spaCy ``Doc``,
    handling special name prefixes and preserving other mid-word
    capitalizations.

    Args:
        content: The string or spaCy ``Doc`` to capitalize.

    Returns:
        str: The capitalized string.
    """
    doc: Doc = process_as_doc(content)
    return doc_to_case(doc, Casing.START)


def cardinal_to_ordinal(text: str) -> str:
    """
    Convert cardinal numbers to ordinal numbers in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    def _replace_cardinal(match: re.Match[str]) -> str:
        """
        Helper function to replace a matched cardinal number with an
        ordinal.

        Args:
            match: A match object representing a cardinal
                number found in the string.

        Returns:
            str: The ordinal version of the matched cardinal.
        """
        number_str: str = match.group(0)
        number: int = int(number_str.replace(',', ''))
        suffix: str

        if 10 <= number % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')

        return number_str + suffix

    return WarpingPatterns.CARDINAL.sub(_replace_cardinal, text)


def expand_contractions(content: str | Doc) -> str:
    """
    Expand all contractions in a given string or spaCy ``Doc``.

    Args:
        content: The string or spaCy ``Doc`` to convert.

    Returns:
        str: The converted string.
    """
    doc: Doc = process_as_doc(content)
    return expand_contractions_from_doc(doc)


def from_binary(binary_text: str) -> str:
    """
    Convert a string from binary.

    Args:
        binary_text: The space-separated binary string to convert.

    Returns:
        str: The converted string.
    """
    binary_chars: list[str] = binary_text.split(' ')
    decoded_chars: list[str] = [chr(int(binary, 2)) for binary in binary_chars]
    return ''.join(decoded_chars)


def from_hexadecimal(text: str) -> str:
    """
    Convert a string from hexadecimal.

    Args:
        text: The hexadecimal string to convert.

    Returns:
        str: The converted string.
    """
    chars: list[str] = [
        chr(int(hex_char, 16)) for hex_char in text.split(' ')
    ]
    return ''.join(chars)


def from_morse(text: str) -> str:
    """
    Convert a string from Morse code.

    Args:
        text: The Morse string to convert.

    Returns:
        str: The converted string (in uppercase).
    """
    words: list[str] = text.strip().split('   ')
    decoded_words: list[str] = []

    for w in words:
        char_codes: list[str] = w.split(' ')
        decoded_word: str = ''.join(
            REVERSED_MORSE_MAP.get(code, '') for code in char_codes
        )
        decoded_words.append(decoded_word)

    return ' '.join(decoded_words)


def hyphens_to_em(text: str) -> str:
    """
    Convert em dash stand-ins to em dashes in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return WarpingPatterns.EM_DASH_STAND_IN.sub('—', text)


def hyphen_to_en(text: str) -> str:
    """
    Convert hyphens to en dashes in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return text.replace('-', '–')


def ordinal_to_cardinal(text: str) -> str:
    """
    Convert ordinal numbers to cardinal numbers in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    def _replace_ordinal(match: re.Match[str]) -> str:
        """
        Helper function to replace a matched ordinal number with its
        cardinal equivalent.

        Args:
            match: A match object representing an ordinal number found
                in the string.

        Returns:
            str: The cardinal version of the matched ordinal.
        """
        ordinal: str = match.group(0)
        return ordinal[:-2]

    return WarpingPatterns.ORDINAL.sub(_replace_ordinal, text)


def punct_to_inside(text: str) -> str:
    """
    Move periods and commas at the end of quotes inside quotation
    marks.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    def _repl(match: re.Match[str]) -> str:
        """
        Reorder periods and commas to move them inside quotation marks.

        Args:
            match: A match object.

        Returns:
            str: The reordered string.
        """
        punct: str
        quote: str
        punct, quote = match.groups()
        return quote + punct

    return WarpingPatterns.PUNCT_OUTSIDE.sub(_repl, text)


def punct_to_outside(text: str) -> str:
    """
    Move periods and commas at the end of quotes to outside quotation
    marks.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    def _repl(match: re.Match[str]) -> str:
        """
        Reorder periods and commas to move them outside quotation
        marks.

        Args:
            match: A match object.

        Returns:
            str: The reordered string.
        """
        quote: str
        punct: str
        quote, punct = match.groups()
        return punct + quote

    return WarpingPatterns.PUNCT_INSIDE.sub(_repl, text)

def random_case(text: str) -> str:
    """
    Randomize the casing of each character in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    result: list[str] = []

    for char in text:
        if char.isalpha():
            if choice([True, False]):
                result.append(char.upper())
            else:
                result.append(char.lower())
        else:
            result.append(char)

    return ''.join(result)


def randomize(text: str) -> str:
    """
    Randomize the characters of a given string.

    Args:
        text: The string to randomize.

    Returns:
        str: The randomized string.
    """
    # Convert the string into a list of characters.
    char_list: list[str] = list(text)
    shuffle(char_list)
    return ''.join(char_list)


def redact(text: str) -> str:
    """
    Redact a string by replacing each word character with a black
    square.

    Args:
        text: The string to redact.

    Returns:
        str: The redacted string.
    """
    return WarpingPatterns.WORD_CHARACTER.sub('█', text)


def reverse(text: str) -> str:
    """
    Reverses the characters of a given string.

    Args:
        text: The string to reverse.

    Returns:
        The reversed string.
    """
    return text[::-1]


def to_alternating_caps(text: str) -> str:
    """
    Convert a string to alternating caps.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    result: list[str] = []
    # Toggle switch for alternating caps effect.
    upper: bool = False

    for char in text:
        if char.isalpha():
            if upper:
                result.append(char.upper())
            else:
                result.append(char.lower())
            upper = not upper
        else:
            result.append(char)

    return ''.join(result)


def to_binary(text: str) -> str:
    """
    Convert a string to binary.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string in binary, with each character's
            binary value separated by a space.
    """
    binary_chars: list[str] = [format(ord(char), '08b') for char in text]
    return ' '.join(binary_chars)


def to_camel_case(text: str) -> str:
    """
    Convert a string to camel case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    pascal_text: str = to_pascal_case(text)
    return ProgrammingCasePatterns.PASCAL_WORD.sub(
        lambda m: change_first_letter_case(m.group(0), str.lower),
        pascal_text
    )


def to_dot_case(text: str) -> str:
    """
    Convert a string to dot case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return to_separator_case(text, CaseSeparator.DOT)


def to_hexadecimal(text: str) -> str:
    """
    Convert a string to hexadecimal.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string in hexadecimal, with each character's
            hex value separated by a space.
    """
    straight_text: str = curly_to_straight(text)
    hex_chars: list[str] = [
        format(ord(char), '02x') for char in straight_text
    ]
    return ' '.join(hex_chars)


def to_kebab_case(text: str) -> str:
    """
    Convert a string to kebab case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return to_separator_case(text, CaseSeparator.KEBAB)


def to_morse(text: str) -> str:
    """
    Convert a given string to Morse code.

    Letters (A-Z), numbers (0-9) and common punctuation (., ?, !, ,, :,
    ;, +, -, =, @, (, ), ", ', /, &) are all supported.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string, with a single space between
            character codes and three spaces between word codes.
    """
    def _normalize_for_morse(text: str) -> str:
        """
        Normalize a string for Morse code by converting to
        uppercase and replacing non-Morse-compatible characters.

        Args:
            text: The string to normalize.

        Returns:
            str: The normalized string.
        """
        straight_text: str = curly_to_straight(text.upper())
        hyphenated_text: str = WarpingPatterns.DASH.sub('-', straight_text)
        return hyphenated_text.replace('…', '...')

    normalized_text: str = _normalize_for_morse(text)

    morse_words: Generator[str, None, None] = (
        ' '.join(MORSE_MAP[char] for char in word if char in MORSE_MAP)
        for word in normalized_text.split()
    )

    return '   '.join(filter(None, morse_words))


def to_pascal_case(text: str) -> str:
    """
    Convert a string to Pascal case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    no_apostrophes_text: str = remove_apostrophes(text)
    words: list[str] = (
        ProgrammingCasePatterns.SPLIT_FOR_PASCAL_CONVERSION.split(
            no_apostrophes_text
        )
    )
    pascal_substrings: list[str] = []

    for w in words:
        pascal_word: str
        if not any(char.isalpha() for char in w):
            pascal_substrings.append(w)
            continue
        # Word is already in Pascal case.
        elif ProgrammingCasePatterns.PASCAL_WORD.match(w):
            pascal_word = w
        # Word is in camel case.
        elif ProgrammingCasePatterns.CAMEL_WORD.match(w):
            pascal_word = change_first_letter_case(w, str.upper)
        # Word is not in Pascal or camel case.
        else:
            pascal_word = capitalize_from_string(w)
        pascal_substrings.append(pascal_word)

    return ''.join(pascal_substrings)


def to_sentence_case(content: str | Doc) -> str:
    """
    Convert a string or spaCy ``Doc`` to sentence case.

    Args:
        content: The string or spaCy ``Doc`` to convert.

    Returns:
        str: The converted string.
    """
    doc: Doc = process_as_doc(content)
    return doc_to_case(doc, Casing.SENTENCE)


def to_single_spaces(text: str) -> str:
    """
    Convert consecutive spaces to a single space.

    This function preserves leading spaces and tabs.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return WarpingPatterns.MULTIPLE_SPACES.sub(' ', text)


def to_snake_case(text: str) -> str:
    """
    Convert a string to snake case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return to_separator_case(text, CaseSeparator.SNAKE)


def to_title_case(content: str | Doc) -> str:
    """
    Convert a string or spaCy ``Doc`` to title case, handling special
    name prefixes and preserving other mid-word capitalizations.

    Args:
        content: The string or spaCy ``Doc`` to convert.

    Returns:
        str: The converted string.
    """
    doc: Doc = process_as_doc(content)
    return doc_to_case(doc, Casing.TITLE)


def widen(text: str) -> str:
    """
    Widen a string by adding a space after each character except
    the last one.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return ' '.join(text)
