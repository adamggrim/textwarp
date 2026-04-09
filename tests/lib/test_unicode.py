"""Tests for transformation behavior with non-ASCII and Unicode characters."""

import pytest

from textwarp.warping import (
    capitalize,
    random_case,
    randomize,
    redact,
    reverse,
    to_alternating_caps,
    to_sentence_case,
    to_snake_case,
    to_title_case
)


@pytest.mark.parametrize('input_str, expected', [
    ('Die Walküre', 'die_walküre'),
    ('En un lugar de la Mancha', 'en_un_lugar_de_la_mancha'),
    ('Les Misérables', 'les_misérables'),
    ('Ἰλιάς', 'ἰλιάς'),
])
def test_separator_cases_handle_unicode(input_str, expected):
    """
    Test that separator cases safely handle non-ASCII letters using the
    underlying regular expression engine's `\\p{L}` matching.
    """
    assert to_snake_case(input_str) == expected


def test_reverse_handles_symbols():
    """
    Test that string reversal handles multi-byte symbols like emojis
    without shredding the underlying encoding.
    """
    assert reverse('Dante Alighieri 📜') == '📜 ireihgilA etnaD'
    assert reverse('Veni, vidi, vici. 🏛️') == '🏛️ .iciv ,idiv ,ineV'


def test_title_case_unicode():
    """
    Test that title casing correctly capitalizes non-ASCII starting
    letters while respecting the English provider's particle rules.
    """
    text = 'à la recherche du temps perdu'
    result = to_title_case(text)

    assert result.startswith('À')
    assert 'du' in result.split()
    assert result == 'À La Recherche du Temps Perdu'


@pytest.mark.parametrize('warping_func', [
    capitalize,
    random_case,
    randomize,
    redact,
    to_alternating_caps,
    to_sentence_case
])
def test_all_warping_standard_unicode(warping_func):
    """
    Smoke test to ensure that warping functions process non-ASCII
    characters without raising `UnicodeEncodeError` or
    `UnicodeDecodeError`.
    """
    text = 'Die Walküre 🇩🇪 y Don Quijote 🇪🇸'
    try:
        result = warping_func(text)
        assert isinstance(result, str)
        assert len(result) > 0
    except Exception as e:
        pytest.fail(
            f'{warping_func.__name__} failed on Unicode input with: {e}'
        )
