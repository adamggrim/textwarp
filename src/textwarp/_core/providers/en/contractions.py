"""Sets used in English contraction variants."""

from typing import Final

__all__ = [
    'AIN_T_SUFFIX_VARIANTS',
    'APOSTROPHE_D_VARIANTS',
    'APOSTROPHE_S_VARIANTS'
]

AIN_T_SUFFIX_VARIANTS: Final[frozenset[str]] = frozenset({
    "n't",
    'n’t',
    'n‘t'
})

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
