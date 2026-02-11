"""Sets used for command-line input."""

from typing import Final

__all__ = [
    'EXIT_INPUTS',
    'NO_INPUTS',
    'YES_INPUTS'
]

# Inputs for exiting the program.
EXIT_INPUTS: Final = {'quit', 'q', 'exit', 'e'}

# Inputs for indicating a negative response.
NO_INPUTS: Final = {'no', 'n'}

# Inputs for indicating an affirmative response.
YES_INPUTS: Final = {'yes', 'y'}
