from enum import Enum


class SeparatorCase(Enum):
    """
    Enum for selecting the separator case to apply to a string.
    
    Attributes:
        KEBAB: Represents kebab case.
        SNAKE: Represents snake case.
    """
    KEBAB = "-"
    SNAKE = "_"