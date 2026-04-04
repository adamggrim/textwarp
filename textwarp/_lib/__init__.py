"""Exposes library functions for use across the package."""

from textwarp._lib.casing import (
    change_first_letter_case,
    doc_to_case,
    to_separator_case,
    word_to_pascal,
    map_all_entities,
    case_from_string,
    should_capitalize_pos_or_length
)
from textwarp._lib.contractions import expand_contractions
from textwarp._lib.encoding import (
    from_binary,
    from_hexadecimal,
    from_morse, to_binary,
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
    'change_first_letter_case',
    'doc_to_case',
    'to_separator_case',
    'word_to_pascal',
    'map_all_entities',
    'case_from_string',
    'should_capitalize_pos_or_length',
    'expand_contractions',
    'from_binary',
    'from_hexadecimal',
    'from_morse',
    'to_binary',
    'to_hexadecimal',
    'to_morse',
    'randomize',
    'reverse',
    'to_single_spaces',
    'widen',
    'extract_words_from_doc',
    'process_as_doc',
    'cardinal_to_ordinal',
    'ordinal_to_cardinal',
    'curly_to_straight',
    'remove_apostrophes',
    'straight_to_curly'
]
