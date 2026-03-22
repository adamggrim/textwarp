"""Tests for English contraction suffix variants."""

from textwarp._core.providers.en_rules.apostrophes import (
    AIN_T_SUFFIX_VARIANTS,
    APOSTROPHE_D_VARIANTS,
    APOSTROPHE_S_VARIANTS
)


def test_apostrophe_sets_are_frozensets():
    """
    Verify that the apostrophe collections are immutable `frozenset`
    objects.
    """
    assert isinstance(AIN_T_SUFFIX_VARIANTS, frozenset)
    assert isinstance(APOSTROPHE_D_VARIANTS, frozenset)
    assert isinstance(APOSTROPHE_S_VARIANTS, frozenset)


def test_ain_t_suffix_variants():
    """Test the variants of the "n't" suffix."""
    assert "n't" in AIN_T_SUFFIX_VARIANTS
    assert "n’t" in AIN_T_SUFFIX_VARIANTS
    assert "n‘t" in AIN_T_SUFFIX_VARIANTS

    assert "ain't" not in AIN_T_SUFFIX_VARIANTS


def test_apostrophe_d_variants():
    """Test the variants of the "'d" suffix."""
    assert "'d" in APOSTROPHE_D_VARIANTS
    assert "’d" in APOSTROPHE_D_VARIANTS

    assert "you'd" not in APOSTROPHE_D_VARIANTS


def test_apostrophe_s_variants():
    """Test the variants of the "'s" suffix."""
    assert "'s" in APOSTROPHE_S_VARIANTS
    assert "’s" in APOSTROPHE_S_VARIANTS

    assert "it's" not in APOSTROPHE_S_VARIANTS
