import re
from typing import Optional

from nltk import pos_tag

from textwarp.enums import SeparatorCase
from textwarp.regexes import SeparatorCaseRegexes, WarpingRegexes


class HelperFunctions:
    """Helper functions for text warping."""

    def capitalize_words(string: str, word_count: Optional[int] = None) -> str:
            """
            Capitalizes the first letter of each in a specified number 
                of words and converts all other letters in each word to 
                lowercase.

            Args:
                string (str): The string to capitalize.
                count (int): The number of matches to replace.

            Returns:
                str: The capitalized string.
            """
            # Capitalize the first letter of every word.
            if word_count is None:
                return re.sub(WarpingRegexes.LETTER_WORD, lambda match: 
                              match.group(0).capitalize(), string)
            # Capitalize the first letter of a specified number of words.
            else:
                return re.sub(WarpingRegexes.LETTER_WORD, lambda match: 
                              match.group(0).capitalize(), string, 
                              count=word_count)

    def remove_apostrophes(string: str) -> str:
        """
        Removes apostrophes from a string without removing single 
            quotes.

        Args:
            string (str): The string to convert.

        Returns:
            str: The converted string.
        """
        return re.sub(WarpingRegexes.LETTER_APOSTROPHE, '', string)

    def to_separator_case(string: str, separator_case: SeparatorCase) -> str:
        """
        Converts a string to kebab case or snake case.

        Args:
            string (str): The string to convert.
            separator (SeparatorCase): The separator for the converted 
                string.

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
            separator_mapping = {
                SeparatorCase.KEBAB: "_",
                SeparatorCase.SNAKE: "-",
            }
            return separator_mapping.get(separator_case)
        other_separator = _get_other_separator()
        separator_sub = re.compile(rf'{other_separator}| ')
        no_apostrophes_str = HelperFunctions.remove_apostrophes(string)
        substrings = re.split(SeparatorCaseRegexes.SEPARATOR_SPLIT, 
                              no_apostrophes_str)
        separator_substrings = []
        for substring in substrings:
            # Substring is already in a separator case.
            if (SeparatorCaseRegexes.KEBAB_CASE.match(substring) or
                SeparatorCaseRegexes.SNAKE_CASE.match(substring)):
                if substring.isupper():
                    separator_substring = re.sub(separator_sub, 
                                                 separator_case.value, 
                                                 substring)
                else:
                    separator_substring = re.sub(separator_sub, 
                                                 separator_case.value, 
                                                 substring.lower())
            # Substring is in camel case or Pascal case.
            elif (SeparatorCaseRegexes.CAMEL_CASE.match(substring) or 
                SeparatorCaseRegexes.PASCAL_CASE.match(substring)):
                # Break camel case and Pascal case into constituent words.
                broken_words = re.split(
                    SeparatorCaseRegexes.CAMEL_PASCAL_SPLIT, substring)
                converted_words = []
                for word in broken_words:
                    converted_word = word.lower()
                    converted_words.append(converted_word)
                separator_substring = separator_case.value.join(
                    converted_words)
            # Substring is not in any of the above cases.
            else:
                # Substring is in all caps.
                if substring.isupper():
                    separator_substring = substring.replace(' ', 
                                                        separator_case.value)
                # Substring begins with an alphabebtical letter.
                elif re.match(WarpingRegexes.FIRST_LETTER, substring):
                    separator_substring = substring.lower().replace(' ', 
                                                        separator_case.value)
                # Substring does not meet either of the above conditions.
                else:
                    separator_substring = substring
            separator_substrings.append(separator_substring)
        return ''.join(separator_substrings)

    def uppercase_first_letter(string: str) -> str:
        """
        Converts the first letter of the string to uppercase without 
            modifying any other letters.

        Args:
            string (str): The string to convert.

        Returns:
            str: The converted string.
        """
        return re.sub(WarpingRegexes.FIRST_LETTER, lambda match: 
                      match.group(0).upper(), string, count=1)


def capitalize(string: str) -> str:
    """
    Capitalizes the first character of each word in a given string.

    Args:
        string (str): The string to capitalize.

    Returns:
        str: The capitalized string.
    """
    return HelperFunctions.capitalize_words(string)


def cardinal_to_ordinal(string: str) -> str:
    """
    Converts cardinal numbers to ordinal numbers in a given string.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    def replace_cardinal(match):
        """
        Helper function to replace a matched cardinal number with an 
            ordinal.

        Args:
            match (re.Match): A match object representing a cardinal 
                number found in the string.

        Returns:
            str: The ordinal version of the matched cardinal.
        """
        number_str = match.group(0)
        number = int(number_str.replace(',', ''))
        if 10 <= number % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
        formatted_number = f'{number:,}' if ',' in number_str else str(number)
        return f'{formatted_number}{suffix}'
    return re.sub(WarpingRegexes.CARDINAL, replace_cardinal, string)


def curly_to_straight(string: str) -> str:
    """
    Converts curly quotes to straight quotes in a given string.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    translation_table = str.maketrans({
        # Curly opening double quotes to straight double quotes
        '”': '"', 
        # Curly closing double quotes to straight double quotes
        '“': '"', 
        # Curly opening single quotes to straight single quotes
        '’': "'", 
        # Curly closing single quotes to straight single quotes
        '‘': "'"
    })
    return string.translate(translation_table)


def hyphens_to_em(string: str) -> str:
    """
    Converts consecutive hyphens to em dashes in a given string.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    return re.sub(WarpingRegexes.HYPHENS, '—', string)


def hyphen_to_en(string: str) -> str:
    """
    Converts hyphens to en dashes in a given string.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    return string.replace('-', '–')


def punct_to_inside(string: str) -> str:
    """
    Moves periods and commas at the end of quotes inside the quotation 
        marks.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    def _repl(match: re.Match) -> str:
        """
        Reorders periods and commas to move them inside quotation marks.

        Args:
            match (re.Match): A regular expression match object.

        Returns:
            str: The reordered string.
        """
        punct, quote = match.groups()
        return quote + punct
    return re.sub(WarpingRegexes.PUNCT_OUTSIDE, _repl, string)


def punct_to_outside(string: str) -> str:
    """
    Moves periods and commas at the end of quotes to outside the 
        quotation marks.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    def _repl(match: re.Match) -> str:
        """
        Reorders periods and commas to move them outside quotation 
            marks.

        Args:
            match (re.Match): A regular expression match object.

        Returns:
            str: The reordered string.
        """
        quote, punct = match.groups()
        return punct + quote
    return re.sub(WarpingRegexes.PUNCT_INSIDE, _repl, string)


def straight_to_curly(string: str) -> str:
    """
    Convert straight quotes to curly quotes in a given string.

    Args:
        string (str): The string to convert.

    Returns:
        curly_str (str): The converted string.
    """
    # Replace straight double quotes with opening curly double quotes.
    curly_str = re.sub(WarpingRegexes.OPENING_STRAIGHT_DOUBLE, '“', string)
    # Replace straight double quotes with closing curly double quotes.
    curly_str = re.sub(WarpingRegexes.CLOSING_STRAIGHT_DOUBLE, '”', curly_str)
    # Replace straight single quotes with opening curly single quotes.
    curly_str = re.sub(WarpingRegexes.OPENING_STRAIGHT_SINGLE, '‘', curly_str)
    # Replace straight single quotes with closing curly single quotes.
    curly_str = re.sub(WarpingRegexes.CLOSING_STRAIGHT_SINGLE, '’', curly_str)
    return curly_str


def to_alternating_caps(string: str) -> str:
    """
    Converts a string to alternating caps.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    result = []
    upper = False
    for char in string:
        if char.isalpha():
            if upper:
                result.append(char.upper())
            else:
                result.append(char.lower())
            upper = not upper
        else:
            result.append(char)
    return ''.join(result)


def to_camel_case(string: str) -> str:
    """
    Converts a string to camel case.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    def _lowercase_first_letter(string) -> str:
        """
        Lowercases the first letter of the string without modifying 
            any other letters.

        Args:
            string (str): The string to convert.

        Returns:
            str: The converted string.
        """
        return re.sub(WarpingRegexes.FIRST_LETTER, lambda match: 
                      match.group(0).lower(), string, count=1)
    pascal_str = to_pascal_case(string)
    # Split between each instance of Pascal case in the string.
    pascal_words = re.split(SeparatorCaseRegexes.CAMEL_SPLIT, pascal_str)
    camel_words = []
    for word in pascal_words:
        camel_word = _lowercase_first_letter(word)
        camel_words.append(camel_word)
    return ''.join(camel_words)


def to_kebab_case(string: str) -> str:
    """
    Converts a string to kebab case.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    return HelperFunctions.to_separator_case(string, SeparatorCase.KEBAB)


def to_lowercase(string: str) -> str:
    """
    Converts a string to lowercase.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    return string.lower()


def ordinal_to_cardinal(string: str) -> str:
    """
    Converts ordinal numbers to cardinal numbers in a given string.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    def replace_ordinal(match):
        """
        Helper function to replace a matched ordinal number with its 
            cardinal equivalent.

        Args:
            match (re.Match): A match object representing an ordinal 
                number found in the string.

        Returns:
            str: The cardinal version of the matched ordinal.
        """
        ordinal = match.group(0)
        number_str = ordinal[:-2]
        return number_str
    return re.sub(WarpingRegexes.ORDINAL, replace_ordinal, string)


def to_pascal_case(string: str) -> str:
    """
    Converts a string to Pascal case.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    no_apostrophes_str = HelperFunctions.remove_apostrophes(string)
    words = re.split(SeparatorCaseRegexes.PASCAL_SPLIT, no_apostrophes_str)
    pascal_words = []
    for word in words:
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
            pascal_word = HelperFunctions.capitalize_words(word, word_count=1)
        pascal_words.append(pascal_word)
    return ''.join(pascal_words)


def to_snake_case(string: str) -> str:
    """
    Converts a string to snake case.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    return HelperFunctions.to_separator_case(string, SeparatorCase.SNAKE)


def to_title_case(string: str) -> str:
    """
    Converts a string to title case.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    def should_capitalize(tag: str) -> bool:
        """
        Determines whether a word should be capitalized based on its 
            part of speech.

        Args:
            tag (str): The NLTK POS tag to check.

        Returns:
            bool: True if the tag should be capitalized, otherwise 
                False.
        """
        return tag not in ['CC', 'DT', 'IN', 'RP', 'TO', 'WDT']
    substrings = re.split(WarpingRegexes.TITLE_SUBSTRING_SPLIT, string)
    title_substrings = []
    for substring in substrings:
        # Capitalize the first character of the substring.
        title_substring = HelperFunctions.uppercase_first_letter(substring)
        # Split the substring into words.
        words = re.split(WarpingRegexes.TITLE_WORD_SPLIT, title_substring)
        all_words = []
        # For loop to break camel and Pascal case into constituent words
        for word in words:
            broken_words = re.split(WarpingRegexes.CAMEL_PASCAL_SPLIT, word)
            all_words.extend([broken_word for broken_word in broken_words])
        all_words_tags = pos_tag(all_words)
        # Capitalize words based on their part of speech.
        title_words = [HelperFunctions.capitalize_words(word, word_count=1) if 
                       should_capitalize(tag) else word for word, tag in 
                       all_words_tags]
        title_substring = ' '.join(title_words)
        title_substrings.append(title_substring)
    return ''.join(title_substrings)


def to_uppercase(string: str) -> str:
    """
    Converts a string to uppercase.

    Args:
        string (str): The string to convert.

    Returns:
        str: The converted string.
    """
    return string.upper()
