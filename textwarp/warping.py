import re

from textwarp.enums import SeparatorCase
from textwarp.regexes import WarpingRegexes


class HelperFunctions:

    def capitalize_first_word(string) -> str:
        """
        Capitalizes the first letter of the first word of a string and 
            converts all other letters in the word to lowercase.

        Args:
            string (str): The string to capitalize.

        Returns:
            capitalized_str (str): The capitalized string.
        """
        capitalized_str = re.sub(WarpingRegexes.LETTER_WORD, lambda match: 
                                 match.group(0).capitalize(), string, count=1)
        return capitalized_str

    def to_separator_case(string, separator_case: SeparatorCase) -> str:
        """
        Converts a string to kebab case or snake case.

        Args:
            string (str): The string to convert.
            separator (SeparatorCase): The separator for the converted 
                string.

        Returns:
            separator_str (str): The converted string.

        """
        def _get_other_separator():
            """
            For a given a separator case, returns the other separator 
                character.

            Returns:
                The other separator character.
            """
            separator_mapping = {
                SeparatorCase.KEBAB: "_",
                SeparatorCase.SNAKE: "-",
            }
            return separator_mapping.get(separator_case)
        other_separator = _get_other_separator()
        separator_sub = re.compile(rf'{other_separator}| ')
        substrings = re.split(WarpingRegexes.SEPARATOR_SPLIT, string)
        separator_substrings = []
        for substring in substrings:
            # Substring is already in a separator case.
            if (WarpingRegexes.KEBAB_CASE.match(substring) or
                WarpingRegexes.SNAKE_CASE.match(substring)):
                if substring.isupper():
                    separator_substring = re.sub(separator_sub, 
                                                 separator_case.value, 
                                                 substring)
                else:
                    separator_substring = re.sub(separator_sub, 
                                                 separator_case.value, 
                                                 substring.lower())
            # Substring is in camel case or Pascal case.
            elif (WarpingRegexes.CAMEL_CASE.match(substring) or 
                WarpingRegexes.PASCAL_CASE.match(substring)):
                # Break camel case and Pascal case into constituent words.
                broken_words = re.split(WarpingRegexes.CAMEL_PASCAL_SPLIT, 
                                        substring)
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
        separator_str = ''.join(separator_substrings)
        return separator_str


def capitalize(string: str) -> str:
    """
    Capitalizes the first character of each word in a given string.

    Args:
        string (str): The string to capitalize.

    Return:
        capitalized_str (str): The capitalized string.
    """
    capitalized_str = re.sub(WarpingRegexes.WORD_WITH_APOS, 
        lambda m: m.group(0).capitalize(), string)
    return capitalized_str


def curly_to_straight(string: str) -> str:
    """
    Converts curly quotes to straight quotes in a given string.

    Args:
        string (str): The string to convert.

    Returns:
        straight_str (str): The converted string.
    """
    translation_table = str.maketrans({
        # Opening curly double quotes to straight double quotes
        '”': '"', 
        # Closing curly double quotes to straight double quotes
        '“': '"', 
        # Opening curly single quotes to straight single quotes
        '’': "'", 
        # Closing curly single quotes to straight single quotes
        '‘': "'"
    })
    straight_str = string.translate(translation_table)
    return straight_str


def hyphens_to_em(string: str) -> str:
    """
    Converts consecutive hyphens to em dashes in a given string.

    Args:
        string (str): The string to convert.

    Returns:
        em_str (str): The converted string.
    """
    em_str = re.sub(WarpingRegexes.HYPHENS, '—', string)
    return em_str


def hyphen_to_en(string: str) -> str:
    """
    Converts hyphens to en dashes in a given string.

    Args:
        string (str): The string to convert.

    Returns:
        en_str (str): The converted string.
    """
    en_str = string.replace('-', '–')
    return en_str


def punct_to_inside(string: str) -> str:
    """
    Moves periods and commas at the end of quotes inside the quotation 
        marks.

    Args:
        string (str): The string to convert.

    Returns:
        punct_inside_str: The converted string.
    """
    def _repl(match: re.Match) -> str:
        """
        Reorders periods and commas to move them inside quotation marks.

        Args:
            match (re.Match): A regular expression match object.

        Returns:
            reordered_str (str): The reordered string.
        """
        punct, quote = match.groups()
        reordered_str = quote + punct
        return reordered_str
    punct_inside_str = re.sub(WarpingRegexes.PUNCT_OUTSIDE, _repl, string)
    return punct_inside_str


def punct_to_outside(string: str) -> str:
    """
    Moves periods and commas at the end of quotes to outside the 
        quotation marks.

    Args:
        string (str): The string to convert.

    Returns:
        punct_outside_str: The converted string.
    """
    def _repl(match: re.Match) -> str:
        """
        Reorders periods and commas to move them outside quotation 
            marks.

        Args:
            match (re.Match): A regular expression match object.

        Returns:
            reordered_str (str): The reordered string.
        """
        quote, punct = match.groups()
        reordered_str = punct + quote
        return reordered_str
    punct_outside_str = re.sub(WarpingRegexes.PUNCT_INSIDE, _repl, string)
    return punct_outside_str


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


def to_camel_case(string: str) -> str:
    """
    Converts a string to camel case.

    Args:
        string (str): The string to convert.

    Returns:
        camel_str (str): The converted string.
    """
    def _lowercase_first_letter(string) -> str:
        """
        Lowercases the first letter of the string without modifying 
            any other letters.

        Args:
            string (str): The string to convert.

        Returns:
            lowercase_first_letter_str (str): The converted string.
        """
        lowercase_first_letter_str = re.sub(WarpingRegexes.FIRST_LETTER, 
                                            lambda match: 
                                            match.group(0).lower(), string, 
                                            count=1)
        return lowercase_first_letter_str
    pascal_str = to_pascal_case(string)
    # Split between each instance of Pascal case in the string.
    pascal_words = re.split(WarpingRegexes.CAMEL_SPLIT, pascal_str)
    camel_words = []
    for word in pascal_words:
        camel_word = _lowercase_first_letter(word)
        camel_words.append(camel_word)
    camel_str = ''.join(camel_words)
    return camel_str


def to_kebab_case(string: str) -> str:
    """
    Converts a string to kebab case.

    Args:
        string (str): The string to convert.

    Returns:
        kebab_str (str): The converted string.
    """
    return HelperFunctions.to_separator_case(string, SeparatorCase.KEBAB)


def to_lowercase(string: str) -> str:
    """
    Converts a string to lowercase.

    Args:
        string (str): The string to convert.

    Returns:
        lowercase_str (str): The lowercase string.
    """
    lowercase_str = string.lower()
    return lowercase_str


def to_pascal_case(string: str) -> str:
    """
    Converts a string to Pascal case.

    Args:
        string (str): The string to convert.

    Returns:
        pascal_str (str): The converted string.
    """
    def _capitalize_first_letter(string) -> str:
        """
        Capitalizes the first letter of the string without modifying 
            any other letters.

        Args:
            string (str): The string to convert.

        Returns:
            capitalized_first_letter_str (str): The converted string.
        """
        capitalized_first_letter_str = re.sub(WarpingRegexes.FIRST_LETTER, 
                                              lambda match: 
                                              match.group(0).upper(), string, 
                                              count=1)
        return capitalized_first_letter_str
    words = re.split(WarpingRegexes.PASCAL_SPLIT, string)
    pascal_words = []
    for word in words:
        # Word is already in Pascal case.
        if WarpingRegexes.PASCAL_CASE.match(word):
            pascal_word = word
        # Word is an acronym of two characters.
        elif WarpingRegexes.SHORT_ACRONYM.match(word):
            pascal_word = word
        # Word is in camel case.
        elif WarpingRegexes.CAMEL_CASE.match(word):
            pascal_word = _capitalize_first_letter(word)
        # Word is not in Pascal case or camel case.
        else:
            pascal_word = HelperFunctions.capitalize_first_word(word)
        pascal_words.append(pascal_word)
    pascal_str = ''.join(pascal_words)
    return pascal_str


def to_snake_case(string: str) -> str:
    """
    Converts a string to snake case.

    Args:
        string (str): The string to convert.

    Returns:
        snake_str (str): The converted string.
    """
    return HelperFunctions.to_separator_case(string, SeparatorCase.SNAKE)


def to_uppercase(string: str) -> str:
    """
    Converts a string to uppercase.

    Args:
        string (str): The string to convert.

    Returns:
        upper_str (str): The converted string.
    """
    upper_str = string.upper()
    return upper_str