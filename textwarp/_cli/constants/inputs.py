import gettext
from typing import Final

_ = gettext.gettext

__all__ = [
    'EXIT_INPUTS',
    'NO_INPUTS',
    'YES_INPUTS'
]

# Inputs for exiting the program.
EXIT_INPUTS: Final[frozenset[str]] = frozenset(
    {_('quit'), _('q'), _('exit'), _('e')}
)

# Inputs for indicating a negative response.
NO_INPUTS: Final[frozenset[str]] = frozenset({_('no'), _('n')})

# Inputs for indicating an affirmative response.
YES_INPUTS: Final[frozenset[str]] = frozenset({_('yes'), _('y')})
