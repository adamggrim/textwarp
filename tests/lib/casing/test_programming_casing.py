"""Tests for converting between programming cases."""

from textwarp._core.enums import CaseSeparator
from textwarp._lib.casing.programming_casing import (
    to_camel_case,
    to_pascal_case,
    to_separator_case
)


def test_to_camel_case():
    assert to_camel_case('yonder cloud') == 'yonderCloud'
    assert to_camel_case('SHAPE OF A CAMEL') == 'shapeOfACamel'
    assert to_camel_case('LikeACamelIndeed') == 'likeACamelIndeed'
    assert to_camel_case('backed_like_a_snake') == 'backedLikeASnake'


def test_to_pascal_case():
    assert to_pascal_case('DieuEst') == 'DieuEst'
    assert to_pascal_case('il n’est pas') == 'IlNestPas'
    assert to_pascal_case('PENSÉES') == 'Pensées'
    assert to_pascal_case('un_serpent_qui_danse') == 'UnSerpentQuiDanse'


def test_to_separator_case_basic():
    assert to_separator_case(
        'Why did it have to be snakes?', CaseSeparator.SNAKE
    ) == 'why_did_it_have_to_be_snakes?'
    assert to_separator_case(
        'Vlad the Impaler', CaseSeparator.KEBAB
    ) == 'vlad-the-impaler'
    assert to_separator_case(
        'sunday on la grande jatte', CaseSeparator.DOT
    ) == 'sunday.on.la.grande.jatte'


def test_to_separator_case_from_existing_cases():
    assert to_separator_case(
        'withThySharpTeethThisKnotIntrinsicate', CaseSeparator.SNAKE
    ) == 'with_thy_sharp_teeth_this_knot_intrinsicate'
    assert to_separator_case(
        'spitted.upon.pikes', CaseSeparator.KEBAB
    ) == 'spitted-upon-pikes'
    assert to_separator_case(
        'a_square_round', CaseSeparator.DOT
    ) == 'a.square.round'


def test_to_separator_case_non_alpha():
    assert to_separator_case(
        '16 June 1904',
        CaseSeparator.SNAKE
    ) == '16_june_1904'
