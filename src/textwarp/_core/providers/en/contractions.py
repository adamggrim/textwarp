"""Sets used in English contraction variants."""

from typing import Final

__all__ = [
    'APOSTROPHE_D_VARIANTS',
    'APOSTROPHE_S_VARIANTS',
    'N_T_SUFFIX_VARIANTS'

]

APOSTROPHE_D_VARIANTS: Final[frozenset[str]] = frozenset({
    "'d",
    '’d',
    '‘d'
})

APOSTROPHE_S_VARIANTS: Final[frozenset[str]] = frozenset({
    "'s",
    '’s',
    '‘s'
})

N_T_SUFFIX_VARIANTS: Final[frozenset[str]] = frozenset({
    "n't",
    'n’t',
    'n‘t'
})
