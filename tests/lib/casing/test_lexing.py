"""Tests for tokenization and chunking functions."""

from textwarp._core.enums import TokenType
from textwarp._lib.casing.lexing import get_normalized_tokens


def test_get_normalized_tokens_mixed_case():
    """Test tokenization of mixed casing strings."""
    result = list(get_normalized_tokens('camelCase'))
    assert result == [
        (TokenType.WORD, 'camel'),
        (TokenType.WORD, 'Case')
    ]

    result2 = list(get_normalized_tokens('PascalCaseString'))
    assert result2 == [
        (TokenType.WORD, 'Pascal'),
        (TokenType.WORD, 'Case'),
        (TokenType.WORD, 'String')
    ]


def test_get_normalized_tokens_with_numbers():
    """Test tokenization of strings containing numbers."""
    result = list(get_normalized_tokens('base64Encoding'))
    assert result == [
        (TokenType.WORD, 'base'),
        (TokenType.WORD, '64'),
        (TokenType.WORD, 'Encoding')
    ]

    result2 = list(get_normalized_tokens('v1.0.3'))
    assert result2 == [
        (TokenType.WORD, 'v'),
        (TokenType.WORD, '1'),
        (TokenType.SEPARATOR, '.'),
        (TokenType.WORD, '0'),
        (TokenType.SEPARATOR, '.'),
        (TokenType.WORD, '3')
    ]


def test_get_normalized_tokens_separators():
    """
    Test tokenization of standard separators (space, dot, dash,
    underscore).
    """
    result = list(get_normalized_tokens('hello-world_test.py'))
    assert result == [
        (TokenType.WORD, 'hello'),
        (TokenType.SEPARATOR, '-'),
        (TokenType.WORD, 'world'),
        (TokenType.SEPARATOR, '_'),
        (TokenType.WORD, 'test'),
        (TokenType.SEPARATOR, '.'),
        (TokenType.WORD, 'py')
    ]

    result2 = list(get_normalized_tokens('a simple test'))
    assert result2 == [
        (TokenType.WORD, 'a'),
        (TokenType.SEPARATOR, ' '),
        (TokenType.WORD, 'simple'),
        (TokenType.SEPARATOR, ' '),
        (TokenType.WORD, 'test')
    ]


def test_get_normalized_tokens_symbols():
    """Test tokenization of non-separator symbols."""
    result = list(get_normalized_tokens('email@address.com!'))
    assert result == [
        (TokenType.WORD, 'email'),
        (TokenType.SYMBOL, '@'),
        (TokenType.WORD, 'address'),
        (TokenType.SEPARATOR, '.'),
        (TokenType.WORD, 'com'),
        (TokenType.SYMBOL, '!')
    ]


def test_get_normalized_tokens_apostrophes():
    """Test that apostrophes are removed before tokenization."""
    result = list(get_normalized_tokens("don't fail"))
    assert result == [
        (TokenType.WORD, 'dont'),
        (TokenType.SEPARATOR, ' '),
        (TokenType.WORD, 'fail')
    ]
