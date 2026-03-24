"""Tests for converting between cardinal and ordinal numbers."""

import pytest
from textwarp._lib.numbers import cardinal_to_ordinal, ordinal_to_cardinal


@pytest.mark.parametrize('cardinal, expected_ordinal', [
    ('1', '1st'),
    ('2', '2nd'),
    ('3', '3rd'),
    ('4', '4th'),
    ('10', '10th'),
    ('11', '11th'),
    ('12', '12th'),
    ('13', '13th'),
    ('21', '21st'),
    ('22', '22nd'),
    ('103', '103rd'),
    ('525,600', '525,600th'),
])
def test_cardinal_to_ordinal_isolated(cardinal, expected_ordinal):
    """Test cardinal-to-ordinal conversion on isolated numbers."""
    assert cardinal_to_ordinal(cardinal) == expected_ordinal


def test_cardinal_to_ordinal_in_text():
    """Test cardinal-to-ordinal conversion within a sentence."""
    text = 'It happens in the 1 scene of the 3 act.'
    expected = 'It happens in the 1st scene of the 3rd act.'
    assert cardinal_to_ordinal(text) == expected


def test_cardinal_to_ordinal_ignores_decimals():
    """Test that numbers with decimal points are ignored."""
    assert cardinal_to_ordinal('version 3.14') == 'version 3.14'


@pytest.mark.parametrize('ordinal, expected_cardinal', [
    ('1st', '1'),
    ('2nd', '2'),
    ('3rd', '3'),
    ('4th', '4'),
    ('11th', '11'),
    ('21st', '21'),
    ('525,600th', '525,600'),
])
def test_ordinal_to_cardinal_isolated(ordinal, expected_cardinal):
    """Test ordinal-to-cardinal conversion on isolated numbers."""
    assert ordinal_to_cardinal(ordinal) == expected_cardinal


def test_ordinal_to_cardinal_in_text():
    """Test ordinal-to-cardinal conversion within a sentence."""
    text = "A 7th-nation army couldn't hold me back."
    expected = "A 7-nation army couldn't hold me back."
    assert ordinal_to_cardinal(text) == expected
