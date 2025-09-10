import random

import regex as re
from spacy.tokens import Doc, Token

from textwarp.config import (
    CONTRACTIONS_MAP,
    INITIALISMS_MAP,
    LOWERCASE_PARTICLES,
    MIXED_CASE_WORDS_MAP,
    MORSE_MAP,
    NAME_PREFIX_EXCEPTIONS,
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
    CasePatterns,
    SeparatorPatterns,
    WarpingPatterns
)
from textwarp.setup import nlp


def capitalize(text: str) -> str:
    """
    Capitalize the first letter of each word, with exceptions for
    certain prefixes and mid-word capitalizations.

    Args:
        text: The string to capitalize.

    Returns:
        str: The capitalized string.
    """
    def _repl(match: re.Match) -> str:
        """
        Helper function to capitalize a matched word, handling special
        name prefixes and preserving other mid-word capitalizations.

        Args:
            match: A match object representing a word found in the
                string.

        Returns:
            str: The capitalized word.
        """
        word = match.group(0)
        # Capitalize each part of a hyphenated word.
        parts = word.split('-')
        return '-'.join(_capitalize_with_exceptions(part) for part in parts)

    return WarpingPatterns.WORD_INCLUDING_PUNCTUATION.sub(_repl, text)


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
        formatted_number: str = (
            f'{number:,}' if ',' in number_str else str(number)
        )
        return f'{formatted_number}{suffix}'
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
        normalized_contraction = curly_to_straight(contraction).lower()
        expanded_contraction = CONTRACTIONS_MAP.get(
            normalized_contraction, contraction
        )
        return _apply_casing(contraction, expanded_contraction)

    # If there are no ambiguous contractions, spaCy isn't needed.
    if not WarpingPatterns.AMBIGUOUS_CONTRACTION_PATTERN.search(text):
        def _simple_repl(match: re.Match[str]) -> str:
            return _repl_from_dict(match.group(0))
        return WarpingPatterns.CONTRACTION.sub(_simple_repl, text)

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
                token_text = token_map[i].text
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
            base_word_token = doc[apostrophe_token.i - 1]

            # Combine the base word with the expanded suffix.
            full_expansion = f'{base_word_token.text} {expanded_suffix}'

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
    words = text.strip().split('   ')
    decoded_words = []
    for word in words:
        char_codes = word.split(' ')
        decoded_word = ''.join(
            REVERSED_MORSE_MAP.get(code, '') for code in char_codes
        )
        decoded_words.append(decoded_word)
    return ' '.join(decoded_words)


def hyphens_to_em(text: str) -> str:
    """
    Convert consecutive hyphens to em dashes in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return WarpingPatterns.DOUBLE_HYPHENS.sub('—', text)


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
    def replace_ordinal(match):
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
    def _repl(match: re.Match) -> str:
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
    def _repl(match: re.Match) -> str:
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
    Randomize the characters in each word of a given string.

    Args:
        text: The string to randomize.

    Returns:
        str: The randomized string.
    """
    def _repl(_):
        return next(randomized_iter)

    words = WarpingPatterns.WORD_CHARACTERS.findall(text)

    randomized_words = []
    for word in words:
        chars = list(word)
        random.shuffle(chars)
        randomized_words.append(''.join(chars))

    randomized_iter = iter(randomized_words)
    return WarpingPatterns.WORD_CHARACTERS.sub(_repl, text)


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


def reverse(text):
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
    curly_text = WarpingPatterns.APOSTROPHE_IN_WORD.sub("’", text)

    # Replace opening straight quotes with opening curly quotes.
    curly_text = WarpingPatterns.OPENING_STRAIGHT_QUOTES.sub(
        _replace_opening_quote, curly_text
    )

    # Replace any remaining straight single quotes with closing curly
    # single quotes.
    curly_text = curly_text.replace("'", "’")

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
    return CasePatterns.PASCAL_WORD.sub(
        lambda m: _lowercase_first_letter(m.group(0)),
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
    straight_text = curly_to_straight(text)
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
        hyphenated_text = WarpingPatterns.DASH.sub('-', straight_text)
        return hyphenated_text.replace('…', '...')

    normalized_text: str = _normalize_for_morse(text)

    morse_words = (
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
    words: list[str] = SeparatorPatterns.SPLIT_FOR_PASCAL.split(
        no_apostrophes_text
    )
    pascal_substrings: list[str] = []

    for word in words:
        pascal_word: str
        if not any(char.isalpha() for char in word):
            pascal_substrings.append(word)
            continue
        # Word is in Pascal case.
        elif CasePatterns.PASCAL_WORD.match(word):
            pascal_word = word
        # Word is in camel case.
        elif CasePatterns.CAMEL_WORD.match(word):
            pascal_word = _uppercase_first_letter(word)
        # Word is not in Pascal or camel case.
        else:
            pascal_word = _capitalize_with_exceptions(word)
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
    return WarpingPatterns.FIRST_WORD_IN_SENTENCE.sub(
        lambda m: _capitalize_with_exceptions(m.group(0)), text
    )


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
    return _to_separator_case(
        text, SeparatorPatterns.SNAKE_CASE
    )


def to_title_case(text: str) -> str:
    """
    Convert a string to title case, with exceptions for certain
    prefixes and mid-word capitalizations.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    def _should_capitalize(token: Token) -> bool:
        """
        Determine whether a word should be capitalized based on its
        part of speech.

        Args:
            tag: The spaCy POS tag to check.

        Returns:
            bool: True if the tag should be capitalized, otherwise
                False.
        """
        if token.text.lower() in LOWERCASE_PARTICLES:
            return False

        # Capitalize long words regardless of POS tags.
        if len(token.text) >= 5:
            return True

        tags_to_exclude: set[str] = {
            'CC',   # Coordinating conjunction (e.g., 'and', 'but')
            'DT',   # Determiner (e.g., 'a', 'an', 'the')
            'IN',   # Preposition or subordinating conjunction
                    # (e.g., 'in', 'of', 'on')
            'RP',   # Particle (e.g., 'in' in 'give in')
            'TO',   # to (infinitive marker)
            'WDT',  # Wh-determiner (e.g., 'what')
        }

        return token.tag_ not in tags_to_exclude

    doc: Doc = nlp(text)

    # Find the index of the first non-whitespace token in each
    # sentence and after any colon.
    first_word_indices: set[int] = set()
    last_word_index: int = -1

    for i, token in enumerate(doc):
        if token.is_sent_start:
            for sent_token in token.sent:
                if not sent_token.is_space and not sent_token.is_punct:
                    first_word_indices.add(sent_token.i)
                    break
        if token.text == ":" and i + 1 < len(doc):
            # Find the index of the next non-space token.
            for j in range(i + 1, len(doc)):
                if not doc[j].is_space and not doc[j].is_punct:
                    first_word_indices.add(j)
                    break
        # Find the index of the last non-whitespace, non-punctuation
        # token.
        if not token.is_space and not token.is_punct:
            last_word_index = i

    title_case_tokens: list[str] = []

    for i, token in enumerate(doc):
        # Preserve the token if it contains only whitespace.
        if token.is_space:
            cased_token = token.text
        # Preserve the token if it is in the contraction suffixes list.
        elif WarpingPatterns.CONTRACTION_SUFFIX_PATTERN.fullmatch(token.text):
            cased_token = token.text
        # Capitalize the first token in the title or subtitle.
        elif i in first_word_indices:
            cased_token = _capitalize_with_exceptions(token.text)
        # Capitalize the last word of the title.
        elif i == last_word_index:
            cased_token = _capitalize_with_exceptions(token.text)
        # Capitalize the word based on its POS tag and length.
        elif _should_capitalize(token):
            cased_token = _capitalize_with_exceptions(token.text)
        # Otherwise, lowercase the word.
        else:
            cased_token = token.text.lower()

        # Add back trailing whitespace.
        title_case_tokens.append(cased_token + token.whitespace_)

    return ''.join(title_case_tokens)


def _capitalize_with_exceptions(word: str) -> str:
    """
    Capitalize a word, handling special name prefixes and preserving
    other mid-word capitalizations.

    Args:
        word: The word to capitalize.

    Returns:
        str: The capitalized word.
    """
    if not word or not word[0].isalpha():
        return word

    lower_word: str = word.lower()

    capitalization_strategies = [
        _handle_mixed_case_word,
        _handle_period_separated_initialism,
        _handle_initialism,
        _handle_prefixed_name,
        _preserve_existing_capitalization,
    ]

    for strategy in capitalization_strategies:
        result = strategy(word, lower_word)
        if result is not None:
            return result

    return word.capitalize()


def _handle_mixed_case_word(_word: str, lower_word: str) -> str | None:
    """
    Handle mixed-case capitalization.

    Args:
        _word: The word to capitalize (unused).
        lower_word: The lowercase word.

    Returns:
        str | None: The mixed-case word, or None if lower_word is
            not in MIXED_CASE_WORDS_MAP.
    """
    return MIXED_CASE_WORDS_MAP.get(lower_word)


def _handle_period_separated_initialism(
    _word: str,
    lower_word: str
) -> str | None:
    """
    Handle period-separated initialisms.

    Args:
        _word: The word to capitalize (unused).
        lower_word: The lowercase word.

    Returns:
        str | None: The capitalized initialism, or None if the
            word does not contain a period.
    """
    if '.' in lower_word:
        # Filter empty strings that can result from a trailing
        # period.
        parts = list(filter(None, lower_word.split('.')))
        # Capitalize each part.
        return '.'.join(part.capitalize() for part in parts)
    return None


def _handle_initialism(_word: str, lower_word: str) -> str | None:
    """
    Handle initialisms without periods.

    Args:
        _word: The word to capitalize (unused).
        lower_word: The lowercase word.

    Returns:
        str | None: The capitalized initialism, or None if not in
            INITIALISMS_MAP.
    """
    return INITIALISMS_MAP.get(lower_word)


def _handle_prefixed_name(word: str, lower_word: str) -> str | None:
    """
    Handle prefixed names.

    Args:
        word: The word to capitalize.
        lower_word: The lowercase word.

    Returns:
        str | None: The capitalized name, or None if the
            string starts with a name prefix exception.
    """
    if lower_word.startswith(NAME_PREFIX_EXCEPTIONS):
        return None
    if (match := WarpingPatterns.NAME_PREFIX_PATTERN.match(word)):
        prefix_len = len(match.group(0))
        return (word[:prefix_len].capitalize() +
                word[prefix_len:].capitalize())
    return None


def _lowercase_first_letter(text: str) -> str:
    """
    Convert the first letter of the string to lowercase without
    modifying any other letters.

    Args:
        text: The string to convert.

    Returns:
        str: The converted text.
    """
    for i, char in enumerate(text):
        if char.isalpha():
            # Lowercase the first letter and return the new text.
            return text[:i] + char.lower() + text[i+1:]
    # Return the original text if no letters were in the string.
    return text


def _preserve_existing_capitalization(word: str, _lower_word: str) -> str:
    """
    Preserve words that are already mixed-case.

    Args:
        word: The word to check.
        _lower_word: The lowercase word.

    Returns:
        str: The original word, or None if the word is all
            lowercase or uppercase.
    """
    if not word.islower() and not word.isupper():
        return word
    return None


def _remove_apostrophes(text: str) -> str:
    """
    Remove apostrophes from a string without removing single
    quotes.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return SeparatorPatterns.APOSTROPHE_IN_WORD.sub('', text)


def _replace_opening_quote(match: re.Match[str]) -> str:
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


def _uppercase_first_letter(text: str) -> str:
    """
    Convert the first letter of the string to uppercase without
    modifying any other letters.

    Args:
        text: The string to convert.

    Returns:
        str: The converted text.
    """
    for i, char in enumerate(text):
        if char.isalpha():
            # Uppercase the first letter and return the new text.
            return text[:i] + char.upper() + text[i+1:]
    # Return the original text if no letters were in the string.
    return text


def _to_separator_case(
    text: str,
    separator: CaseSeparator
) -> str:
    """
    Convert a string to dot case, kebab case or snake case.

    Args:
        text: The string to convert.
        separator: The separator for the converted string.

    Returns:
        str: The converted string.
    """
    def _get_other_separator():
        """
        For a given a separator case, return the other separator
        character.

        Returns:
            str: The other separator character.
        """
        separator_mapping: dict[CaseSeparator, str] = {
            CaseSeparator.KEBAB: "_",
            CaseSeparator.SNAKE: "-",
        }
        return separator_mapping.get(separator)
    other_separator: str | None = _get_other_separator()
    no_apostrophes_text: str = _remove_apostrophes(text)
    substrings: list[str] = SeparatorPatterns.SEPARATOR_SPLIT.split(
        no_apostrophes_text
    )
    separator_sub: re.Pattern[str] = re.compile(rf'{other_separator}| ')
    separator_substrings: list[str] = []
    for substring in substrings:
        separator_substring: str
        # Substring is already in a separator case.
        if (SeparatorPatterns.KEBAB_CASE.match(substring) or
            SeparatorPatterns.SNAKE_CASE.match(substring)):
            if substring.isupper():
                separator_substring = separator_sub.sub(
                    separator.value, substring
                )
            else:
                separator_sub.sub(separator.value, substring.lower())
        # Substring is in camel case or Pascal case.
        elif (CasePatterns.CAMEL_WORD.match(substring) or
            CasePatterns.PASCAL_WORD.match(substring)):
            # Break camel case and Pascal case into constituent words.
            broken_words: list[str] = (
                SeparatorPatterns.CAMEL_PASCAL_SPLIT.split(substring)
            )
            converted_words: list[str] = []
            for word in broken_words:
                converted_word = word.lower()
                converted_words.append(converted_word)
            separator_substring = separator.value.join(
                converted_words
            )
        # Substring is not in any of the above cases.
        else:
            # Substring is in all caps.
            if substring.isupper():
                separator_substring = substring.replace(
                    ' ', separator.value
                )
            # Substring begins with an alphabebtical letter.
            elif SeparatorPatterns.LETTER.match(substring):
                separator_substring = substring.lower().replace(
                    ' ', separator.value
                )
            # Substring does not meet either of the above conditions.
            else:
                separator_substring = substring
        separator_substrings.append(separator_substring)
    return ''.join(separator_substrings)
