"""Tests for text encoding and decoding functions."""

from textwarp._lib.encoding import (
    from_binary,
    from_hexadecimal,
    from_morse,
    to_binary,
    to_hexadecimal,
    to_morse
)


def test_binary_conversion():
    """Test converting to and from binary strings."""
    original = 'Turing'
    binary = to_binary(original)

    assert binary == '01010100 01110101 01110010 01101001 01101110 01100111'
    assert from_binary(binary) == original


def test_hexadecimal_conversion():
    """Test converting to and from hexadecimal strings."""
    original = 'This only is the witchcraft I have used.'
    hex_str = to_hexadecimal(original)

    assert hex_str == (
        '54 68 69 73 20 6f 6e 6c 79 20 69 73 20 74 68 65 20 77 69 74 '
        '63 68 63 72 61 66 74 20 49 20 68 61 76 65 20 75 73 65 64 2e'
    )
    assert from_hexadecimal(hex_str) == original


def test_morse_conversion_basic():
    """Test converting standard alphanumeric text to Morse code."""
    original = 'SOS'
    morse = to_morse(original)

    assert morse == '... --- ...'
    assert from_morse(morse) == original


def test_morse_conversion_complex():
    """Test converting words, spaces and punctuation to Morse code."""
    text = 'What hath God wrought?'
    morse = to_morse(text)

    expected = (
        '.-- .... .- -   .... .- - ....   --. --- -..   .-- .-. --- '
        '..- --. .... - ..--..'
    )
    assert morse == expected
    assert from_morse(morse) == text.upper()


def test_morse_conversion_unsupported_chars():
    """Test unsupported characters ignored during Morse conversion."""
    text = 'A * B'
    morse = to_morse(text)

    assert morse == '.-   -...'


def test_morse_conversion_dashes():
    """
    Test that em and en dashes are normalized to hyphens for Morse.
    """
    text = 'A—Z'
    morse = to_morse(text)

    assert morse == '.- -....- --..'
