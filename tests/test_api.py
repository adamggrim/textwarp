"""Tests for public API functions."""

import pytest
import textwarp


@pytest.mark.parametrize(
    'func_name, text, expected',
    [
        (
            'calculate_ttr',
            (
                'Bent double, like old beggars under sacks,\n'
                'Knock-kneed, coughing like hags, we cursed through sludge,\n'
                'Till on the haunting flares we turned our backs\n'
                'And towards our distant rest began to trudge.'
            ),
            None
        ),
        ('capitalize', 'das kapital', 'Das Kapital'),
        ('cardinal_to_ordinal', 'October 30', 'October 30th'),
        ('count_chars', 'Six Characters in Search of an Author', 37),
        (
            'count_lines',
            (
                'I keep a close watch on this heart of mine.\n'
                'I keep my eyes wide open all the time.\n'
                'I keep the ends out for the tie that binds.'
            ),
            3
        ),
        ('count_pos', 'Colorless green ideas sleep furiously.', None),
        (
            'count_sents',
            (
                'Vigorous writing is concise. A sentence should contain no '
                'unnecessary words.'
            ),
            2
        ),
        ('count_words', 'Words, words, words.', 3),
        (
            'curly_to_straight',
            '“Of all sweet passions Shame is the loveliest.”',
            '"Of all sweet passions Shame is the loveliest."',
        ),
        (
            'expand_contractions',
            'I’m opening out like the largest telescope that ever was!',
            'I am opening out like the largest telescope that ever was!',
        ),
        (
            'from_binary',
            (
                '01100011 01110010 01100101 01100001 01110100 01101001 '
                '01101111 00100000 01100101 01111000 00100000 01101110 '
                '01101001 01101000 01101001 01101100 01101111'
            ),
            'creatio ex nihilo',
        ),
        (
            'from_hexadecimal',
            (
                '54 68 69 73 20 6f 6e 6c 79 20 69 73 20 74 68 65 20 77 '
                '69 74 63 68 63 72 61 66 74 20 49 20 68 61 76 65 20 75 '
                '73 65 64 2e'
            ),
            'This only is the witchcraft I have used.',
        ),
        (
            'from_morse',
            (
                '.-- .... .- -   .... .- - ....   --. --- -..   .-- '
                '.-. --- ..- --. .... -'
            ),
            'WHAT HATH GOD WROUGHT',
        ),
        (
            'hyphens_to_em',
            (
                'Call me Ishmael. (Some years ago--never mind how long '
                'precisely--)'
            ),
            (
                'Call me Ishmael. (Some years ago—never mind how long '
                'precisely—)'
            ),
        ),
        ('hyphens_to_en', 'Books I-XII', 'Books I–XII'),
        ('ordinal_to_cardinal', 'October 30th', 'October 30'),
        (
            'punct_to_inside',
            '“Get in, loser, we’re going shopping”.',
            '“Get in, loser, we’re going shopping.”',
        ),
        (
            'punct_to_outside',
            '“You can’t sit with us.”',
            '“You can’t sit with us”.',
        ),
        ('random_case', 'Tell all the truth but tell it slant.', None),
        ('randomize', 'shaken, not stirred', None),
        (
            'redact',
            'yes I said yes I will yes',
            '███ █ ████ ███ █ ████ ███'
        ),
        ('reverse', 'Strike that, reverse it.', '.ti esrever ,taht ekirtS'),
        (
            'straight_to_curly',
            '"There is no such thing as a moral or an immoral book."',
            '“There is no such thing as a moral or an immoral book.”',
        ),
        ('strip_html', '<p>To <b>or not to </b></p>', 'To or not to '),
        (
            'to_alternating_caps',
            'absorbent and yellow and porous',
            'aBsOrBeNt AnD yElLoW aNd PoRoUs'
        ),
        (
            'to_binary',
            'creatio ex nihilo',
            (
                '01100011 01110010 01100101 01100001 01110100 01101001 '
                '01101111 00100000 01100101 01111000 00100000 01101110 '
                '01101001 01101000 01101001 01101100 01101111'
            ),
        ),
        ('to_camel_case', 'i.see.the.camel', 'iSeeTheCamel'),
        ('to_dot_case', 'lookAgainAtThatDot', 'look.again.at.that.dot'),
        (
            'to_hexadecimal',
            'This only is the witchcraft I have used.',
            (
                '54 68 69 73 20 6f 6e 6c 79 20 69 73 20 74 68 65 20 77 '
                '69 74 63 68 63 72 61 66 74 20 49 20 68 61 76 65 20 75 '
                '73 65 64 2e'
            ),
        ),
        ('to_kebab_case', 'headsOnTheStakes', 'heads-on-the-stakes'),
        (
            'to_morse',
            'What hath God wrought',
            (
                '.-- .... .- -   .... .- - ....   --. --- -..   '
                '.-- .-. --- ..- --. .... -'
            ),
        ),
        ('to_pascal_case', 'laPascaline', 'LaPascaline'),
        (
            'to_sentence_case',
            'sentence first—verdict afterwards.',
            'Sentence first—verdict afterwards.',
        ),
        (
            'to_single_spaces',
            'Mind the gap.  Mind the gap.',
            'Mind the gap. Mind the gap.',
        ),
        ('to_snake_case', 'filletOfFennySnake', 'fillet_of_fenny_snake'),
        (
            'to_title_case',
            'the artist formerly known as prince (tafkap)',
            'The Artist Formerly Known as Prince (TAFKAP)',
        ),
        (
            'to_zalgo',
            'Dorian Gray',
            None
        ),
        ('unzalgo', 'n̼̫̥͐a͓̣͛r̠̮̓c̷͓̘̪̊i̵̧͚̅̃s̫̮̑s̩̣ͯu̮͑ͣṡ̹̩́', 'narcissus'),
        (
            'widen',
            'violet beauregarde',
            'v i o l e t   b e a u r e g a r d e'
        ),
    ]
)
def test_single_arg_functions(func_name, text, expected):
    """
    Verify that single-argument API functions correctly lazy load,
    route to their underlying implementations, and execute.
    """
    func = getattr(textwarp, func_name)
    result = func(text)

    if expected is not None:
        if isinstance(expected, list):
            assert isinstance(result, list)
        else:
            assert result == expected
    else:
        assert result is not None


@pytest.mark.parametrize(
    'func_name, text, param, expected',
    [
        ('calculate_time_to_read', 'A time to be born, a time to die', 300, 1),
        ('count_entities', 'Count von Count', 1, []),
        (
            'count_mfws',
            'Put out the light, and then put out the light.',
            1,
            []
        ),
    ]
)
def test_two_arg_functions(func_name, text, param, expected):
    """
    Verify that two-argument API functions correctly lazy load,
    route to their underlying implementations, and execute.
    """
    func = getattr(textwarp, func_name)
    result = func(text, param)

    if expected is not None:
        if isinstance(expected, list):
            assert isinstance(result, list)
        else:
            assert result == expected
    else:
        assert result is not None
