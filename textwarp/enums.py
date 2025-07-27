from enum import Enum, auto


class Casing(Enum):
    """
    Specify which casing style to apply to a string.

    Attributes:
        TITLE: Represents title case (e.g., A Tale of Two Cities).
        SENTENCE: Represents sentence case (e.g., A tale of two
            cities.).
        CAPITALIZE: Represents capitalizing every word (e.g., A Tale Of
            Two Cities).
    """
    TITLE = auto()
    SENTENCE = auto()
    CAPITALIZE = auto()


class Separator(Enum):
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

