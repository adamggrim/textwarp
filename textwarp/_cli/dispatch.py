"""A mapping of string inputs to case conversion functions."""

from typing import (
    Final,
    Callable
)

from ..warping import (
    to_camel_case,
    to_dot_case,
    to_kebab_case,
    to_pascal_case,
    to_snake_case
)

__all__ = [
    'CASE_NAMES_FUNC_MAP'
]

# Mapping of valid case name inputs to their standardized names.
CASE_NAMES_FUNC_MAP: Final[dict[str, Callable[[str], str]]]= {
    'camel': to_camel_case,
    'camel case': to_camel_case,
    'dot': to_dot_case,
    'dot case': to_dot_case,
    'lower': str.lower,
    'lowercase': str.lower,
    'kebab': to_kebab_case,
    'kebab case': to_kebab_case,
    'pascal': to_pascal_case,
    'pascal case': to_pascal_case,
    'snake': to_snake_case,
    'snake case': to_snake_case,
    'upper': str.upper,
    'uppercase': str.upper,
}
