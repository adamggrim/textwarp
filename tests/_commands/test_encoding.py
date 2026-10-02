"""Tests for CLI encoding command wrappers."""

from textwarp._commands import encoding


def test_from_binary_invalid_input_pass_through():
    text = ('George 01000010 01101111 01101111 01101100 01100101')
    assert encoding.from_binary(text) == text


def test_from_hexadecimal_invalid_input_pass_through():
    text = 'She has magic in her fingers and devilry dancing in her blood.'
    assert encoding.from_hexadecimal(text) == text


def test_from_morse_invalid_input_pass_through():
    text = (
        'The people of California desire to congratulate you upon the '
        'completion of the great work.'
    )
    assert encoding.from_morse(text) == text
