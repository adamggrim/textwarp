"""Tests for text encoding and decoding functions."""

import regex as re
from hypothesis import given, strategies

from textwarp._lib.encoding import (
    from_binary,
    from_hexadecimal,
    from_morse,
    to_binary,
    to_hexadecimal,
    to_morse
)

_MORSE_WORD_GAP_PATTERN = re.compile(r'(?<=[.-]) {3}(?=[.-])')
_MORSE_CHAR_GAP_PATTERN = re.compile(r'(?<=[.-]) (?=[.-])')


def test_binary_conversion():
    original = 'Harriot'
    binary = to_binary(original)

    assert binary == (
        '01001000 01100001 01110010 01110010 01101001 01101111 01110100'
    )
    assert from_binary(binary) == original


def test_binary_invalid_input_pass_through():
    text = (
        'Gottfried Wilhelm 01001100 01100101 01101001 01100010 01101110 '
        '01101001 01111010'
    )
    assert from_binary(text) == text


def test_hexadecimal_conversion():
    original = (
        'I saw Sarah Good with the Devil! I saw Goody Osburn with the Devil! '
        'I saw Bridget Bishop with the Devil!'
    )
    hex_str = to_hexadecimal(original)

    assert hex_str == (
        '49 20 73 61 77 20 53 61 72 61 68 20 47 6f 6f 64 20 77 69 74 68 20 74 '
        '68 65 20 44 65 76 69 6c 21 20 49 20 73 61 77 20 47 6f 6f 64 79 20 4f '
        '73 62 75 72 6e 20 77 69 74 68 20 74 68 65 20 44 65 76 69 6c 21 20 49 '
        '20 73 61 77 20 42 72 69 64 67 65 74 20 42 69 73 68 6f 70 20 77 69 74 '
        '68 20 74 68 65 20 44 65 76 69 6c 21'
    )
    assert from_hexadecimal(hex_str) == original


def test_hexadecimal_invalid_input_pass_through():
    text = 'These things must be done delicately, or you hurt the spell.'
    assert from_hexadecimal(text) == text


def test_morse_conversion_basic():
    original = 'SOS'
    morse = to_morse(original)

    assert morse == '... --- ...'
    assert from_morse(morse) == original


def test_morse_conversion_complex():
    original = (
        'May both oceans be dry before a foot of all the land that lies '
        'between them shall belong to any other than one united country.'
    )
    morse = to_morse(original)

    morse_irreg_word_spacing = _MORSE_WORD_GAP_PATTERN.sub(
        lambda _: ' ' * 24,
        morse
    )
    morse_irreg_spacing = _MORSE_CHAR_GAP_PATTERN.sub(
        lambda _: ' ' * 5,
        morse_irreg_word_spacing
    )

    expected = (
        '-- .- -.--   -... --- - ....   --- -.-. . .- -. ...   -... .   '
        '-.. .-. -.--   -... . ..-. --- .-. .   .-   ..-. --- --- -   '
        '--- ..-.   .- .-.. .-..   - .... .   .-.. .- -. -..   - .... .- -   '
        '.-.. .. . ...   -... . - .-- . . -.   - .... . --   '
        '... .... .- .-.. .-..   -... . .-.. --- -. --.   - ---   '
        '.- -. -.--   --- - .... . .-.   - .... .- -.   --- -. .   '
        '..- -. .. - . -..   -.-. --- ..- -. - .-. -.-- .-.-.-'
    )
    assert morse == expected
    assert from_morse(morse) == original.upper()
    assert from_morse(morse_irreg_spacing) == original.upper()


def test_morse_invalid_input_pass_through():
    text = (
        'We intend to begin on the first of February unrestricted submarine '
        'warfare. We shall endeavor in spite of this to keep the United '
        'States of America neutral.'
    )
    assert from_morse(text) == text


def test_morse_conversion_unsupported_chars():
    original = 'A * B'
    morse = to_morse(original)

    assert morse == '.-   -...'


def test_morse_conversion_dashes():
    """Test that dashes are normalized to hyphens for Morse code."""
    original = 'A—Z'
    morse = to_morse(original)

    assert morse == '.- -....- --..'


@given(strategies.text())
def test_binary_symmetry(s):
    assert from_binary(to_binary(s)) == s


@given(strategies.text())
def test_hexadecimal_symmetry(s):
    assert from_hexadecimal(to_hexadecimal(s)) == s
