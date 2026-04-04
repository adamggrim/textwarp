"""Objects used across the package for spaCy processing."""

from typing import Final

__all__ = [
    'NOUN_TAGS',
    'POS_TAGS',
    'POS_WORD_TAGS',
]

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
