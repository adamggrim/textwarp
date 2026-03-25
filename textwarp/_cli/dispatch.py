"""A mapping of string inputs to case conversion functions."""

import importlib
from typing import Callable, Final


def _lazy_load_warping(func_name: str) -> Callable[[str], str]:
    """Lazy load functions from the warping module."""
    def wrapper(text: str) -> str:
        mod = importlib.import_module('textwarp.warping')
        return getattr(mod, func_name)(text)
    return wrapper


__all__ = ['CASE_NAMES_FUNC_MAP']

# Mapping of valid case name inputs to their standardized names.
CASE_NAMES_FUNC_MAP: Final[dict[str, Callable[[str], str]]] = {
    'camel': _lazy_load_warping('to_camel_case'),
    'camel case': _lazy_load_warping('to_camel_case'),
    'dot': _lazy_load_warping('to_dot_case'),
    'dot case': _lazy_load_warping('to_dot_case'),
    'kebab': _lazy_load_warping('to_kebab_case'),
    'kebab case': _lazy_load_warping('to_kebab_case'),
    'lower': str.lower,
    'lowercase': str.lower,
    'pascal': _lazy_load_warping('to_pascal_case'),
    'pascal case': _lazy_load_warping('to_pascal_case'),
    'snake': _lazy_load_warping('to_snake_case'),
    'snake case': _lazy_load_warping('to_snake_case'),
    'upper': str.upper,
    'uppercase': str.upper
}
