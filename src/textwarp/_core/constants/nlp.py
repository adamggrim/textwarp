"""Objects used across the package for spaCy processing."""

from typing import Final

from textwarp._core.context import N_
from textwarp._core.enums import POSTag

__all__ = [
    'NOUN_TAGS',
    'POS_TAGS',
    'POS_WORD_TAGS'
]

NOUN_TAGS: Final[frozenset[POSTag]] = frozenset({POSTag.NOUN, POSTag.PROPN})

POS_TAGS: Final[tuple[tuple[POSTag, str], ...]] = (
    (POSTag.ADJ, N_('Adjectives')),
    (POSTag.ADP, N_('Adpositions')),
    (POSTag.ADV, N_('Adverbs')),
    (POSTag.AUX, N_('Auxiliaries')),
    (POSTag.CCONJ, N_('Coordinating Conjunctions')),
    (POSTag.DET, N_('Determiners')),
    (POSTag.INTJ, N_('Interjections')),
    (POSTag.NOUN, N_('Nouns')),
    (POSTag.NUM, N_('Numbers')),
    (POSTag.PART, N_('Particles')),
    (POSTag.PRON, N_('Pronouns')),
    (POSTag.PROPN, N_('Proper Nouns')),
    (POSTag.SCONJ, N_('Subordinating Conjunctions')),
    (POSTag.VERB, N_('Verbs')),
    (POSTag.X, N_('Other'))
)

POS_WORD_TAGS: Final[frozenset[POSTag]] = frozenset(
    item[0] for item in POS_TAGS if item[0] != POSTag.X
)
