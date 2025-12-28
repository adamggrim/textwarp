"""
This module contains sets and tuples used across the package.
"""
from typing import (
    Callable,
    Final
)
import regex as re

from .._constants import CasePatterns
from ..warping import (
    to_camel_case,
    to_dot_case,
    to_kebab_case,
    to_pascal_case,
    to_snake_case
)

__all__ = [
    'CASE_NAMES_FUNC_MAP',
    'CASE_NAMES_REGEX_MAP',
    'EXIT_INPUTS',
    'NO_INPUTS',
    'OPEN_QUOTES',
    'POS_TAGS',
    'POS_WORD_TAGS',
    'PROPER_NOUN_ENTITIES',
    'TITLE_CASE_TAG_EXCEPTIONS',
    'YES_INPUTS'
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

# Inputs for exiting the program.
EXIT_INPUTS: Final = {'quit', 'q', 'exit', 'e'}

# Inputs for indicating a negative response.
NO_INPUTS: Final = {'no', 'n'}

# Opening quote characters.
OPEN_QUOTES: Final = {'"', '“', "'", '‘'}

# Tuple of tuples for all part-of-speech tags and their names.
POS_TAGS: Final[tuple[tuple[str, str], ...]] = (
    ('ADJ', 'Adjectives'),
    ('ADP', 'Adpositions'),
    ('ADV', 'Adverbs'),
    ('CONJ', 'Conjunctions'),
    ('DET', 'Determiners'),
    ('NOUN', 'Nouns'),
    ('NUM', 'Numbers'),
    ('PART', 'Particles'),
    ('PRON', 'Pronouns'),
    ('VERB', 'Verbs'),
    ('X', 'Other')
)

# Tuple of strings for all part-of-speech tags representing words.
POS_WORD_TAGS: Final[tuple[str, ...]] = tuple(
    item[0] for item in POS_TAGS if item[0] != 'X'
)

# Named entities that are typically proper nouns.
PROPER_NOUN_ENTITIES: Final = {
    'PERSON',
    'GPE',
    'ORG',
    'NORP',
    'FAC',
    'LOC',
    'PRODUCT',
    'EVENT',
    'WORK_OF_ART',
    'LAW'
}

# Part-of-speech tag exceptions for title case capitalization.
TITLE_CASE_TAG_EXCEPTIONS: Final = {
    'CC',   # Coordinating conjunction (e.g., 'and', 'but')
    'DT',   # Determiner (e.g., 'a', 'an', 'the')
    'IN',   # Preposition or subordinating conjunction
            # (e.g., 'in', 'of', 'on')
    'RP',   # Particle (e.g., 'in' in 'give in')
    'TO',   # to (infinitive marker)
    'WDT',  # Wh-determiner (e.g., 'what')
}

# Inputs for indicating an affirmative response.
YES_INPUTS: Final = {'yes', 'y'}
