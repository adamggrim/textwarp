"""Maps used across the package for lookups."""

from functools import lru_cache
from types import MappingProxyType

import regex as re

from textwarp._core.constants import patterns

__all__ = ['get_case_names_regex_map']


@lru_cache(maxsize=1)
def get_case_names_regex_map() -> MappingProxyType[str, re.Pattern[str]]:
    """
    Get a mapping of valid case name inputs to their corresponding
    compiled regular expressions.

    Returns:
        MappingProxyType[str, re.Pattern[str]]: A read-only dictionary
            mapping string inputs to regular expression patterns.
    """
    return MappingProxyType({
        'camel': patterns.cases.get_camel_word(),
        'camel case': patterns.cases.get_camel_word(),
        'dot': patterns.cases.get_dot_word(),
        'dot case': patterns.cases.get_dot_word(),
        'kebab': patterns.cases.get_kebab_word(),
        'kebab case': patterns.cases.get_kebab_word(),
        'lower': patterns.cases.get_lower_word(),
        'lowercase': patterns.cases.get_lower_word(),
        'pascal': patterns.cases.get_pascal_word(),
        'pascal case': patterns.cases.get_pascal_word(),
        'snake': patterns.cases.get_snake_word(),
        'snake case': patterns.cases.get_snake_word(),
        'upper': patterns.cases.get_upper_word(),
        'uppercase': patterns.cases.get_upper_word(),
    })
