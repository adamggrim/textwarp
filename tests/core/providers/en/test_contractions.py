"""Tests for English contraction variant sets."""

from textwarp._core.providers.en.contractions import (
    AIN_T_SUFFIX_VARIANTS,
    APOSTROPHE_D_VARIANTS,
    APOSTROPHE_S_VARIANTS
)


def test_contraction_variants_are_frozensets():
    """Verify that all contraction variant sets are immutable."""
    assert isinstance(AIN_T_SUFFIX_VARIANTS, frozenset)
    assert isinstance(APOSTROPHE_D_VARIANTS, frozenset)
    assert isinstance(APOSTROPHE_S_VARIANTS, frozenset)


def test_ain_t_suffix_variants():
    """Verify straight and curly variations of the "n't" suffix."""
    assert "n't" in AIN_T_SUFFIX_VARIANTS
    assert 'n’t' in AIN_T_SUFFIX_VARIANTS
    assert 'n‘t' in AIN_T_SUFFIX_VARIANTS


def test_apostrophe_d_variants():
    """Verify straight and curly variations of the "d" suffix."""
    assert "'d" in APOSTROPHE_D_VARIANTS
    assert '’d' in APOSTROPHE_D_VARIANTS
    assert '‘d' in APOSTROPHE_D_VARIANTS


def test_apostrophe_s_variants():
    """Verify straight and curly variations of the "s" suffix."""
    assert "'s" in APOSTROPHE_S_VARIANTS
    assert '’s' in APOSTROPHE_S_VARIANTS
    assert '‘s' in APOSTROPHE_S_VARIANTS
