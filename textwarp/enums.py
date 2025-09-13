from enum import Enum


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
