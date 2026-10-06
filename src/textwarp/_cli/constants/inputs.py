"""Sets for accepted CLI inputs."""

from textwarp._core.context import _

__all__ = [
    'get_exit_inputs',
    'get_no_inputs',
    'get_yes_inputs'
]


def get_exit_inputs() -> frozenset[str]:
    """Get a `frozenset` of inputs for exiting the program."""
    return frozenset({_('quit'), _('q'), _('exit'), _('e')})


def get_no_inputs() -> frozenset[str]:
    """
    Get a `frozenset` of inputs for indicating a negative
    response.
    """
    return frozenset({
        _('no'),
        _('n')
    })


def get_yes_inputs() -> frozenset[str]:
    """
    Get a `frozenset` of inputs for indicating an affirmative
    response.
    """
    return frozenset({
        _('yes'),
        _('y')
    })
