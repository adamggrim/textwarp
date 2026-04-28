"""
Enumerations for casing, count labels, presence checking and regular
expression boundaries.
"""

from enum import Enum, auto, unique

from textwarp._core.context import N_

__all__ = [
    'CaseSeparator',
    'Casing',
    'CountLabels',
    'ModelPriority',
    'PresenceCheckType',
    'RegexBoundary'
]


@unique
class CaseSeparator(str, Enum):
    """
    Specify which separator character to use in a string.

    Attributes:
        DOT: Represents `dot.case`.
        KEBAB: Represents `kebab-case`.
        SNAKE: Represents `snake_case`.
    """
    DOT = '.'
    KEBAB = '-'
    SNAKE = '_'


@unique
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


@unique
class CountLabels(str, Enum):
    """
    Label strings for count formatting.

    Attributes:
        CHAR: String specifying character count.
        LINE: String specifying line count.
        SENTENCE: String specifying sentence count.
        WORD: String specifying word count.
    """
    CHAR = N_('Character')
    LINE = N_('Line')
    SENTENCE = N_('Sentence')
    WORD = N_('Word')


@unique
class ModelPriority(str, Enum):
    """
    Specify whether to prioritize accuracy or speed for spaCy model
    selection.

    Attributes:
        ACCURACY: Prioritize accuracy over speed.
        SPEED: Prioritize speed over accuracy.
    """
    ACCURACY = 'accuracy'
    SPEED = 'speed'


@unique
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
    CASE = auto()
    REGEX = auto()
    SUBSTRING = auto()


@unique
class RegexBoundary(Enum):
    """
    Specify the boundary-matching strategy for a regular expression.

    Attributes:
        WORD_BOUNDARY: Matches the pattern only when it appears as a
            whole word.
        START_ANCHOR: Matches the pattern only when it appears at the
            start of a string.
        END_ANCHOR: Matches the pattern only when it appears at the end
            of a string.
    """
    WORD_BOUNDARY = auto()
    START_ANCHOR = auto()
    END_ANCHOR = auto()


@unique
class TokenType(Enum):
    """
    Specify the type of token extracted during programming case
    chunking.

    Attributes:
        WORD: An alphanumeric word chunk.
        SYMBOL: A non-alphanumeric character that is not a standard
            casing separator.
        SEPARATOR: A standard casing separator (space, dot, dash, or
            underscore).
    """
    WORD = auto()
    SYMBOL = auto()
    SEPARATOR = auto()
