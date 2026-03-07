"""Sets for command-line input."""

from typing import Final

__all__ = [
    'EXIT_INPUTS',
    'NO_INPUTS',
    'YES_INPUTS'
]

# Inputs for exiting the program.
EXIT_INPUTS: Final[frozenset[str]] = frozenset({'quit', 'q', 'exit', 'e'})

# Inputs for indicating a negative response.
NO_INPUTS: Final[frozenset[str]] = frozenset({'no', 'n'})

# Inputs for indicating an affirmative response.
YES_INPUTS: Final[frozenset[str]] = frozenset({'yes', 'y'})
