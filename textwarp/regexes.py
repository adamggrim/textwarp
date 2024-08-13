import re


class SeparatorCaseRegexes:
    """
    Compiled regular expressions for parsing and warping text before 
        conversion to kebab case or snake case.

    Attributes:
        CAMEL_CASE (Pattern): Compiled regular expression object that 
            captures a camel case string.
        CAMEL_PASCAL_SPLIT (Pattern): Compiled regular expression 
            object for splitting on the boundary between words in camel 
            case and Pascal case.
        KEBAB_CASE (Pattern): Compiled regular expression object that 
            captures a kebab case string.
        PASCAL_CASE (Pattern): Compiled regular expression object that 
            captures a Pascal case string.
        PASCAL_SPLIT (Pattern): Compiled regular expression object for 
            splitting strings before converting substrings to camel 
            case or Pascal case.
        SEPARATOR_SPLIT (Pattern): Compiled regular expression object 
            for splitting strings before converting substrings to kebab 
            case or snake case.
        SHORT_ACRONYM (Pattern): Compiled regular expression object 
            that captures a two-character acronym or initialism.
        SNAKE_CASE (Pattern): Compiled regular expression object that 
            captures a snake case string.
    """
    CAMEL_CASE = re.compile(r'[a-z][a-z0-9]*([A-Z][A-Z]?[a-z0-9]*)+')
    CAMEL_PASCAL_SPLIT = re.compile(r'''
        (?<=[a-z0-9])   # Positive lookbehind to split after a lowercase 
                            # letter or digit
        (?=[A-Z])       # Positive lookahead to split before an uppercase 
                            # letter
        |               # OR
        (?<=[a-zA-Z])   # Positive lookbehind to split after a lowercase or 
                            # uppercase letter
        (?=[0-9])       # Positive lookahead to split before a digit
        ''', re.VERBOSE)
    KEBAB_CASE = re.compile(r'([A-Za-z0-9]+\-[A-Za-z0-9]\-?)+')
    PASCAL_CASE = re.compile(r'[A-Z][a-z0-9]+([A-Z][A-Z]?[a-z0-9]*)+')
    PASCAL_SPLIT = re.compile(r'''
        (?<![ .!?—–\-,:;"”\'’]) # Negative lookbehind to preserve spacing 
                                    # after spaces, punctuation and dashes
        [ ]                     # Character class to split on a single space
        (?![ —–\-"“\'‘\(\[{])   # Negative lookahead to preserve spacing 
                                    # before dashes, quotes and brackets
        |                       # OR
        (?<=\w)-(?=\w)          # Positive lookbehind to split on a hyphen 
                                    # between word characters and convert from 
                                    # kebab case
        |                       # OR
        _                       # Split on an underscore to convert from snake 
                                    # case
        |                       # OR
        \b                      # Split on a word boundary character to ensure 
                                    # substrings begin and end with a word 
                                    # character.
        ''', re.VERBOSE)
    SEPARATOR_SPLIT = re.compile(r'''
        (?<=\W\s)               # Positive lookbehind to split after a 
                                    # non-word character followed by a space 
                                    # character
        |                       # OR
        (?<=["“\'‘(\[{])        # Positive lookbehind to split after opening 
                                    # quotes and brackets
        |                       # OR
        (?<=—\b)                # Postive lookbehind to split after an em dash 
                                    # followed by a word boundary character
        |                       # OR
        (?<=\t)                 # Positive lookbehind to split after a tab 
                                    # character
        |                       # OR
        (?=[.!?—,:;"”\'’)\]}])  # Positive lookahead to split before 
                                    # punctuation or an em dash or bracket
        |                       # OR
        (?=\s+[–"”(\[{])        # Positive lookahead to split before spacing 
                                    # followed by an en dash, quote or bracket
        |                       # OR
        (?=--)                  # Positive lookahead to split before two 
                                    # consecutive hyphens
        |                       # OR
        (?=-\s+)                # Positive lookahead to split before a hyphen 
                                    # followed by one or more space characters
        |                       # OR
        (?=\s{2,})              # Positive lookahead to split before 
                                    # consecutive spaces
        |                       # OR
        (?=\t)                  # Positive lookahead to split on a tab 
                                    # character
        ''', re.VERBOSE)
    SHORT_ACRONYM = re.compile(r'[A-Z]{2}\b')
    SNAKE_CASE = re.compile(r'([A-Za-z0-9]+_[A-Za-z0-9]+_?)+')


class WarpingRegexes:
    """
    Compiled regular expressions and strings for parsing and warping 
        text.

    Attributes:
        __CLOSING_LOOKAHEAD_STR (str): Regular expression pattern for 
            identifying when a quote is closing.
        __OPENING_LOOKBEHIND_STR (str): Regular expression pattern for 
            identifying when a quote is opening.

        CAMEL_SPLIT (Pattern): Compiled regular expression object for 
            splitting strings before converting substrings to camel 
            case.
        CARDINAL (Pattern): Compiled regular expression object that 
            captures a cardinal number.
        CLOSING_STRAIGHT_DOUBLE (Pattern): Compiled regular expression 
            object that captures closing straight double quotes.
        CLOSING_STRAIGHT_SINGLE (Pattern): Compiled regular expression 
            object that captures closing straight single quotes.
        FIRST_LETTER (Pattern): Compiled regular expression object that 
            captures the first alphabetical letter of a string.
        HYPHENS (Pattern): Compiled regular expression object that 
            captures double hyphens that function as an em dash.
        HYPHEN_UNDERSCORE (Pattern): Compiled regular expression object 
            that captures hyphens and underscores.
        LETTER_APOSTROPHE (Pattern): Compiled regular expression object 
            that captures an apostrophe character surrounded by 
            alphabetical letter characters
        LETTER_WORD (Pattern): Compiled regular expression object that 
            captures a sequence of word characters that begin with an 
            alphabetical letter. Captures words with apostrophes as a 
            single word.
        OPENING_STRAIGHT_DOUBLE (Pattern): Compiled regular expression 
            object that captures opening straight double quotes.
        OPENING_STRAIGHT_SINGLE (Pattern): Compiled regular expression 
            object that captures opening straight single quotes.
        ORDINAL (Pattern): Compiled regular expression object that 
            captures an ordinal number.
        PUNCT_INSIDE (Pattern): Compiled regular expression object with 
            capturing groups for punctuation inside quotes and quotes 
            outside punctuation.
        PUNCT_OUTSIDE (Pattern): Compiled regular expression object 
            with capturing groups for quotes inside punctuation and 
            punctuation outside quotes.
        TITLE_SUBSTRING_SPLIT (Pattern): Compiled regular expression 
            object for splitting strings into substrings before 
            capitalizing the first character.
        TITLE_WORD_SPLIT (Pattern): Compiled regular expression object 
            for splitting substrings into words before capitalizing 
            title case words.
    """
    __CLOSING_LOOKAHEAD_STR = r'(?=\w|\s|\.|\!|\?|:|;|,|\)|\]|\})'
    __OPENING_LOOKBEHIND_STR = r'(?<=\s|\(|\[|\{)'

    CAMEL_SPLIT = re.compile(r'(?<=[\s—–\-])')
    CARDINAL = re.compile(r'(?<!\d\.)\b(\d{1,3}(?:,\d{3})+|\d+)\b(?!\.\d)')
    CLOSING_STRAIGHT_DOUBLE = re.compile(rf'"$|"{__CLOSING_LOOKAHEAD_STR}')
    CLOSING_STRAIGHT_SINGLE = re.compile(rf"'$|'{__CLOSING_LOOKAHEAD_STR}")
    FIRST_LETTER = re.compile(r'([A-Za-z])')
    HYPHENS = re.compile(r'\s?--?\s?')
    HYPHEN_UNDERSCORE = re.compile(r'\-|_')
    LETTER_APOSTROPHE = re.compile(r'(?<=[A-Za-z])[\'’](?=[A-Za-z])')
    LETTER_WORD = re.compile(r'([A-Za-z]\w*)([\'’]\w+)?')
    OPENING_STRAIGHT_DOUBLE = re.compile(rf'(^|{__OPENING_LOOKBEHIND_STR})"')
    OPENING_STRAIGHT_SINGLE = re.compile(rf"(^|{__OPENING_LOOKBEHIND_STR})'")
    ORDINAL = re.compile(r'\b\d+(?:st|nd|rd|th)\b')
    PUNCT_INSIDE = re.compile(r'([.,])(["”\'’]?["”\'’])')
    PUNCT_OUTSIDE = re.compile(r'(["”\'’]?["”\'’])([.,])')
    TITLE_SUBSTRING_SPLIT = re.compile(r'(?<=[\n\.:])')
    TITLE_WORD_SPLIT = re.compile(r' |-|_')
