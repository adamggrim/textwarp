import gettext

_ = gettext.gettext

__all__ = [
    'get_exit_inputs',
    'get_no_inputs',
    'get_yes_inputs'
]


def get_exit_inputs() -> frozenset[str]:
    """Get a cached `frozenset` of inputs for exiting the program."""
    _ = gettext.gettext
    return frozenset({_('quit'), _('q'), _('exit'), _('e')})


def get_no_inputs() -> frozenset[str]:
    """
    Get a cached `frozenset` of inputs for indicating a negative
    response.
    """
    _ = gettext.gettext
    return frozenset({
        _('no'),
        _('n')
    })


def get_yes_inputs() -> frozenset[str]:
    """
    Get a cached `frozenset` of inputs for indicating an affirmative
    response.
    """
    _ = gettext.gettext
    return frozenset({
        _('yes'),
        _('y')
    })
