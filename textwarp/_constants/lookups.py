"""Sets, tuples and dictionaries used across the package for lookups."""

from typing import Final

import regex as re

from . import CasePatterns

__all__ = [
    'CASE_NAMES_REGEX_MAP',
    'POS_TAGS',
    'POS_WORD_TAGS',
    'PROPER_NOUN_ENTITIES',
    'TITLE_CASE_TAG_EXCEPTIONS'
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
    'LANGUAGE',
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
