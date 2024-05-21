import re


class WarpingRegexes:
    """
    Compiled regular expressions and strings for parsing text.

    Attributes:
        _CLOSING_LOOKAHEAD_STR (str): Regular expression pattern for 
            identifying when a quote is closing.
        _OPENING_LOOKBEHIND_STR (str): Regular expression pattern for 
            identifying when a quote is opening.

        CAMEL_CASE (Pattern): Compiled regular expression object that 
            captures a camel case string.
        CAMEL_PASCAL_SPLIT (Pattern): Compiled regular expression 
            object for substituting the boundary between words in camel 
            case and Pascal case.
        CAMEL_SPLIT (Pattern): Compiled regular expression object for 
            splitting strings before converting substrings to camel 
            case.
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
        KEBAB_CASE (Pattern): Compiled regular expression object that 
            captures a kebab case string.
        LETTER_WORD (Pattern): Compiled regular expression object that 
            captures a sequence of word characters that begin with an 
            alphabetical letter.
        OPENING_STRAIGHT_DOUBLE (Pattern): Compiled regular expression 
            object that captures opening straight double quotes.
        OPENING_STRAIGHT_SINGLE (Pattern): Compiled regular expression 
            object that captures opening straight single quotes.
        PASCAL_CASE (Pattern): Compiled regular expression object that 
            captures a Pascal case string.
        PASCAL_SPLIT (Pattern): Compiled regular expression object for 
            splitting strings before converting substrings to camel 
            case or Pascal case.
        PUNCT_INSIDE (Pattern): Compiled regular expression object with 
            capturing groups for punctuation inside quotes and quotes 
            outside punctuation.
        PUNCT_OUTSIDE (Pattern): Compiled regular expression object 
            with capturing groups for quotes inside punctuation and 
            punctuation outside quotes.
        SEPARATOR_SPLIT (Pattern): Compiled regular expression object 
            for splitting strings before converting substrings to kebab 
            case or snake case.
        SHORT_ACRONYM (Pattern): Compiled regular expression object 
            that captures a two-character acronym or initialism.
        SNAKE_CASE (Pattern): Compiled regular expression object that 
            captures a snake case string.
        WORD_WITH_APOS (Pattern): Compiled regular expression object 
            that captures words with apostrophes as a single word.
    """
    _CLOSING_LOOKAHEAD_STR = r'(?=\w|\s|\.|\!|\?|:|;|,|\)|\]|\})'
    _OPENING_LOOKBEHIND_STR = r'(?<=\s|\(|\[|\{)'

    CAMEL_CASE = re.compile(r'[a-z][a-z0-9]*([A-Z][A-Z]?[a-z0-9]*)+')
    CAMEL_PASCAL_SPLIT = re.compile(r'(?<=[a-z0-9])(?=[A-Z])')
    CAMEL_SPLIT = re.compile(r'(?<=[\s—–\-])')
    CLOSING_STRAIGHT_DOUBLE = re.compile(rf'"$|"{_CLOSING_LOOKAHEAD_STR}')
    CLOSING_STRAIGHT_SINGLE = re.compile(rf"'$|'{_CLOSING_LOOKAHEAD_STR}")
    FIRST_LETTER = re.compile(r'([A-Za-z])')
    HYPHENS = re.compile(r'\s?--?\s?')
    HYPHEN_UNDERSCORE = re.compile(r'\-|_')
    KEBAB_CASE = re.compile(r'([A-Za-z0-9]+\-[A-Za-z0-9]\-?)+')
    LETTER_WORD = re.compile(r'([A-Za-z]\w*)')
    OPENING_STRAIGHT_DOUBLE = re.compile(rf'(^|{_OPENING_LOOKBEHIND_STR})"')
    OPENING_STRAIGHT_SINGLE = re.compile(rf"(^|{_OPENING_LOOKBEHIND_STR})'")
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
        \b                      # Split to ensure word character substrings 
                                    # begin and end with word characters
        ''', re.VERBOSE)
    PUNCT_INSIDE = re.compile(r'([.,])(["”\'’]?["”\'’])')
    PUNCT_OUTSIDE = re.compile(r'(["”\'’]?["”\'’])([.,])')
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
    WORD_WITH_APOS = re.compile(r'\w+([\'’]\w+)?')