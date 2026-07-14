"""Tests for tokenization and chunking functions."""

import pytest

from textwarp._core.enums import TokenType
from textwarp._lib.casing.lexing import get_normalized_tokens


@pytest.mark.parametrize('input_str, expected', [
    (
        'To make believe, doctor! To make believe that I am normal.',
        [
            (TokenType.WORD, 'To'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'make'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'believe'),
            (TokenType.SYMBOL, ','),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'doctor'),
            (TokenType.SYMBOL, '!'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'To'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'make'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'believe'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'that'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'I'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'am'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'normal'),
            (TokenType.SEPARATOR, '.')
        ]
    ),
    (
        'threadThePostern',
        [
            (TokenType.WORD, 'thread'),
            (TokenType.WORD, 'The'),
            (TokenType.WORD, 'Postern')
        ]
    ),
    (
        'ÉquilibreDesLiqueurs',
        [
            (TokenType.WORD, 'Équilibre'),
            (TokenType.WORD, 'Des'),
            (TokenType.WORD, 'Liqueurs')
        ]
    ),
    (
        'v4.0.950',
        [
            (TokenType.WORD, 'v'),
            (TokenType.WORD, '4'),
            (TokenType.SEPARATOR, '.'),
            (TokenType.WORD, '0'),
            (TokenType.SEPARATOR, '.'),
            (TokenType.WORD, '950')
        ]
    ),
    (
        'cache.h',
        [
            (TokenType.WORD, 'cache'),
            (TokenType.SEPARATOR, '.'),
            (TokenType.WORD, 'h')
        ]
    ),
    (
        'yorick@elsinore.dk',
        [
            (TokenType.WORD, 'yorick'),
            (TokenType.SYMBOL, '@'),
            (TokenType.WORD, 'elsinore'),
            (TokenType.SEPARATOR, '.'),
            (TokenType.WORD, 'dk'),
        ]
    ),
    (
        'It’s a beautiful thing, the destruction of words.',
        [
            (TokenType.WORD, 'Its'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'a'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'beautiful'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'thing'),
            (TokenType.SYMBOL, ','),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'the'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'destruction'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'of'),
            (TokenType.SEPARATOR, ' '),
            (TokenType.WORD, 'words'),
            (TokenType.SEPARATOR, '.')
        ]
    )
])
def test_get_normalized_tokens(input_str, expected):
    assert list(get_normalized_tokens(input_str)) == expected
ers = get_normalized_tokens('It’s a beautiful thing, the destruction of words.')
print(list(ers))