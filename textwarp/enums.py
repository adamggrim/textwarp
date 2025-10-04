from enum import Enum, auto


class CaseSeparator(Enum):
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


class Casing(Enum):
    """
    Specify which capitalization style to use in a string.

    Attributes:
        SENTENCE: Represents sentence case.
        TITLE: Represents title case.
    """
    SENTENCE = auto()
    TITLE = auto()
