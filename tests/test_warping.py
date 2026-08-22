"""Tests for text warping functions."""

import unicodedata

import pytest
from hypothesis import given, strategies

from textwarp.warping import (
    capitalize,
    cardinal_to_ordinal,
    curly_to_straight,
    expand_contractions,
    from_binary,
    from_hexadecimal,
    from_morse,
    hyphen_to_en,
    hyphens_to_em,
    ordinal_to_cardinal,
    punct_to_inside,
    punct_to_outside,
    random_case,
    redact,
    reverse,
    straight_to_curly,
    strip_html,
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
    to_zalgo,
    unzalgo,
    widen
)

@pytest.mark.parametrize(
    'func, input_str, expected',
    [
        (capitalize, 'das kapital', 'Das Kapital'),
        (cardinal_to_ordinal, 'October 30', 'October 30th'),
        (
            curly_to_straight,
            '“Of all sweet passions Shame is the loveliest.”',
            '"Of all sweet passions Shame is the loveliest."',
        ),
        (
            expand_contractions,
            'I’m opening out like the largest telescope that ever was!',
            'I am opening out like the largest telescope that ever was!',
        ),
        (
            from_binary,
            (
                '01100011 01110010 01100101 01100001 01110100 01101001 '
                '01101111 00100000 01100101 01111000 00100000 01101110 '
                '01101001 01101000 01101001 01101100 01101111'
            ),
            'creatio ex nihilo',
        ),
        (
            from_hexadecimal,
            (
                '54 68 69 73 20 6f 6e 6c 79 20 69 73 20 74 68 65 20 77 '
                '69 74 63 68 63 72 61 66 74 20 49 20 68 61 76 65 20 75 '
                '73 65 64 2e'
            ),
            'This only is the witchcraft I have used.',
        ),
        (
            from_morse,
            (
                '.-- .... .- -   .... .- - ....   --. --- -..   .-- '
                '.-. --- ..- --. .... -'
            ),
            'WHAT HATH GOD WROUGHT',
        ),
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
            ),
        ),
        (ordinal_to_cardinal, 'October 30th', 'October 30'),
        (
            punct_to_inside,
            '“Get in, loser, we’re going shopping”.',
            '“Get in, loser, we’re going shopping.”',
        ),
        (
            punct_to_outside,
            '“You can’t sit with us.”',
            '“You can’t sit with us”.',
        ),
        (redact, 'yes I said yes I will yes', '███ █ ████ ███ █ ████ ███'),
        (reverse, 'Strike that, reverse it.', '.ti esrever ,taht ekirtS'),
        (
            straight_to_curly,
            '"There is no such thing as a moral or an immoral book."',
            '“There is no such thing as a moral or an immoral book.”',
        ),
        (strip_html, '<p>To <b>or not to </b></p>', 'To or not to '),
        (
            to_alternating_caps,
            'absorbent and yellow and porous',
            'aBsOrBeNt AnD yElLoW aNd PoRoUs'
        ),
        (
            to_binary,
            'creatio ex nihilo',
            (
                '01100011 01110010 01100101 01100001 01110100 01101001 '
                '01101111 00100000 01100101 01111000 00100000 01101110 '
                '01101001 01101000 01101001 01101100 01101111'
            ),
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
            ),
        ),
        (to_kebab_case, 'headsOnTheStakes', 'heads-on-the-stakes'),
        (to_kebab_case, 'heads.on.the.stakes', 'heads-on-the-stakes'),
        (to_kebab_case, 'HeadsOnTheStakes', 'heads-on-the-stakes'),
        (to_kebab_case, 'heads_on_the_stakes', 'heads-on-the-stakes'),
        (
            to_morse,
            'What hath God wrought',
            (
                '.-- .... .- -   .... .- - ....   --. --- -..   '
                '.-- .-. --- ..- --. .... -'
            ),
        ),
        (to_pascal_case, 'laPascaline', 'LaPascaline'),
        (to_pascal_case, 'la.pascaline', 'LaPascaline'),
        (to_pascal_case, 'la-pascaline', 'LaPascaline'),
        (to_pascal_case, 'la_pascaline', 'LaPascaline'),
        (
            to_sentence_case,
            'sentence first—verdict afterwards.',
            'Sentence first—verdict afterwards.',
        ),
        (
            to_single_spaces,
            'Mind the gap.  Mind the gap.',
            'Mind the gap. Mind the gap.',
        ),
        (to_snake_case, 'filletOfFennySnake', 'fillet_of_fenny_snake'),
        (to_snake_case, 'fillet.of.fenny.snake', 'fillet_of_fenny_snake'),
        (to_snake_case, 'fillet-of-fenny-snake', 'fillet_of_fenny_snake'),
        (to_snake_case, 'FilletOfFennySnake', 'fillet_of_fenny_snake'),
        (
            to_title_case,
            'the artist formerly known as prince (tafkap)',
            'The Artist Formerly Known as Prince (TAFKAP)',
        ),
        (unzalgo, 'n̷̡̪̈́̏á̗̣r̙̈ͫc̬͙ͪį̴́ͩs̹̙̣ͧͬs̸̟̀ů̸̬̫ś̺̣', 'narcissus'),
        (widen, 'violet beauregarde', 'v i o l e t   b e a u r e g a r d e'),
    ],
)
def test_deterministic_warping_functions(func, input_str, expected):
    assert func(input_str) == expected


def test_random_case():
    input_str = 'Tell all the truth but tell it slant.'
    result = random_case(input_str)

    # Check that the function changes casing while preserving length and
    # characters.
    assert len(result) == len(input_str)
    assert result.lower() == input_str.lower()


def test_to_zalgo():
    original_text = (
        'For every sin that he committed, a stain would fleck and wreck its '
        'fairness.'
    )
    zalgonized_text = to_zalgo(original_text)

    # Zalgonized text should be longer than the original.
    assert len(zalgonized_text) > len(original_text)

    assert unzalgo(zalgonized_text) == original_text


def test_to_zalgo_unicode():
    original_text = (
        'Un rire de démon, un rire qu’on ne peut avoir que lorsqu’on n’est '
        'plus homme, éclata sur le visage livide du prêtre.'
    )
    zalgonized_text = to_zalgo(original_text)

    cleaned_text = unzalgo(zalgonized_text)

    assert (
        unicodedata.normalize('NFC', cleaned_text)
        == unicodedata.normalize('NFC', original_text)
    )


@given(strategies.text())
def test_zalgo_stripping(s):
    assert unzalgo(to_zalgo(s)) == unzalgo(s)
