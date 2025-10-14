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
    DOT = '.'
    KEBAB = '-'
    SNAKE = '_'


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
