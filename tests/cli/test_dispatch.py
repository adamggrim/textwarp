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
    test_string = 'Hello World'

    assert CASE_NAMES_FUNC_MAP['camel'](test_string) == 'helloWorld'
    assert CASE_NAMES_FUNC_MAP['dot case'](test_string) == 'hello.world'
    assert CASE_NAMES_FUNC_MAP['lower'](test_string) == 'hello world'
    assert CASE_NAMES_FUNC_MAP['kebab'](test_string) == 'hello-world'
    assert CASE_NAMES_FUNC_MAP['pascal case'](test_string) == 'HelloWorld'
    assert CASE_NAMES_FUNC_MAP['snake'](test_string) == 'hello_world'
    assert CASE_NAMES_FUNC_MAP['uppercase'](test_string) == 'HELLO WORLD'
