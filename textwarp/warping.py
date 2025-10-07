import random
from collections.abc import Generator

import regex as re
from spacy.tokens import Doc, Token

from textwarp.enums import Casing
from textwarp._helpers import (
    _capitalize_from_string,
    _change_first_letter_case,
    _remove_apostrophes,
    _replace_opening_quote,
    _to_case_from_doc,
    _to_separator_case
)
from textwarp.config import (
    CONTRACTIONS_MAP,
    MORSE_MAP,
    REVERSED_MORSE_MAP
)
from textwarp.constants import (
    APOSTROPHE_D_VARIANTS,
    APOSTROPHE_S_VARIANTS,
    APOSTROPHE_VARIANTS,
    PAST_PARTICIPLE_TAGS
)
from textwarp.enums import CaseSeparator
from textwarp.regexes import (
    ProgrammingCasePatterns,
    WarpingPatterns
)
from textwarp.setup import nlp


def capitalize(text: str) -> str:
    """
    Capitalize the first letter of each word, handling special name
    prefixes and preserving other mid-word capitalizations.

    Args:
        text: The string to capitalize.

    Returns:
        str: The capitalized string.
    """
    doc: Doc = nlp(text)
    capitalized_tokens: list[str] = []
    capitalized_token: str

    for token in doc:
        # Preserve the token if it contains only whitespace or is in
        # the contraction suffixes list.
        if token.is_space or (
            WarpingPatterns.CONTRACTION_SUFFIX_TOKENS_PATTERN
            .fullmatch(token.text)
        ):
            capitalized_token = token.text
        else:
            capitalized_token = _capitalize_from_string(token.text)

        # Add back trailing whitespace.
        capitalized_tokens.append(capitalized_token + token.whitespace_)

    return ''.join(capitalized_tokens)


def cardinal_to_ordinal(text: str) -> str:
    """
    Convert cardinal numbers to ordinal numbers in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    def replace_cardinal(match: re.Match[str]) -> str:
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

    return WarpingPatterns.CARDINAL.sub(replace_cardinal, text)


def curly_to_straight(text: str) -> str:
    """
    Convert curly quotes to straight quotes in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    translation_table: dict[int, str] = str.maketrans({
        # Curly opening single quotes to straight single quotes
        '’': "'",
        # Curly opening double quotes to straight double quotes
        '”': '"',
        # Curly closing single quotes to straight single quotes
        '‘': "'",
        # Curly closing double quotes to straight double quotes
        '“': '"'
    })
    return text.translate(translation_table)


def expand_contractions(text: str) -> str:
    """
    Expand contractions in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    def _apply_casing(original_word: str, expanded_word: str) -> str:
        """
        Apply the casing of the original word to the expanded word.

        Args:
            original_word: The original word.
            expanded_word: The new word to which the casing should be
                applied.

        Returns:
            str: The expanded word in the original word's casing.
        """
        if original_word.isupper():
            return expanded_word.upper()
        elif original_word.istitle():
            return expanded_word.capitalize()
        return expanded_word

    def _repl_from_dict(contraction: str) -> str:
        """
        Replace a contraction using the contractions map.

        Args:
            contraction: The contraction to expand.

        Returns:
            str: The expanded contraction.
        """
        normalized_contraction: str = curly_to_straight(contraction).lower()
        expanded_contraction: str = CONTRACTIONS_MAP.get(
            normalized_contraction, contraction
        )
        return _apply_casing(contraction, expanded_contraction)

    # If there are no ambiguous contractions, spaCy isn't needed.
    if not WarpingPatterns.AMBIGUOUS_CONTRACTION_PATTERN.search(text):
        return WarpingPatterns.CONTRACTION.sub(
        lambda match: _repl_from_dict(match.group(0)), text
    )

    doc: Doc = nlp(text)
    token_map: dict[int, Token] = {token.idx: token for token in doc}

    def _repl(match: re.Match[str]) -> str:
        """
        Helper function to replace a matched contraction with its
        expanded version.

        This function uses spaCy to disambiguate certain contractions
        based on the part of speech of the following word.

        Args:
            match: A match object representing a contraction.

        Returns:
            str: The expanded version of the matched contraction.
        """
        contraction: str = match.group(0)
        start_char_index: int = match.start()

        apostrophe_token: Token | None = None

        for i in range(start_char_index, match.end()):
            if i in token_map:
                token_text: str = token_map[i].text
                if any(char in token_text for char in APOSTROPHE_VARIANTS):
                    apostrophe_token = token_map[i]
                    break

        expanded_suffix: str = ''

        if apostrophe_token and apostrophe_token.i + 1 < len(doc):
            next_token: Token = doc[apostrophe_token.i + 1]
            # Disambiguate 's: "is" vs. "has"
            if apostrophe_token.lower_ in APOSTROPHE_S_VARIANTS:
                if next_token.tag_ in PAST_PARTICIPLE_TAGS:
                    expanded_suffix = 'has'
                else:
                    expanded_suffix = 'is'
            # Disambiguate 'd: "would" vs. "had"
            elif apostrophe_token.lower_ in APOSTROPHE_D_VARIANTS:
                if next_token.tag_ in PAST_PARTICIPLE_TAGS:
                    expanded_suffix = 'had'
                else:
                    expanded_suffix = 'would'
        if expanded_suffix:
            base_word_token: Token = doc[apostrophe_token.i - 1]

            # Combine the base word with the expanded suffix.
            full_expansion: str = f'{base_word_token.text} {expanded_suffix}'

            return _apply_casing(contraction, full_expansion)

        # Fallback to contractions map.
        return _repl_from_dict(contraction)

    return WarpingPatterns.CONTRACTION.sub(_repl, text)


def from_hexadecimal(text: str) -> str:
    """
    Convert a given string from hexadecimal.

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
    Convert a given string from Morse code.

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
    def replace_ordinal(match: re.Match[str]) -> str:
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

    return WarpingPatterns.ORDINAL.sub(replace_ordinal, text)


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
    random.shuffle(char_list)
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


def straight_to_curly(text: str) -> str:
    """
    Convert straight quotes to curly quotes in a given string.

    Args:
        text: The string to convert.

    Returns:
        curly_text: The converted string.
    """
    curly_text: str

    # Replace intra-word apostrophes and apostrophes in elisions.
    curly_text = WarpingPatterns.APOSTROPHE_IN_WORD.sub('’', text)

    # Replace opening straight quotes with opening curly quotes.
    curly_text = WarpingPatterns.OPENING_STRAIGHT_QUOTES.sub(
        _replace_opening_quote, curly_text
    )

    # Replace any remaining straight single quotes with closing curly
    # single quotes.
    curly_text = curly_text.replace("'", '’')

    # Replace any remaining straight double quotes with closing curly
    # double quotes.
    curly_text = curly_text.replace('"', '”')

    return curly_text


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
    binary_chars: list [str] = [format(ord(char), '08b') for char in text]
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
        lambda m: _change_first_letter_case(m.group(0), str.lower),
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
    return _to_separator_case(text, CaseSeparator.DOT)


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
    return _to_separator_case(text, CaseSeparator.KEBAB)


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
    no_apostrophes_text: str = _remove_apostrophes(text)
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
            pascal_word = _change_first_letter_case(w, str.upper)
        # Word is not in Pascal or camel case.
        else:
            pascal_word = _capitalize_from_string(w)
        pascal_substrings.append(pascal_word)

    return ''.join(pascal_substrings)


def to_sentence_case(text: str) -> str:
    """
    Convert a string to sentence case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    doc: Doc = nlp(text)
    return _to_case_from_doc(doc, Casing.SENTENCE)


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
    return _to_separator_case(text, CaseSeparator.SNAKE)


def to_title_case(text: str) -> str:
    """
    Convert a string to title case, handling special name prefixes and
    preserving other mid-word capitalizations.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    doc: Doc = nlp(text)
    return _to_case_from_doc(doc, Casing.TITLE)
