"""Tests for core case identification patterns."""

import regex as re

from textwarp._core.constants.patterns.cases import (
    get_camel_word,
    get_pascal_word,
    get_snake_word
)


def test_case_patterns_return_compiled_regexes():
    """
    Verify that case pattern methods return compiled regular
    expression objects.
    """
    assert isinstance(get_camel_word(), re.Pattern)
    assert isinstance(get_snake_word(), re.Pattern)
    assert isinstance(get_pascal_word(), re.Pattern)
