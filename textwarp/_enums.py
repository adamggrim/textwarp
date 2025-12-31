"""
Enumerations for casing, count labels, presence checking and regular
expression boundaries.
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
class PresenceCheckType(Enum):
    """
    Specify whether to check for the presence of a case, regular
    expression or substring in a given string.

    Attributes:
        CASE: Check for the presence of a specific case (e.g., camel
            case or snake case).
        REGEX: Check for a regular expression match.
        SUBSTRING: Check for the presence of a substring.
    """
    CASE_NAME = auto()
    REGEX = auto()
    SUBSTRING = auto()


@final
class RegexBoundary(Enum):
    """
    Specify the boundary-matching strategy for a regular expression.

    Attributes:
        WORD_BOUNDARY: Matches the pattern only when it appears as a
            whole word.
        END_ANCHOR: Matches the pattern only when it appears at the end
            of a string.
    """
    WORD_BOUNDARY = auto()
    END_ANCHOR = auto()
