"""Map used across the package for lookups."""

from functools import lru_cache
from types import MappingProxyType

import regex as re

from textwarp._core.constants.regexes import CasePatterns

__all__ = [
    'get_case_names_regex_map'
]


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
        'camel': CasePatterns.get_camel_word(),
        'camel case': CasePatterns.get_camel_word(),
        'dot': CasePatterns.get_dot_word(),
        'dot case': CasePatterns.get_dot_word(),
        'kebab': CasePatterns.get_kebab_word(),
        'kebab case': CasePatterns.get_kebab_word(),
        'lower': CasePatterns.get_lower_word(),
        'lowercase': CasePatterns.get_lower_word(),
        'pascal': CasePatterns.get_pascal_word(),
        'pascal case': CasePatterns.get_pascal_word(),
        'snake': CasePatterns.get_snake_word(),
        'snake case': CasePatterns.get_snake_word(),
        'upper': CasePatterns.get_upper_word(),
        'uppercase': CasePatterns.get_upper_word(),
    })
