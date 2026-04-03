"""A Python package for analyzing and transforming text."""

__all__ = [
    'calculate_time_to_read',
    'capitalize',
    'cardinal_to_ordinal',
    'count_chars',
    'count_lines',
    'count_mfws',
    'count_pos',
    'count_sents',
    'count_words',
    'curly_to_straight',
    'expand_contractions',
    'from_binary',
    'from_hexadecimal',
    'from_morse',
    'hyphen_to_en',
    'hyphens_to_em',
    'ordinal_to_cardinal',
    'punct_to_inside',
    'punct_to_outside',
    'random_case',
    'randomize',
    'redact',
    'reverse',
    'straight_to_curly',
    'to_alternating_caps',
    'to_binary',
    'to_camel_case',
    'to_dot_case',
    'to_hexadecimal',
    'to_kebab_case',
    'to_morse',
    'to_pascal_case',
    'to_sentence_case',
    'to_single_spaces',
    'to_snake_case',
    'to_title_case',
    'widen'
]

def __getattr__(name: str):
    if name in {
        'calculate_time_to_read',
        'count_chars',
        'count_lines',
        'count_mfws',
        'count_pos',
        'count_sents',
        'count_words'
    }:
        import textwarp.analysis as mod
        return getattr(mod, name)
    elif name in {'curly_to_straight', 'straight_to_curly'}:
        import textwarp._lib.punctuation as mod
        return getattr(mod, name)
    elif name in {
        'capitalize',
        'cardinal_to_ordinal',
        'expand_contractions',
        'from_binary',
        'from_hexadecimal',
        'from_morse',
        'hyphen_to_en',
        'hyphens_to_em',
        'ordinal_to_cardinal',
        'punct_to_inside',
        'punct_to_outside',
        'random_case',
        'randomize',
        'redact',
        'reverse',
        'to_alternating_caps',
        'to_binary',
        'to_camel_case',
        'to_dot_case',
        'to_hexadecimal',
        'to_kebab_case',
        'to_morse',
        'to_pascal_case',
        'to_sentence_case',
        'to_single_spaces',
        'to_snake_case',
        'to_title_case',
        'widen'
    }:
        import textwarp.warping as mod
        return getattr(mod, name)

    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
