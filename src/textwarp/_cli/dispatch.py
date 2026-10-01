"""A map of string inputs to case conversion functions."""

from collections.abc import Callable
from typing import Final

from textwarp._cli.args import lazy_load

__all__ = ['CASE_NAMES_FUNC_MAP']

CASE_NAMES_FUNC_MAP: Final[dict[str, Callable[[str], str]]] = {
    'camel': lazy_load('.._lib.casing', 'to_camel_case'),
    'camel case': lazy_load('.._lib.casing', 'to_camel_case'),
    'dot': lazy_load('.._lib.casing', 'to_dot_case'),
    'dot case': lazy_load('.._lib.casing', 'to_dot_case'),
    'kebab': lazy_load('.._lib.casing', 'to_kebab_case'),
    'kebab case': lazy_load('.._lib.casing', 'to_kebab_case'),
    'lower': str.lower,
    'lowercase': str.lower,
    'pascal': lazy_load('.._lib.casing', 'to_pascal_case'),
    'pascal case': lazy_load('.._lib.casing', 'to_pascal_case'),
    'snake': lazy_load('.._lib.casing', 'to_snake_case'),
    'snake case': lazy_load('.._lib.casing', 'to_snake_case'),
    'upper': str.upper,
    'uppercase': str.upper
}
