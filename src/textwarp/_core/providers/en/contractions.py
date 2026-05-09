"""Sets used in English contraction variants."""

from typing import Final

__all__ = [
    'AIN_T_SUFFIX_VARIANTS',
    'APOSTROPHE_D_VARIANTS',
    'APOSTROPHE_S_VARIANTS'
]

# Variants of "'s" for contractions.
AIN_T_SUFFIX_VARIANTS: Final[frozenset[str]] = frozenset({
    "n't",
    'n’t',
    'n‘t'
})

# Variants of "'d" for contractions.
APOSTROPHE_D_VARIANTS: Final[frozenset[str]] = frozenset({
    "'d",
    '’d',
    '‘d'
})

# Variants of "'s" for contractions.
APOSTROPHE_S_VARIANTS: Final[frozenset[str]] = frozenset({
    "'s",
    '’s',
    '‘s'
})
