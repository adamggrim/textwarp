"""Sets used across the package for variants and input."""

from typing import Final

__all__ = [
    'AIN_T_SUFFIX_VARIANTS',
    'APOSTROPHE_D_VARIANTS',
    'APOSTROPHE_S_VARIANTS',
    'OPEN_QUOTES'
]

# Variants of 's for contractions.
AIN_T_SUFFIX_VARIANTS: Final = {"n't", 'n’t', 'n‘t'}

# Variants of 'd for contractions.
APOSTROPHE_D_VARIANTS: Final = {"'d", '’d', '‘d'}

# Variants of 's for contractions.
APOSTROPHE_S_VARIANTS: Final = {"'s", '’s', '‘s'}

# Opening quote characters.
OPEN_QUOTES: Final = {'"', '“', "'", '‘'}
