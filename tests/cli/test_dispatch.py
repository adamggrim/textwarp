"""Tests for command-line case conversion dispatch mapping."""

from textwarp._cli.dispatch import CASE_NAMES_FUNC_MAP


def test_case_names_func_map_keys():
    """
    Verify that all expected case name keys are present in the case-
    names-to-function map.
    """
    expected_keys = {
        'camel',
        'camel case',
        'dot',
        'dot case',
        'lower',
        'lowercase',
        'kebab',
        'kebab case',
        'pascal',
        'pascal case',
        'snake',
        'snake case',
        'upper',
        'uppercase'
    }
    assert set(CASE_NAMES_FUNC_MAP.keys()) == expected_keys


def test_case_names_func_map_execution():
    """
    Verify that mapped functions correctly transform a test string.
    """
    test_string = 'Big Brother Is Watching'

    expected_outputs = {
        'camel': 'bigBrotherIsWatching',
        'dot case': 'big.brother.is.watching',
        'lower': 'big brother is watching',
        'kebab': 'big-brother-is-watching',
        'pascal case': 'BigBrotherIsWatching',
        'snake': 'big_brother_is_watching',
        'uppercase': 'BIG BROTHER IS WATCHING',
    }

    for case, expected in expected_outputs.items():
        assert CASE_NAMES_FUNC_MAP[case](test_string) == expected
