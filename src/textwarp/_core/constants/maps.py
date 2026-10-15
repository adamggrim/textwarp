"""Maps used across the package for lookups."""

from functools import cache
from types import MappingProxyType

import regex as re

from textwarp._core.constants import patterns
from textwarp._core.enums import CaseName

__all__ = ['get_case_names_regex_map']


@cache
def get_case_names_regex_map() -> MappingProxyType[str, re.Pattern[str]]:
    """Get a map of valid case name inputs to their corresponding
    compiled regular expressions.

    Returns:
        MappingProxyType[str, re.Pattern[str]]: A read-only dictionary
            mapping string inputs to regular expression patterns.
    """
    return MappingProxyType({
        CaseName.CAMEL.value: patterns.cases.get_camel_word(),
        CaseName.CAMEL_CASE.value: patterns.cases.get_camel_word(),
        CaseName.DOT.value: patterns.cases.get_dot_word(),
        CaseName.DOT_CASE.value: patterns.cases.get_dot_word(),
        CaseName.KEBAB.value: patterns.cases.get_kebab_word(),
        CaseName.KEBAB_CASE.value: patterns.cases.get_kebab_word(),
        CaseName.LOWER.value: patterns.cases.get_lower_word(),
        CaseName.LOWERCASE.value: patterns.cases.get_lower_word(),
        CaseName.PASCAL.value: patterns.cases.get_pascal_word(),
        CaseName.PASCAL_CASE.value: patterns.cases.get_pascal_word(),
        CaseName.SNAKE.value: patterns.cases.get_snake_word(),
        CaseName.SNAKE_CASE.value: patterns.cases.get_snake_word(),
        CaseName.UPPER.value: patterns.cases.get_upper_word(),
        CaseName.UPPERCASE.value: patterns.cases.get_upper_word(),
    })
