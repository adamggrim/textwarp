"""Tests for converting between programming cases."""

import string

from hypothesis import given, strategies
import pytest

from textwarp._core.enums import CaseSeparator
from textwarp._lib.casing.programming_casing import (
    to_camel_case,
    to_pascal_case,
    to_separator_case
)

_PROGRAMMING_CASE_CHARS = string.ascii_letters + string.digits + ' _-.'


@pytest.mark.parametrize('text, expected', [
    ('yonder cloud', 'yonderCloud'),
    ('SHAPE OF A CAMEL', 'shapeOfACamel'),
    ('LikeACamelIndeed', 'likeACamelIndeed'),
    ('backed_like_a_snake', 'backedLikeASnake')
])
def test_to_camel_case(text, expected):
    assert to_camel_case(text) == expected


@pytest.mark.parametrize('text, expected', [
    ('DieuEst', 'DieuEst'),
    ('il n’est pas', 'IlNestPas'),
    ('PENSÉES', 'Pensées'),
    ('un_serpent_qui_danse', 'UnSerpentQuiDanse')
])
def test_to_pascal_case(text, expected):
    assert to_pascal_case(text) == expected


@pytest.mark.parametrize('text, separator, expected', [
    (
        'Why did it have to be snakes?',
        CaseSeparator.SNAKE,
        'why_did_it_have_to_be_snakes?'
    ),
    ('Vlad the Impaler', CaseSeparator.KEBAB, 'vlad-the-impaler'),
    ('la grande jatte', CaseSeparator.DOT, 'la.grande.jatte'),
    (
        'withThySharpTeethThisKnotIntrinsicate',
        CaseSeparator.SNAKE,
        'with_thy_sharp_teeth_this_knot_intrinsicate'
    ),
    ('spitted.upon.pikes', CaseSeparator.KEBAB, 'spitted-upon-pikes'),
    ('a_square_round', CaseSeparator.DOT, 'a.square.round'),
    ('16 June 1904', CaseSeparator.SNAKE, '16_june_1904')
])
def test_to_separator_case(text, separator, expected):
    assert to_separator_case(text, separator) == expected


@given(strategies.text(alphabet=_PROGRAMMING_CASE_CHARS))
def test_to_snake_case_idempotence(s):
    first_pass = to_separator_case(s, CaseSeparator.SNAKE)
    second_pass = to_separator_case(first_pass, CaseSeparator.SNAKE)
    assert first_pass == second_pass


@given(strategies.text(alphabet=_PROGRAMMING_CASE_CHARS))
def test_to_camel_case_idempotence(s):
    first_pass = to_camel_case(s)
    second_pass = to_camel_case(first_pass)
    # Account for context loss on first pass.
    assert second_pass == to_camel_case(second_pass)
