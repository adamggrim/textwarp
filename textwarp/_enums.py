"""
Defines enums for text warping and analysis.

Classes:
    CaseSeparator: Specifies separator case separators (dot, kebab, snake).
    Casing: Specifies capitalization styles (sentence, start, title).
    CountLabels: Defines labels for text analysis.
    RegexBoundary: Defines regular expression boundary positions.
"""

from enum import Enum, auto
from typing import final


@final
class CaseSeparator(str, Enum):
    """
    Specify which separator character to use in a string.

    Attributes:
        DOT: Represents dot.case.
        KEBAB: Represents kebab-case.
        SNAKE: Represents snake_case.
    """
    DOT: str = '.'
    KEBAB: str = '-'
    SNAKE: str = '_'


@final
class Casing(Enum):
    """
    Specify which capitalization style to use in a string.

    Attributes:
        SENTENCE: Represents sentence case.
        START: Represents start case.
        TITLE: Represents title case.
    """
    SENTENCE = auto()
    START = auto()
    TITLE = auto()


@final
class CountLabels(str, Enum):
    """
    Label strings for count formatting.

    Attributes:
        CHAR: String specifying character count.
        LINE: String specifying line count.
        SENTENCE: String specifying sentence count.
        WORD: String specifying word count.
    """
    CHAR = 'Character'
    LINE = 'Line'
    SENTENCE = 'Sentence'
    WORD = 'Word'


@final
class RegexBoundary(Enum):
    """
    Specify the boundary-matching strategy for a regular expression.

    Attributes:
        WORD_BOUNDARY: Represents the pattern only when it appears as a
            whole word.
        END_ANCHOR: Anchors the pattern to the end of the string.
        NONE: Represents the pattern without any boundaries or anchors.
    """
    WORD_BOUNDARY = auto()
    END_ANCHOR = auto()
    NONE = auto()
