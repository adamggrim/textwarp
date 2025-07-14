import regex as re

from nltk import pos_tag

from textwarp.enums import SeparatorCase
from textwarp.regexes import SeparatorCaseRegexes, WarpingRegexes


class HelperFunctions:
    """Helper functions for text warping."""

    def remove_apostrophes(text: str) -> str:
        """
        Removes apostrophes from a string without removing single
        quotes.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return re.sub(WarpingRegexes.LETTER_APOSTROPHE, '', text)

    def to_separator_case(
            text: str,
            separator_case: SeparatorCase
        ) -> str:
        """
        Converts a string to kebab case or snake case.

        Args:
            text: The string to convert.
            separator: The separator for the converted string.

        Returns:
            str: The converted string.
        """
        def _get_other_separator():
            """
            For a given a separator case, returns the other separator
                character.

            Returns:
                str: The other separator character.
            """
            separator_mapping: dict[SeparatorCase, str] = {
                SeparatorCase.KEBAB: "_",
                SeparatorCase.SNAKE: "-",
            }
            return separator_mapping.get(separator_case)
        other_separator: str | None = _get_other_separator()
        no_apostrophes_text: str = HelperFunctions.remove_apostrophes(text)
        substrings: list[str] = re.split(
            SeparatorCaseRegexes.SEPARATOR_SPLIT,
            no_apostrophes_text
        )
        separator_sub: re.Pattern[str] = re.compile(rf'{other_separator}| ')
        separator_substrings: list[str] = []
        for substring in substrings:
            separator_substring: str
            # Substring is already in a separator case.
            if (SeparatorCaseRegexes.KEBAB_CASE.match(substring) or
                SeparatorCaseRegexes.SNAKE_CASE.match(substring)):
                if substring.isupper():
                    separator_substring = re.sub(
                        separator_sub,
                        separator_case.value,
                        substring
                    )
                else:
                    separator_substring = re.sub(
                        separator_sub,
                        separator_case.value,
                        substring.lower()
                    )
            # Substring is in camel case or Pascal case.
            elif (SeparatorCaseRegexes.CAMEL_CASE.match(substring) or
                SeparatorCaseRegexes.PASCAL_CASE.match(substring)):
                # Break camel case and Pascal case into constituent words.
                broken_words: list[str] = re.split(
                    SeparatorCaseRegexes.CAMEL_PASCAL_SPLIT, substring)
                converted_words: list[str] = []
                for word in broken_words:
                    converted_word = word.lower()
                    converted_words.append(converted_word)
                separator_substring = separator_case.value.join(
                    converted_words
                )
            # Substring is not in any of the above cases.
            else:
                # Substring is in all caps.
                if substring.isupper():
                    separator_substring = substring.replace(' ',
                                                        separator_case.value)
                # Substring begins with an alphabebtical letter.
                elif re.match(WarpingRegexes.LETTER_GROUP, substring):
                    separator_substring = substring.lower().replace(
                        ' ', separator_case.value
                    )
                # Substring does not meet either of the above conditions.
                else:
                    separator_substring = substring
            separator_substrings.append(separator_substring)
        return ''.join(separator_substrings)

    def uppercase_first_letter(text: str) -> str:
        """
        Converts the first letter of the string to uppercase without
        modifying any other letters.

        Args:
            text: The string to convert.

        Returns:
            str: The converted text.
        """
        return re.sub(WarpingRegexes.LETTER_GROUP, lambda match:
                      match.group(0).upper(), text, count=1)


def capitalize(text: str) -> str:
    """
    Capitalizes the first letter of each word, with exceptions for
    certain prefixes and mid-word capitalizations.

    This function considers apostrophes as part of the word. Hyphenated
    words are capitalized after each hyphen.

    Args:
        text: The string to capitalize.

    Returns:
        str: The capitalized string.
    """
    return HelperFunctions.capitalize_words(text)


def cardinal_to_ordinal(text: str) -> str:
    """
    Converts cardinal numbers to ordinal numbers in a given string.

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
    return re.sub(WarpingRegexes.CARDINAL, replace_cardinal, text)


def curly_to_straight(text: str) -> str:
    """
    Converts curly quotes to straight quotes in a given string.

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


def hyphens_to_em(text: str) -> str:
    """
    Converts consecutive hyphens to em dashes in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return re.sub(WarpingRegexes.DOUBLE_HYPHENS, '—', text)


def hyphen_to_en(text: str) -> str:
    """
    Converts hyphens to en dashes in a given string.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return text.replace('-', '–')


def ordinal_to_cardinal(text: str) -> str:
    """
    Converts ordinal numbers to cardinal numbers in a given string.

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
    return re.sub(WarpingRegexes.ORDINAL, replace_ordinal, text)


def punct_to_inside(text: str) -> str:
    """
    Moves periods and commas at the end of quotes inside the quotation
    marks.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    def _repl(match: re.Match) -> str:
        """
        Reorders periods and commas to move them inside quotation marks.

        Args:
            match: A regular expression match object.

        Returns:
            str: The reordered string.
        """
        punct: str
        quote: str
        punct, quote = match.groups()
        return quote + punct
    return re.sub(WarpingRegexes.PUNCT_OUTSIDE, _repl, text)


def punct_to_outside(text: str) -> str:
    """
    Moves periods and commas at the end of quotes to outside the
    quotation marks.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    def _repl(match: re.Match) -> str:
        """
        Reorders periods and commas to move them outside quotation
            marks.

        Args:
            match: A regular expression match object.

        Returns:
            str: The reordered string.
        """
        quote: str
        punct: str
        quote, punct = match.groups()
        return punct + quote
    return re.sub(WarpingRegexes.PUNCT_INSIDE, _repl, text)


def straight_to_curly(text: str) -> str:
    """
    Converts straight quotes to curly quotes in a given string.

    Args:
        text: The string to convert.

    Returns:
        curly_text: The converted string.
    """
    curly_text: str

    # Replace intra-word apostrophes and apostrophes in elisions.
    curly_text = re.sub(WarpingRegexes.APOSTROPHE, "’", text)

    # Replace opening straight quotes with opening curly quotes.
    curly_text = WarpingRegexes.OPENING_STRAIGHT_QUOTES.sub(
        _replace_opening_quote, curly_text
    )

    # Replace any remaining straight single quotes with closing curly
    # single quotes.
    curly_text = curly_text.replace("'", "’")

    # Replace any remaining straight double quotes with closing curly
    # double quotes.
    curly_text = curly_text.replace('"', '”')

    return curly_text


def strikethrough(text: str) -> str:
    """
    Converts a string to the struck-through version.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string, with each input character followed
            by the Unicode strikethrough character (U+0336).
    """
    strikethrough_char: str = '\u0336'

    return ''.join(char + strikethrough_char for char in text)


def to_alternating_caps(text: str) -> str:
    """
    Converts a string to alternating caps.

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
    Converts a string to binary.

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
    Converts a string to camel case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    def _lowercase_first_letter(text) -> str:
        """
        Lowercases the first letter of the string without modifying any
            other letters.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return re.sub(
            WarpingRegexes.FIRST_LETTER, lambda match:
            match.group(0).lower(), text, count=1
        )
    pascal_text: str = to_pascal_case(text)
    # Split between each instance of Pascal case in the string.
    pascal_words: list[str] = re.split(
        WarpingRegexes.CAMEL_SPLIT, pascal_text
    )
    camel_words: list[str] = []
    for word in pascal_words:
        camel_word: str = _lowercase_first_letter(word)
        camel_words.append(camel_word)
    return ''.join(camel_words)


def to_hexadecimal(text: str) -> str:
    """
    Converts a string to hexadecimal.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string in hexadecimal, with each character's
            hex value separated by a space.
    """
    hex_chars: list[str] = [format(ord(char), '02x') for char in text]
    return ' '.join(hex_chars)


def to_kebab_case(text: str) -> str:
    """
    Converts a string to kebab case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return HelperFunctions.to_separator_case(text, SeparatorCase.KEBAB)


def to_lowercase(text: str) -> str:
    """
    Converts a string to lowercase.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return text.lower()


def to_pascal_case(text: str) -> str:
    """
    Converts a string to Pascal case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    no_apostrophes_text: str = HelperFunctions.remove_apostrophes(text)
    words: list[str] = re.split(SeparatorCaseRegexes.PASCAL_SPLIT, no_apostrophes_text)
    pascal_words: list[str] = []
    for word in words:
        pascal_word: str
        # Word is already in Pascal case.
        if SeparatorCaseRegexes.PASCAL_CASE.match(word):
            pascal_word = word
        # Word is an acronym of two characters.
        elif SeparatorCaseRegexes.SHORT_ACRONYM.match(word):
            pascal_word = word
        # Word is in camel case.
        elif SeparatorCaseRegexes.CAMEL_CASE.match(word):
            pascal_word = HelperFunctions.uppercase_first_letter(word)
        # Word is not in Pascal case or camel case.
        else:
            pascal_word = capitalize(word)
        pascal_words.append(pascal_word)
    return ''.join(pascal_words)


def to_sentence_case(text: str) -> str:
    """
    Converts a string to sentence case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return re.sub(
        WarpingRegexes.SENTENCE_START,
        lambda match: match.group(1) + match.group(2).upper(), text
    )


def to_single_spaces(text: str) -> str:
    """
    Converts consecutive spaces to a single space.

    This function preserves leading spaces and tabs.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return re.sub(WarpingRegexes.MULTIPLE_SPACES, ' ', text)


def to_snake_case(text: str) -> str:
    """
    Converts a string to snake case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return HelperFunctions.to_separator_case(text, SeparatorCase.SNAKE)


def to_title_case(text: str) -> str:
    """
    Converts a string to title case.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    def should_capitalize(tag: str) -> bool:
        """
        Determines whether a word should be capitalized based on its
        part of speech.

        Args:
            tag: The NLTK POS tag to check.

        Returns:
            bool: True if the tag should be capitalized, otherwise
                False.
        """
        return tag not in ['CC', 'DT', 'IN', 'RP', 'TO', 'WDT']
    substrings: list[str] = re.split(
        WarpingRegexes.TITLE_SUBSTRING_SPLIT, text
    )
    title_substrings: list[str] = []
    for substring in substrings:
        # Capitalize the first character of the substring.
        title_substring: str = HelperFunctions.uppercase_first_letter(substring)
        # Split the substring into words.
        words: list[str] = re.split(
            WarpingRegexes.TITLE_WORD_SPLIT, title_substring
        )
        all_words: list[str] = []
        # For loop to break camel and Pascal case into constituent words
        for word in words:
            broken_words: list[str] = re.split(
                SeparatorCaseRegexes.CAMEL_PASCAL_SPLIT, word)
            all_words.extend([broken_word for broken_word in broken_words])
        all_words_tags: list[tuple[str, str]] = pos_tag(all_words)
        # Capitalize words based on their part of speech.
        title_words = [
            capitalize(word) if
            should_capitalize(tag) else word for word, tag in all_words_tags
        ]
        title_substring = ' '.join(title_words)
        title_substrings.append(title_substring)
    return ''.join(title_substrings)


def to_uppercase(text: str) -> str:
    """
    Converts a string to uppercase.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    return text.upper()


def _replace_opening_quote(match: re.Match[str]) -> str:
    """
    Converts a sequence of straight quotes to opening curly quotes in a
    given match.

    Args:
        match: A regular expression match object where the first
            captured group is a string of one or more consecutive
            straight quote characters.

    Returns:
        str: A string of opening curly quotes.
    """
    quote_chars: str | None = match.group(1) or match.group(2)
    if quote_chars.startswith("'"):
        return '‘' * len(quote_chars)
    else:
        return '“' * len(quote_chars)


def _capitalize_with_exceptions(word: str) -> str:
    """
    Capitalizes the first letter of a word, handling special name
    prefixes and preserving other mid-word capitalizations.

    Args:
        text: The string to capitalize.

    Returns:
        str: The capitalized word.
    """
    lower_word: str = word.lower()

    if not word or not word[0].isalpha():
        return word

    # Handle al- and el- prefixes, keeping them lowercase.
    if lower_word.startswith(('al-', 'el-')):
        return lower_word[:3] + word[3:].capitalize()

    # Handle Mac prefix.
    if lower_word.startswith('mac'):
        return word[:3].capitalize() + word[3:].capitalize()

    # Handle O', M', L' and Mc prefixes.
    if (re.match(r"^(o|m|l)['‘’]", lower_word)
        or lower_word.startswith('mc')):
        return word[:2].capitalize() + word[2:].capitalize()

    # Handle d' prefix.
    if re.match(r"^d['‘’]", lower_word):
        return lower_word[:2] + word[2:].capitalize()

    # Preserve existing capitalization for words that contain another
    # mid-word capitalization.
    if any(char.isupper() for char in word[1:]):
        return word

    # Otherwise, apply default capitalization.
    return word[0].upper() + word[1:]
