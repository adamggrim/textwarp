"""Exposes library functions for use across the package."""

from textwarp._lib.casing import (
    case_from_string,
    map_all_entities,
    should_capitalize_pos_or_length,
    to_camel_case,
    to_natural_case,
    to_pascal_case,
    to_separator_case
)
from textwarp._lib.contractions import expand_contractions
from textwarp._lib.encoding import (
    from_binary,
    from_hexadecimal,
    from_morse,
    to_binary,
    to_hexadecimal,
    to_morse
)
from textwarp._lib.manipulation import (
    randomize,
    reverse,
    to_single_spaces,
    widen
)
from textwarp._lib.nlp import extract_words_from_doc, process_as_doc
from textwarp._lib.numbers import cardinal_to_ordinal, ordinal_to_cardinal
from textwarp._lib.punctuation import (
    curly_to_straight,
    remove_apostrophes,
    straight_to_curly
)

__all__ = [
    'cardinal_to_ordinal',
    'case_from_string',
    'curly_to_straight',
    'expand_contractions',
    'extract_words_from_doc',
    'from_binary',
    'from_hexadecimal',
    'from_morse',
    'map_all_entities',
    'ordinal_to_cardinal',
    'process_as_doc',
    'randomize',
    'remove_apostrophes',
    'reverse',
    'should_capitalize_pos_or_length',
    'straight_to_curly',
    'to_binary',
    'to_camel_case',
    'to_hexadecimal',
    'to_morse',
    'to_natural_case',
    'to_pascal_case',
    'to_separator_case',
    'to_single_spaces',
    'widen'
]
