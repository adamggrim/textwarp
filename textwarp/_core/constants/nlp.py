"""Objects used across the package for spaCy processing."""

from typing import Final

__all__ = [
    'NOUN_TAGS',
    'POS_TAGS',
    'POS_WORD_TAGS',
    'PROPER_NOUN_ENTITIES',
    'SUBJECT_POS_TAGS'
]

# Coarse-grained parts-of-speech tags for stopping a subject search when
# looking left.
LEFT_SEARCH_STOP_TAGS: Final[frozenset[str]] = frozenset(
    {'DET', 'VERB', 'PUNCT'}
)

# Coarse-grained parts-of-speech tags for singular and proper nouns.
NOUN_TAGS: Final[frozenset[str]] = frozenset({'NOUN', 'PROPN'})

# Tuple of tuples for all parts-of-speech tags and their names.
POS_TAGS: Final[tuple[tuple[str, str], ...]] = (
    ('ADJ', 'Adjectives'),
    ('ADP', 'Adpositions'),
    ('ADV', 'Adverbs'),
    ('AUX', 'Auxiliaries'),
    ('CCONJ', 'Coordinating Conjunctions'),
    ('DET', 'Determiners'),
    ('INTJ', 'Interjections'),
    ('NOUN', 'Nouns'),
    ('NUM', 'Numbers'),
    ('PART', 'Particles'),
    ('PRON', 'Pronouns'),
    ('PROPN', 'Proper Nouns'),
    ('SCONJ', 'Subordinating Conjunctions'),
    ('VERB', 'Verbs'),
    ('X', 'Other')
)

# Tuple of strings for all coarse-grained parts-of-speech tags
# representing words.
POS_WORD_TAGS: Final[tuple[str, ...]] = tuple(
    item[0] for item in POS_TAGS if item[0] != 'X'
)

# Coarse-grained parts-of-speech tags for stopping a subject search when
# looking right.
RIGHT_SEARCH_STOP_TAGS: Final[frozenset[str]] = frozenset({'VERB', 'PUNCT'})

# Named entities that are typically proper nouns.
PROPER_NOUN_ENTITIES: Final[frozenset[str]] = frozenset({
    'EVENT',
    'FAC',
    'GPE',
    'LANGUAGE',
    'LAW',
    'LOC',
    'NORP',
    'ORG',
    'PERSON',
    'PRODUCT',
    'WORK_OF_ART'
})

# Coarse-grained parts-of-speech tags for pronouns, proper nouns, and
# nouns.
SUBJECT_POS_TAGS: Final[frozenset[str]] = frozenset({'PRON', 'PROPN', 'NOUN'})
