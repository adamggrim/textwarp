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
    test_string = 'The Strange Case of Dr Jekyll and Mr Hyde'

    expected_outputs = {
        'camel': 'theStrangeCaseOfDrJekyllAndMrHyde',
        'dot case': 'the.strange.case.of.dr.jekyll.and.mr.hyde',
        'lower': 'the strange case of dr jekyll and mr hyde',
        'kebab': 'the-strange-case-of-dr-jekyll-and-mr-hyde',
        'pascal case': 'TheStrangeCaseOfDrJekyllAndMrHyde',
        'snake': 'the_strange_case_of_dr_jekyll_and_mr_hyde',
        'uppercase': 'THE STRANGE CASE OF DR JEKYLL AND MR HYDE',
    }

    for case, expected in expected_outputs.items():
        assert CASE_NAMES_FUNC_MAP[case](test_string) == expected
