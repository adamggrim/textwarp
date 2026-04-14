"""Tests for the root package initialization and lazy loading."""

import pytest

import textwarp


def test_lazy_loading_all_attributes():
    """
    Verify that all attributes exposed in `__all__` are mapped to valid,
    callable functions.
    """
    for attr_name in textwarp.__all__:
        attr = getattr(textwarp, attr_name)
        assert callable(attr), f"Attribute '{attr_name}' is not callable."


def test_lazy_loading_invalid_attribute():
    """
    Verify that an invalid attribute raises a standard `AttributeError`.
    """
    with pytest.raises(
        AttributeError,
        match="module 'textwarp' has no attribute 'invalid_function_name'"
    ):
        _ = textwarp.invalid_function_name


def test_all_list_matches_module_map():
    """
    Verify that the `__all__` list matches the keys available in the
    internal `_MODULE_MAP`.
    """
    assert set(textwarp.__all__) == set(textwarp._MODULE_MAP.keys())
