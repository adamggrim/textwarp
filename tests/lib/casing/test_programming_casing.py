"""Tests for converting between programming cases."""

from textwarp._core.enums import CaseSeparator
from textwarp._lib.casing.programming_casing import (
    to_camel_case,
    to_pascal_case,
    to_separator_case
)


def test_to_camel_case():
    """Test converting text to camel case."""
    assert to_camel_case('hello world') == 'helloWorld'
    assert to_camel_case('HELLO WORLD') == 'helloWorld'
    assert to_camel_case('AlreadyCamelCase') == 'alreadyCamelCase'
    assert to_camel_case('snake_case_test') == 'snakeCaseTest'


def test_to_pascal_case():
    """Test converting text to Pascal case."""
    assert to_pascal_case('hello world') == 'HelloWorld'
    assert to_pascal_case('HELLO WORLD') == 'HelloWorld'
    assert to_pascal_case('alreadyPascalCase') == 'AlreadyPascalCase'
    assert to_pascal_case('snake_case_test') == 'SnakeCaseTest'


def test_to_separator_case_basic():
    """Test converting standard spaced text to separator cases."""
    assert to_separator_case('bell jar', CaseSeparator.SNAKE) == 'bell_jar'
    assert to_separator_case('bell jar', CaseSeparator.KEBAB) == 'bell-jar'
    assert to_separator_case('bell jar', CaseSeparator.DOT) == 'bell.jar'


def test_to_separator_case_existing_cases():
    """
    Test converting from existing programming cases to a new separator
    case.
    """
    assert to_separator_case(
        'existence-precedes-essence', CaseSeparator.SNAKE
    ) == 'existence_precedes_essence'
    assert to_separator_case(
        'being.nothingness', CaseSeparator.KEBAB
    ) == 'being-nothingness'
    assert to_separator_case(
        'deBeauvoir', CaseSeparator.SNAKE
    ) == 'de_beauvoir'
    assert to_separator_case(
        'LeMytheDeSisyphe', CaseSeparator.DOT
    ) == 'le.mythe.de.sisyphe'


def test_to_separator_case_non_alpha():
    """Test that separator casing safely handles numbers and symbols."""
    assert to_separator_case(
        'April 4th 1984',
        CaseSeparator.SNAKE
    ) == 'april_4th_1984'
