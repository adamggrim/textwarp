"""Sets used across the package for variants and input."""

from typing import Final

__all__ = [
    'AIN_T_SUFFIX_VARIANTS',
    'APOSTROPHE_D_VARIANTS',
    'APOSTROPHE_S_VARIANTS',
    'APOSTROPHE_VARIANTS',
    'EXIT_INPUTS',
    'NO_INPUTS',
    'OPEN_QUOTES',
    'YES_INPUTS'
]

# Variants of 's for contractions.
AIN_T_SUFFIX_VARIANTS: Final = {"n't", 'n’t', 'n‘t'}

# Variants of 'd for contractions.
APOSTROPHE_D_VARIANTS: Final = {"'d", '’d', '‘d'}

# Variants of 's for contractions.
APOSTROPHE_S_VARIANTS: Final = {"'s", '’s', '‘s'}

# Variants of apostrophes.
APOSTROPHE_VARIANTS: Final = {"'", '’', '‘'}

# Inputs for exiting the program.
EXIT_INPUTS: Final = {'quit', 'q', 'exit', 'e'}

# Inputs for indicating a negative response.
NO_INPUTS: Final = {'no', 'n'}

# Opening quote characters.
OPEN_QUOTES: Final = {'"', '“', "'", '‘'}

# Inputs for indicating an affirmative response.
YES_INPUTS: Final = {'yes', 'y'}
