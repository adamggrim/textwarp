"""Tests for converting between cardinal and ordinal numbers."""

import pytest
from textwarp._lib.numbers import cardinal_to_ordinal, ordinal_to_cardinal


@pytest.mark.parametrize('cardinal, expected_ordinal', [
    ('1', '1st'),
    ('1', '1st'),
    ('2', '2nd'),
    ('3', '3rd'),
    ('5', '5th'),
    ('8', '8th'),
    ('13', '13th'),
    ('21', '21st'),
    ('34', '34th')
])
def test_cardinal_to_ordinal_isolated(cardinal, expected_ordinal):
    assert cardinal_to_ordinal(cardinal) == expected_ordinal


def test_cardinal_to_ordinal_in_text():
    text = 'It happens in the 1 scene of the 3 act.'
    expected = 'It happens in the 1st scene of the 3rd act.'
    assert cardinal_to_ordinal(text) == expected


def test_cardinal_to_ordinal_ignores_decimals():
    assert cardinal_to_ordinal('811.52') == '811.52'


@pytest.mark.parametrize('ordinal, expected_cardinal', [
    ('4th', '4'),
    ('5th', '5'),
    ('25th', '25'),
    ('32nd', '32')
])
def test_ordinal_to_cardinal_isolated(ordinal, expected_cardinal):
    assert ordinal_to_cardinal(ordinal) == expected_cardinal


def test_ordinal_to_cardinal_in_text():
    text = '9th concentric circles'
    expected = '9 concentric circles'
    assert ordinal_to_cardinal(text) == expected
