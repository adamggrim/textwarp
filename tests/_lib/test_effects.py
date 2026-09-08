"""Tests for visual and structural text effects."""

import unicodedata

from hypothesis import given, strategies

from textwarp._lib.effects import (
    _GRAPHEME_PATTERN,
    random_case,
    randomize,
    reverse,
    to_zalgo,
    unzalgo,
    widen
)


def test_random_case():
    input_text = 'Ch-ch-ch-ch-changes'
    result = random_case(input_text)

    # Check that the function changes casing while preserving length and
    # characters.
    assert len(result) == len(input_text)
    assert result.lower() == input_text.lower()


def test_randomize():
    original = 'all shook up'
    randomized = randomize(original)

    assert len(randomized) == len(original)
    assert sorted(randomized) == sorted(original)


@given(strategies.text())
def test_randomize_properties(s):
    result = randomize(s)
    assert len(result) == len(s)
    assert set(result) == set(s)


def test_reverse():
    assert reverse('number nine, number nine') == 'enin rebmun ,enin rebmun'
    assert reverse('redrum') == 'murder'


@given(strategies.text())
def test_reverse_symmetry(s):
    reversed_text = reverse(s)
    # Only enforce perfect symmetry if the previous reversal did not
    # merge any grapheme clusters.
    if (
        len(_GRAPHEME_PATTERN.findall(s))
        == len(_GRAPHEME_PATTERN.findall(reversed_text))
    ):
        assert reverse(reversed_text) == s


def test_to_zalgo():
    original = (
        'For every sin that he committed, a stain would fleck and wreck its '
        'fairness.'
    )
    zalgonized = to_zalgo(original)

    # Zalgonized text should be longer than the original.
    assert len(zalgonized) > len(original)

    assert unzalgo(zalgonized) == original


def test_to_zalgo_unicode():
    original = (
        'Un rire de démon, un rire qu’on ne peut avoir que lorsqu’on n’est '
        'plus homme, éclata sur le visage livide du prêtre.'
    )
    zalgonized = to_zalgo(original)

    cleaned = unzalgo(zalgonized)

    assert (
        unicodedata.normalize('NFC', cleaned)
        == unicodedata.normalize('NFC', original)
    )


@given(strategies.text())
def test_zalgo_stripping(s):
    assert unzalgo(to_zalgo(s)) == unzalgo(s)


def test_widen():
    assert widen('wide open spaces') == 'w i d e   o p e n   s p a c e s'
    assert widen('') == ''


@given(strategies.text(
    alphabet=strategies.characters(blacklist_categories=('Cs', 'Cn'))
))
def test_widen_properties(s):
    expected_length = max(0, (len(s) * 2) - 1)
    assert len(widen(s)) == expected_length
