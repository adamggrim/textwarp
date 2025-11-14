"""
Provides a custom decorator function to denote non-instantiable classes.
"""

def non_instantiable(cls) -> None:
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
    def __init__(self, *args, **kwargs):
        raise RuntimeError(f'{cls.__name__} cannot be instantiated.')

    cls.__init__ = __init__
    return cls
