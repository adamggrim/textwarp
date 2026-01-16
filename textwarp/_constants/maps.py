"""Map used across the package for lookups."""

from typing import Final

import regex as re

from .regexes import CasePatterns

__all__ = [
    'CASE_NAMES_REGEX_MAP'
]

CASE_NAMES_REGEX_MAP: Final[dict[str, re.Pattern[str]]] = {
    'camel': CasePatterns.CAMEL_WORD,
    'camel case': CasePatterns.CAMEL_WORD,
    'dot': CasePatterns.DOT_WORD,
    'dot case': CasePatterns.DOT_WORD,
    'kebab': CasePatterns.KEBAB_WORD,
    'kebab case': CasePatterns.KEBAB_WORD,
    'lower': CasePatterns.LOWER_WORD,
    'lowercase': CasePatterns.LOWER_WORD,
    'pascal': CasePatterns.PASCAL_WORD,
    'pascal case': CasePatterns.PASCAL_WORD,
    'snake': CasePatterns.SNAKE_WORD,
    'snake case': CasePatterns.SNAKE_WORD,
    'upper': CasePatterns.UPPER_WORD,
    'uppercase': CasePatterns.UPPER_WORD,
}
