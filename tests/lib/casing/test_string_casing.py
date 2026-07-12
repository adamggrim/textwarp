"""Tests for string capitalization through dictionary lookups."""

from textwarp._lib.casing.string_casing import case_from_string


def test_case_from_string_pronoun_i():
    assert case_from_string('i') == 'I'


def test_case_from_string_abbreviations():
    assert case_from_string('e.g.', lowercase_by_default=True) == 'e.g.'
    assert case_from_string('vs.', lowercase_by_default=True) == 'vs.'


def test_case_from_string_initialisms():
    assert case_from_string('u.s.a.') == 'U.S.A.'
    assert case_from_string('ph.d.') == 'Ph.D.'


def test_case_from_string_absolute_map():
    """Test words that have hardcoded casings in the lookup map."""
    assert case_from_string('nato') == 'NATO'
    assert case_from_string('macos') == 'macOS'
    assert case_from_string('iphone') == 'iPhone'


def test_case_from_string_map_suffix():
    """
    Test that dictionary capitalization preserves contraction suffixes.
    """
    assert case_from_string("nato's") == "NATO's"
    assert case_from_string("ceo's") == "CEO's"


def test_case_from_string_prefixed_surname():
    assert case_from_string('mcdonald') == 'McDonald'
    assert case_from_string('o’connor') == 'O’Connor'
    assert case_from_string('macarthur') == 'MacArthur'


def test_case_from_string_prefixed_surname_exception():
    assert case_from_string('macaw') == 'Macaw'
    assert case_from_string('machine') == 'Machine'


def test_case_from_string_mixed_case():
    assert case_from_string('camelCase') == 'camelCase'

    assert (
        case_from_string('camelCase', preserve_mixed_case=False) == 'Camelcase'
    )


def test_case_from_string_fallback():
    assert case_from_string('muffin') == 'Muffin'
