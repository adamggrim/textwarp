"""Tests for command-line input sets."""

from textwarp._cli.constants.inputs import (
    get_exit_inputs,
    get_no_inputs,
    get_yes_inputs
)


def test_input_sets_are_frozensets():
    assert isinstance(get_exit_inputs(), frozenset)
    assert isinstance(get_no_inputs(), frozenset)
    assert isinstance(get_yes_inputs(), frozenset)


def test_yes_inputs():
    assert 'yes' in get_yes_inputs()
    assert 'y' in get_yes_inputs()


def test_no_inputs():
    assert 'no' in get_no_inputs()
    assert 'n' in get_no_inputs()


def test_exit_inputs():
    assert 'quit' in get_exit_inputs()
    assert 'exit' in get_exit_inputs()
    assert 'q' in get_exit_inputs()
    assert 'e' in get_exit_inputs()
    assert 'exit, pursued by a bear' not in get_exit_inputs()


def test_inputs_are_mutually_exclusive():
    assert get_yes_inputs().isdisjoint(get_no_inputs()), (
        'Overlap between YES and NO inputs.'
    )
    assert get_yes_inputs().isdisjoint(get_exit_inputs()), (
        'Overlap between YES and EXIT inputs.'
    )
    assert get_no_inputs().isdisjoint(get_exit_inputs()), (
        'Overlap between NO and EXIT inputs.'
    )
