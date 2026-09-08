"""Tests for command-line arguments mapping and lazy loading."""

import pytest

from textwarp._cli.args import (
    ARGS_MAP,
    CLICommand,
    CommandType,
    _lazy_load
)


def test_lazy_load():
    lazy_func = _lazy_load('.._lib.casing', 'to_title_case')

    assert callable(lazy_func)
    assert lazy_func('bartleby, the scrivener') == 'Bartleby, the Scrivener'


def test_args_map_structure():
    """
    Test that every entry in `ARGS_MAP` is a properly configured CLICommand.
    """
    for cmd_name, cmd in ARGS_MAP.items():
        assert isinstance(cmd_name, str), (
            f'Command name {cmd_name} is not a string.'
        )
        assert isinstance(cmd, CLICommand), (
            f'Value for {cmd_name} is not a CLICommand.'
        )
        assert callable(cmd.func), (
            f'The function mapped to {cmd_name} is not callable.'
        )
        assert isinstance(cmd.help_text, str), (
            f'The help text for {cmd_name} is not a string.'
        )
        assert len(cmd.help_text.strip()) > 0, (
            f'The help text for {cmd_name} is empty.'
        )
        assert isinstance(cmd.command_type, CommandType), (
            f'The command type for {cmd_name} is not a valid CommandType.'
        )


@pytest.mark.parametrize(
    'command, input_text, expected_output',
    [
        ('clear', 'Out, out, brief candle!', ''),
        (
            'lowercase',
            'LOOK ON MY WORKS, YE MIGHTY',
            'look on my works, ye mighty',
        ),
        (
            'plain-text',
            'An honest tale speeds best being plainly told.',
            'An honest tale speeds best being plainly told.',
        ),
        ('strip', '  off, you lendings  ', 'off, you lendings'),
        (
            'swapcase',
            'fAIR iS fOUL, aND fOUL iS fAIR',
            'Fair Is Foul, And Foul Is Fair',
        ),
        ('uppercase', 'i sound my barbaric yawp', 'I SOUND MY BARBARIC YAWP'),
    ],
)
def test_built_in_string_functions(command, input_text, expected_output):
    func = ARGS_MAP[command].func
    assert func(input_text) == expected_output
