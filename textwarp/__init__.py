"""A Python package for analyzing and transforming text."""

import importlib

_MODULE_MAP: dict[str, str] = {
    'calculate_time_to_read': 'textwarp.analysis',
    'count_chars': 'textwarp.analysis',
    'count_lines': 'textwarp.analysis',
    'count_mfws': 'textwarp.analysis',
    'count_pos': 'textwarp.analysis',
    'count_sents': 'textwarp.analysis',
    'count_words': 'textwarp.analysis',
    'curly_to_straight': 'textwarp._lib.punctuation',
    'straight_to_curly': 'textwarp._lib.punctuation',
    'capitalize': 'textwarp.warping',
    'cardinal_to_ordinal': 'textwarp.warping',
    'expand_contractions': 'textwarp.warping',
    'from_binary': 'textwarp.warping',
    'from_hexadecimal': 'textwarp.warping',
    'from_morse': 'textwarp.warping',
    'hyphen_to_en': 'textwarp.warping',
    'hyphens_to_em': 'textwarp.warping',
    'ordinal_to_cardinal': 'textwarp.warping',
    'punct_to_inside': 'textwarp.warping',
    'punct_to_outside': 'textwarp.warping',
    'random_case': 'textwarp.warping',
    'randomize': 'textwarp.warping',
    'redact': 'textwarp.warping',
    'reverse': 'textwarp.warping',
    'to_alternating_caps': 'textwarp.warping',
    'to_binary': 'textwarp.warping',
    'to_camel_case': 'textwarp.warping',
    'to_dot_case': 'textwarp.warping',
    'to_hexadecimal': 'textwarp.warping',
    'to_kebab_case': 'textwarp.warping',
    'to_morse': 'textwarp.warping',
    'to_pascal_case': 'textwarp.warping',
    'to_sentence_case': 'textwarp.warping',
    'to_single_spaces': 'textwarp.warping',
    'to_snake_case': 'textwarp.warping',
    'to_title_case': 'textwarp.warping',
    'widen': 'textwarp.warping'
}


def __getattr__(name: str):
    """
    Lazily load functions from submodules when accessed as attributes ofs
    the package.

    Args:
        name: The name of the accessed attribute.
    """
    if name in _MODULE_MAP:
        mod = importlib.import_module(_MODULE_MAP[name])
        return getattr(mod, name)

    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
