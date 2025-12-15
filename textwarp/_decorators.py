"""
Provides a custom decorator function to denote non-instantiable classes.
"""

from typing import TypeVar

# Type variable bound to ``type`` so the decorator preserves the
# identity of the class it modifies.
_T = TypeVar('_T', bound=type)


def non_instantiable(cls: _T) -> _T:
    """Class decorator to make a class non-instantiable.

    Args:
        cls (type): The class to be made non-instantiable.

    Returns:
        type: The modified class with an __init__ method that always
            raises a RuntimeError.

    Raises:
        RuntimeError: When an attempt is made to instantiate the
            decorated class.
    """
    def __init__(self, *args, **kwargs) -> None:
        raise RuntimeError(f'{cls.__name__} cannot be instantiated.')

    setattr(cls, '__init__', __init__)
    return cls
