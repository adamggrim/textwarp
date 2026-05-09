"""Objects used across the package for spaCy processing."""

from typing import Final

from textwarp._core.context import N_

__all__ = [
    'NOUN_TAGS',
    'POS_TAGS',
    'POS_WORD_TAGS',
]

# Coarse-grained parts-of-speech tags for singular and proper nouns.
NOUN_TAGS: Final[frozenset[str]] = frozenset({'NOUN', 'PROPN'})

# Tuple of tuples for all parts-of-speech tags and their names.
POS_TAGS: Final[tuple[tuple[str, str], ...]] = (
    ('ADJ', N_('Adjectives')),
    ('ADP', N_('Adpositions')),
    ('ADV', N_('Adverbs')),
    ('AUX', N_('Auxiliaries')),
    ('CCONJ', N_('Coordinating Conjunctions')),
    ('DET', N_('Determiners')),
    ('INTJ', N_('Interjections')),
    ('NOUN', N_('Nouns')),
    ('NUM', N_('Numbers')),
    ('PART', N_('Particles')),
    ('PRON', N_('Pronouns')),
    ('PROPN', N_('Proper Nouns')),
    ('SCONJ', N_('Subordinating Conjunctions')),
    ('VERB', N_('Verbs')),
    ('X', N_('Other'))
)

# Coarse-grained parts-of-speech tags representing words.
POS_WORD_TAGS: Final[frozenset[str]] = frozenset(
    item[0] for item in POS_TAGS if item[0] != 'X'
)
