"""Tests for English-specific string casing logic."""

from textwarp._core.providers.en.casing import case_from_string


def test_case_from_string_pronoun_i():
    assert case_from_string('i') == 'I'
    assert case_from_string('i', lowercase_by_default=True) == 'I'


def test_case_from_string_abbreviations():
    assert case_from_string('e.g.,', lowercase_by_default=True) == 'e.g.,'

    assert case_from_string('vs.', lowercase_by_default=True) == 'vs.'


def test_case_from_string_initialisms():
    assert case_from_string('u.s.a.') == 'U.S.A.'
    assert case_from_string('ph.d.') == 'Ph.D.'
    assert case_from_string("u.s.a.'s") == "U.S.A.'s"
    assert case_from_string('ph.d.’s') == 'Ph.D.’s'


def test_case_from_string_absolute_map():
    assert case_from_string('nato') == 'NATO'
    assert case_from_string('iphone') == 'iPhone'


def test_case_from_string_prefixed_surname():
    assert case_from_string('mcdonald') == 'McDonald'
    assert case_from_string("o'connor") == "O'Connor"


def test_case_from_string_mixed_case():
    assert case_from_string('camelCase') == 'camelCase'
    assert case_from_string(
        'camelCase', preserve_mixed_case=False
    ) == 'Camelcase'
