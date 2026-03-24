"""Tests for warping functions."""

import pytest

from textwarp.warping import (
    capitalize,
    cardinal_to_ordinal,
    curly_to_straight,
    expand_contractions,
    from_binary,
    from_hexadecimal,
    from_morse,
    hyphens_to_em,
    hyphen_to_en,
    ordinal_to_cardinal,
    punct_to_inside,
    punct_to_outside,
    random_case,
    randomize,
    redact,
    reverse,
    straight_to_curly,
    to_alternating_caps,
    to_binary,
    to_camel_case,
    to_dot_case,
    to_hexadecimal,
    to_kebab_case,
    to_morse,
    to_pascal_case,
    to_sentence_case,
    to_single_spaces,
    to_snake_case,
    to_title_case,
    widen
)

@pytest.mark.parametrize('func, input_str, expected', [
    (capitalize, 'divina commedia', 'Divina Commedia'),
    (cardinal_to_ordinal, 'October 30', 'October 30th'),
    (curly_to_straight, '“All art is quite useless.”',
     '"All art is quite useless."'),
    (expand_contractions, 'I’d prefer not to.', 'I would prefer not to.'),
    (from_binary,
     '01100011 01110010 01100101 01100001 01110100 01101001 01101111 00100000 '
     '01100101 01111000 00100000 01101110 01101001 01101000 01101001 01101100 '
     '01101111', 'creatio ex nihilo'),
    (from_hexadecimal, '54 68 69 73 20 6f 6e 6c 79 20 69 73 20 74 68 65 20 77 '
     '69 74 63 68 63 72 61 66 74 20 49 20 68 61 76 65 20 75 73 65 64 2e',
     'This only is the witchcraft I have used.'),
    (from_morse, '.-- .... .- -   .... .- - ....   --. --- -..   .-- .-. --- '
     '..- --. .... -', 'WHAT HATH GOD WROUGHT'),
    (hyphens_to_em, 'Call me Ishmael. (Some years ago--never mind how long '
     'precisely--)', 'Call me Ishmael. (Some years ago—never mind how long '
     'precisely—)'),
    (hyphen_to_en, 'Books I-XII', 'Books I–XII'),
    (ordinal_to_cardinal, 'October 30th', 'October 30'),
    (punct_to_inside, '“To be, or not to be, that is the question”.',
     '“To be, or not to be, that is the question.”'),
    (punct_to_outside, '“To be, or not to be, that is the question.”',
     '“To be, or not to be, that is the question”.'),
    (redact, 'yes I said yes I will yes', '███ █ ████ ███ █ ████ ███'),
    (reverse, 'reverse', 'esrever'),
    (straight_to_curly, '"All art is quite useless."',
     '“All art is quite useless.”'),
    (to_alternating_caps, 'alternating caps', 'aLtErNaTiNg CaPs'),
    (to_binary, 'creatio ex nihilo', '01100011 01110010 01100101 01100001 '
     '01110100 01101001 01101111 00100000 01100101 01111000 00100000 01101110 '
     '01101001 01101000 01101001 01101100 01101111'),
    (to_camel_case, 'camel.case, camel-case, CamelCase, camel_case',
     'camelCase, camelCase, camelCase, camelCase'),
    (to_dot_case, 'dotCase, dot-case, DotCase, dot_case',
     'dot.case, dot.case, dot.case, dot.case'),
    (to_hexadecimal, 'This only is the witchcraft I have used.',
     '54 68 69 73 20 6f 6e 6c 79 20 69 73 20 74 68 65 20 77 69 74 63 68 63 72 '
     '61 66 74 20 49 20 68 61 76 65 20 75 73 65 64 2e'),
    (to_kebab_case, 'kebabCase, kebab.case, KebabCase, kebab_case',
     'kebab-case, kebab-case, kebab-case, kebab-case'),
    (to_morse, 'What hath God wrought', '.-- .... .- -   .... .- - ....   --. '
     '--- -..   .-- .-. --- ..- --. .... -'),
    (to_pascal_case, 'pascalCase, pascal.case, pascal-case, pascal_case',
     'PascalCase, PascalCase, PascalCase, PascalCase'),
    (to_sentence_case, 'mrs. dalloway said she would buy the flowers herself. '
     'for lucy had her work cut out for her.', 'Mrs. dalloway said she would '
     'buy the flowers herself. For lucy had her work cut out for her.'),
    (to_single_spaces, 'The past is never dead.  In fact, it’s not even past.',
     'The past is never dead. In fact, it’s not even past.'),
    (to_snake_case, 'snakeCase, snake.case, snake-case, SnakeCase',
     'snake_case, snake_case, snake_case, snake_case'),
    (to_title_case, 'the tragical history of the life and death of doctor '
     'faustus', 'The Tragical History of the Life and Death of Doctor Faustus'),
    (widen, 'widen', 'w i d e n')
])
def test_deterministic_warping_functions(func, input_str, expected):
    """
    Test warping functions that have deterministic outputs.
    """
    assert func(input_str) == expected


def test_random_case():
    """Test random casing."""
    input_str = 'random case'
    result = random_case(input_str)

    # Check that the function changes casing while preserving length and
    # characters.
    assert len(result) == len(input_str)
    assert result.lower() == input_str.lower()


def test_randomize():
    """Test randomization."""
    input_str = 'randomize'
    result = randomize(input_str)

    # Check that the function shuffles character order while preserving
    # the characters.
    assert len(result) == len(input_str)
    assert sorted(result) == sorted(input_str)
