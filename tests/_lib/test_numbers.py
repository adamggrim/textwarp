from textwarp._lib.numbers import cardinal_to_ordinal, ordinal_to_cardinal


def test_cardinal_to_ordinal_delegation():
    original = 'It happens in the 1 scene of the 3 act.'
    expected = 'It happens in the 1st scene of the 3rd act.'
    assert cardinal_to_ordinal(original) == expected


def test_ordinal_to_cardinal_delegation():
    original = '9th concentric circles'
    expected = '9 concentric circles'
    assert ordinal_to_cardinal(original) == expected
