"""A map of string inputs to case conversion functions."""

from collections.abc import Callable
from typing import Final

from textwarp._cli.args import lazy_load
from textwarp._core.enums import CaseName

__all__ = ['CASE_NAMES_FUNC_MAP']

CASE_NAMES_FUNC_MAP: Final[dict[str, Callable[[str], str]]] = {
    CaseName.CAMEL.value: lazy_load('.._lib.casing', 'to_camel_case'),
    CaseName.CAMEL_CASE.value: lazy_load('.._lib.casing', 'to_camel_case'),
    CaseName.DOT.value: lazy_load('.._lib.casing', 'to_dot_case'),
    CaseName.DOT_CASE.value: lazy_load('.._lib.casing', 'to_dot_case'),
    CaseName.KEBAB.value: lazy_load('.._lib.casing', 'to_kebab_case'),
    CaseName.KEBAB_CASE.value: lazy_load('.._lib.casing', 'to_kebab_case'),
    CaseName.LOWER.value: str.lower,
    CaseName.LOWERCASE.value: str.lower,
    CaseName.PASCAL.value: lazy_load('.._lib.casing', 'to_pascal_case'),
    CaseName.PASCAL_CASE.value: lazy_load('.._lib.casing', 'to_pascal_case'),
    CaseName.SNAKE.value: lazy_load('.._lib.casing', 'to_snake_case'),
    CaseName.SNAKE_CASE.value: lazy_load('.._lib.casing', 'to_snake_case'),
    CaseName.UPPER.value: str.upper,
    CaseName.UPPERCASE.value: str.upper
}
