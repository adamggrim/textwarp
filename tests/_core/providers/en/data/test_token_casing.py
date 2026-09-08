"""Tests for English token casing data loading."""

from textwarp._core.providers.en.data import token_casing


def test_token_casing_config():
    """Test that token casing lists are properly converted to sets."""
    particles = token_casing.get_lowercase_particles()
    assert isinstance(particles, frozenset)
    assert 'von' in particles
