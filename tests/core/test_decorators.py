"""Tests for custom class decorators."""

import pytest
from textwarp._core.decorators import non_instantiable


@non_instantiable
class MockConfig:
    """A mock class to test the non_instantiable decorator."""
    STATIC_PROP = 'Test Property'

    @staticmethod
    def get_static_value() -> str:
        return 'Test Value'


def test_non_instantiable_raises_error():
    """
    Test that attempting class instantiation raises a RuntimeError.
    """
    with pytest.raises(
        RuntimeError, match='MockConfig cannot be instantiated.'
    ):
        MockConfig()


def test_non_instantiable_preserves_class_attributes():
    """Test that static attributes and methods remain accessible."""
    assert MockConfig.STATIC_PROP == 'Test Property'
    assert MockConfig.get_static_value() == 'Test Value'
