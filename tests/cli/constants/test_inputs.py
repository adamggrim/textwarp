"""Tests for command-line input sets."""

from textwarp._cli.constants.inputs import EXIT_INPUTS, NO_INPUTS, YES_INPUTS


def test_input_sets_are_frozensets():
    """
    Verify that input collections are immutable `frozenset` objects.
    """
    assert isinstance(EXIT_INPUTS, frozenset)
    assert isinstance(NO_INPUTS, frozenset)
    assert isinstance(YES_INPUTS, frozenset)


def test_yes_inputs():
    """Test affirmative input values."""
    assert 'yes' in YES_INPUTS
    assert 'y' in YES_INPUTS


def test_no_inputs():
    """Test negative input values."""
    assert 'no' in NO_INPUTS
    assert 'n' in NO_INPUTS


def test_exit_inputs():
    """Test exit input values."""
    assert 'quit' in EXIT_INPUTS
    assert 'exit' in EXIT_INPUTS
    assert 'q' in EXIT_INPUTS
    assert 'e' in EXIT_INPUTS
    assert 'exit, pursued by a bear' not in EXIT_INPUTS


def test_inputs_are_mutually_exclusive():
    """
    Ensure there is no overlap between affirmative, negative, and exit
    commands.
    """
    assert YES_INPUTS.isdisjoint(NO_INPUTS), (
        'Overlap between YES and NO inputs.'
    )
    assert YES_INPUTS.isdisjoint(EXIT_INPUTS), (
        'Overlap between YES and EXIT inputs.'
    )
    assert NO_INPUTS.isdisjoint(EXIT_INPUTS), (
        'Overlap between NO and EXIT inputs.'
    )
