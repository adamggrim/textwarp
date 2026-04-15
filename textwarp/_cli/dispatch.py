"""A map of string inputs to case conversion functions."""

from typing import Callable, Final

from textwarp._cli.args import _lazy_load

__all__ = ['CASE_NAMES_FUNC_MAP']

# Map of valid case name inputs and their associated functions.
CASE_NAMES_FUNC_MAP: Final[dict[str, Callable[[str], str]]] = {
    'camel': _lazy_load('..warping', 'to_camel_case'),
    'camel case': _lazy_load('..warping', 'to_camel_case'),
    'dot': _lazy_load('..warping', 'to_dot_case'),
    'dot case': _lazy_load('..warping', 'to_dot_case'),
    'kebab': _lazy_load('..warping', 'to_kebab_case'),
    'kebab case': _lazy_load('..warping', 'to_kebab_case'),
    'lower': str.lower,
    'lowercase': str.lower,
    'pascal': _lazy_load('..warping', 'to_pascal_case'),
    'pascal case': _lazy_load('..warping', 'to_pascal_case'),
    'snake': _lazy_load('..warping', 'to_snake_case'),
    'snake case': _lazy_load('..warping', 'to_snake_case'),
    'upper': str.upper,
    'uppercase': str.upper
}
