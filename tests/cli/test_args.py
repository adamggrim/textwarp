"""Tests for command-line arguments mapping and lazy loading."""

import pytest

from textwarp._cli.args import (
    ARGS_MAP,
    CASING_COMMANDS,
    MUTUALLY_EXCLUSIVE_COMMANDS,
    SEPARATOR_COMMANDS,
    _lazy_load
)


def test_lazy_load():
    """Test that `_lazy_load` correctly imports a module and function."""
    lazy_func = _lazy_load('..warping', 'reverse')

    assert callable(lazy_func)
    assert lazy_func('textwarp') == 'prawtxet'


def test_args_map_structure():
    """
    Test that every entry in `ARGS_MAP` has a valid callable function
    and help string.
    """
    for cmd_name, (func, help_text) in ARGS_MAP.items():
        assert isinstance(cmd_name, str), (
            f'Command name {cmd_name} is not a string.'
        )
        assert callable(func), (
            f'The function mapped to {cmd_name} is not callable.'
        )
        assert isinstance(help_text, str), (
            f'The help text for {cmd_name} is not a string.'
        )
        assert len(help_text.strip()) > 0, (
            f'The help text for {cmd_name} is empty.'
        )


def test_command_sets_validity():
    """
    Test that all commands in the command sets are in `ARGS_MAP`.
    """
    all_mapped_commands = set(ARGS_MAP.keys())

    assert CASING_COMMANDS.issubset(all_mapped_commands), (
        'Unknown command in CASING_COMMANDS.'
    )
    assert SEPARATOR_COMMANDS.issubset(all_mapped_commands), (
        'Unknown command in SEPARATOR_COMMANDS.'
    )
    assert MUTUALLY_EXCLUSIVE_COMMANDS.issubset(all_mapped_commands), (
        'Unknown command in MUTUALLY_EXCLUSIVE_COMMANDS.'
    )


def test_mutually_exclusive_sets():
    """
    Test that mutually exclusive commands do not overlap with combinable
    command sets.
    """
    assert CASING_COMMANDS.isdisjoint(MUTUALLY_EXCLUSIVE_COMMANDS), (
        'Overlap found between casing and mutually exclusive commands.'
    )
    assert SEPARATOR_COMMANDS.isdisjoint(MUTUALLY_EXCLUSIVE_COMMANDS), (
        'Overlap found between separator and mutually exclusive commands.'
    )


@pytest.mark.parametrize('command, input_text, expected_output', [
    ('clear', 'some text', 'some text'),
    ('lowercase', 'MIXed Case', 'mixed case'),
    ('plain-text', 'just text', 'just text'),
    ('strip', '  padded  ', 'padded'),
    ('swapcase', 'sWAP mE', 'Swap Me'),
    ('uppercase', 'make me loud', 'MAKE ME LOUD'),
])
def test_built_in_string_functions(command, input_text, expected_output):
    """
    Test the commands in `ARGS_MAP` that map directly to built-in
    string methods or lambdas.
    """
    func = ARGS_MAP[command][0]
    assert func(input_text) == expected_output
