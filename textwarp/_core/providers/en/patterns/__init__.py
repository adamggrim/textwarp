"""Exposes English-specific regular expression patterns."""

from textwarp._core.providers.en.patterns.warping import (
    get_ambiguous_contraction,
    get_apostrophe_in_word,
    get_cardinal,
    get_common_stateless_participles,
    get_contraction,
    get_contraction_suffixes_pattern,
    get_idiomatic_phrases,
    get_map_suffix_exceptions_pattern,
    get_n_t_suffix,
    get_name_prefix_exception_pattern,
    get_ordinal,
    get_punct_inside,
    get_punct_outside,
    get_surname_prefix_pattern,
    get_whatcha_are_words,
    get_whatcha_have_words
)

__all__ = [
    'get_ambiguous_contraction',
    'get_apostrophe_in_word',
    'get_cardinal',
    'get_common_stateless_participles',
    'get_contraction',
    'get_contraction_suffixes_pattern',
    'get_idiomatic_phrases',
    'get_map_suffix_exceptions_pattern',
    'get_n_t_suffix',
    'get_name_prefix_exception_pattern',
    'get_ordinal',
    'get_punct_inside',
    'get_punct_outside',
    'get_surname_prefix_pattern',
    'get_whatcha_are_words',
    'get_whatcha_have_words'
]