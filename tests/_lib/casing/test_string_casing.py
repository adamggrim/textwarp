from textwarp._lib.casing.string_casing import case_from_string


def test_case_from_string_delegation():
    assert case_from_string('nato') == 'NATO'
    assert case_from_string('mcdonald') == 'McDonald'
    assert case_from_string('muffin') == 'Muffin'


def test_case_from_string_flags():
    assert case_from_string('muffin', lowercase_by_default=True) == 'muffin'
    assert case_from_string('camelCase', preserve_mixed_case=True) == (
        'camelCase'
    )
    assert case_from_string('camelCase', preserve_mixed_case=False) == (
        'Camelcase'
    )
