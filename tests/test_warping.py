"""Tests for text warping functions."""

import pytest

from textwarp.warping import (
    capitalize,
    cardinal_to_ordinal,
    curly_to_straight,
    expand_contractions,
    from_binary,
    from_hexadecimal,
    from_morse,
    from_zalgo,
    hyphen_to_en,
    hyphens_to_em,
    ordinal_to_cardinal,
    punct_to_inside,
    punct_to_outside,
    random_case,
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
    (
        curly_to_straight,
        '“All art is quite useless.”',
        '"All art is quite useless."'
    ),
    (
        expand_contractions,
        'I’m opening out like the largest telescope that ever was!',
        'I am opening out like the largest telescope that ever was!'),
    (
        from_binary,
        (
            '01100011 01110010 01100101 01100001 01110100 01101001 '
            '01101111 00100000 01100101 01111000 00100000 01101110 '
            '01101001 01101000 01101001 01101100 01101111'
        ),
        'creatio ex nihilo'
    ),
    (
        from_hexadecimal,
        (
            '54 68 69 73 20 6f 6e 6c 79 20 69 73 20 74 68 65 20 77 '
            '69 74 63 68 63 72 61 66 74 20 49 20 68 61 76 65 20 75 '
            '73 65 64 2e'
        ),
        'This only is the witchcraft I have used.'
    ),
    (
        from_morse,
        (
            '.-- .... .- -   .... .- - ....   --. --- -..   .-- '
            '.-. --- ..- --. .... -'
        ),
        'WHAT HATH GOD WROUGHT'
    ),
    (from_zalgo, 'ǹ̡̓a̷͕̱͒r̶̢̟ͩͤç̥ͭi̶̳̖ͬͪs͓̟s̶͗̚u̵̡͑s̵͚͑', 'narcissus'),
    (hyphen_to_en, 'Books I-XII', 'Books I–XII'),
    (
        hyphens_to_em,
        (
            'Call me Ishmael. (Some years ago--never mind how long '
            'precisely--)'
        ),
        (
            'Call me Ishmael. (Some years ago—never mind how long '
            'precisely—)'
        )
    ),
    (ordinal_to_cardinal, 'October 30th', 'October 30'),
    (
        punct_to_inside,
        '“To be, or not to be, that is the question”.',
        '“To be, or not to be, that is the question.”'
    ),
    (
        punct_to_outside,
        '“To be, or not to be, that is the question.”',
        '“To be, or not to be, that is the question”.'
    ),
    (redact, 'yes I said yes I will yes', '███ █ ████ ███ █ ████ ███'),
    (reverse, 'Strike that, reverse it.', '.ti esrever ,taht ekirtS'),
    (
        straight_to_curly,
        '"All art is quite useless."',
        '“All art is quite useless.”'
    ),
    (to_alternating_caps, 'alternating caps', 'aLtErNaTiNg CaPs'),
    (
        to_binary,
        'creatio ex nihilo',
        (
            '01100011 01110010 01100101 01100001 01110100 01101001 '
            '01101111 00100000 01100101 01111000 00100000 01101110 '
            '01101001 01101000 01101001 01101100 01101111'
        )
    ),

    (to_camel_case, 'i.see.the.camel', 'iSeeTheCamel'),
    (to_camel_case, 'i-see-the-camel', 'iSeeTheCamel'),
    (to_camel_case, 'ISeeTheCamel', 'iSeeTheCamel'),
    (to_camel_case, 'i_see_the_camel', 'iSeeTheCamel'),

    (to_dot_case, 'lookAgainAtThatDot', 'look.again.at.that.dot'),
    (to_dot_case, 'look-again-at-that-dot', 'look.again.at.that.dot'),
    (to_dot_case, 'LookAgainAtThatDot', 'look.again.at.that.dot'),
    (to_dot_case, 'look_again_at_that_dot', 'look.again.at.that.dot'),

    (
        to_hexadecimal,
        'This only is the witchcraft I have used.',
        (
            '54 68 69 73 20 6f 6e 6c 79 20 69 73 20 74 68 65 20 77 '
            '69 74 63 68 63 72 61 66 74 20 49 20 68 61 76 65 20 75 '
            '73 65 64 2e'
        )
    ),

    (to_kebab_case, 'headsOnTheStakes', 'heads-on-the-stakes'),
    (to_kebab_case, 'heads.on.the.stakes', 'heads-on-the-stakes'),
    (to_kebab_case, 'HeadsOnTheStakes', 'heads-on-the-stakes'),
    (to_kebab_case, 'heads_on_the_stakes', 'heads-on-the-stakes'),

    (
        to_morse,
        'What hath God wrought',
        (
            '.-- .... .- -   .... .- - ....   --. --- -..   .-- '
            '.-. --- ..- --. .... -'
        )
    ),

    (to_pascal_case, 'laPascaline', 'LaPascaline'),
    (to_pascal_case, 'la.pascaline', 'LaPascaline'),
    (to_pascal_case, 'la-pascaline', 'LaPascaline'),
    (to_pascal_case, 'la_pascaline', 'LaPascaline'),

    (
        to_sentence_case,
        (
            'mrs. dalloway said she would buy the flowers herself. for lucy '
            'had her work cut out for her.'
        ),
        (
            'Mrs. dalloway said she would buy the flowers herself. For lucy '
            'had her work cut out for her.'
        )
    ),
    (
        to_single_spaces,
        'The past is never dead.  In fact, it’s not even past.',
        'The past is never dead. In fact, it’s not even past.'
    ),
    (to_snake_case, 'filletOfFennySnake', 'fillet_of_fenny_snake'),
    (to_snake_case, 'fillet.of.fenny.snake', 'fillet_of_fenny_snake'),
    (to_snake_case, 'fillet-of-fenny-snake', 'fillet_of_fenny_snake'),
    (to_snake_case, 'FilletOfFennySnake', 'fillet_of_fenny_snake'),
    (
        to_title_case,
        'the tragical history of the life and death of doctor faustus',
        'The Tragical History of the Life and Death of Doctor Faustus'
    ),
    (widen, 'violet beauregarde', 'v i o l e t   b e a u r e g a r d e')
])
def test_deterministic_warping_functions(func, input_str, expected):
    assert func(input_str) == expected


def test_random_case():
    input_str = 'Tell all the truth but tell it slant.'
    result = random_case(input_str)

    # Check that the function changes casing while preserving length and
    # characters.
    assert len(result) == len(input_str)
    assert result.lower() == input_str.lower()
