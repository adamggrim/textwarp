"""A Python package for analyzing and transforming text."""

import importlib
from typing import TYPE_CHECKING, Any

_MODULE_MAP: dict[str, str] = {
    'calculate_time_to_read': 'textwarp._lib.analysis',
    'calculate_ttr': 'textwarp._lib.analysis',
    'capitalize': 'textwarp._lib.casing',
    'cardinal_to_ordinal': 'textwarp._lib.numbers',
    'count_chars': 'textwarp._lib.analysis',
    'count_entities': 'textwarp._lib.analysis',
    'count_lines': 'textwarp._lib.analysis',
    'count_mfws': 'textwarp._lib.analysis',
    'count_pos': 'textwarp._lib.analysis',
    'count_sents': 'textwarp._lib.analysis',
    'count_words': 'textwarp._lib.analysis',
    'curly_to_straight': 'textwarp._lib.punctuation',
    'expand_contractions': 'textwarp._lib.contractions',
    'from_binary': 'textwarp._lib.encoding',
    'from_hexadecimal': 'textwarp._lib.encoding',
    'from_morse': 'textwarp._lib.encoding',
    'hyphens_to_em': 'textwarp._lib.punctuation',
    'hyphens_to_en': 'textwarp._lib.punctuation',
    'ordinal_to_cardinal': 'textwarp._lib.numbers',
    'punct_to_inside': 'textwarp._lib.punctuation',
    'punct_to_outside': 'textwarp._lib.punctuation',
    'random_case': 'textwarp._lib.effects',
    'randomize': 'textwarp._lib.effects',
    'redact': 'textwarp._lib.effects',
    'reverse': 'textwarp._lib.effects',
    'straight_to_curly': 'textwarp._lib.punctuation',
    'strip_html': 'textwarp._lib.cleaning',
    'to_alternating_caps': 'textwarp._lib.effects',
    'to_binary': 'textwarp._lib.encoding',
    'to_camel_case': 'textwarp._lib.casing',
    'to_dot_case': 'textwarp._lib.casing',
    'to_hexadecimal': 'textwarp._lib.encoding',
    'to_kebab_case': 'textwarp._lib.casing',
    'to_morse': 'textwarp._lib.encoding',
    'to_pascal_case': 'textwarp._lib.casing',
    'to_sentence_case': 'textwarp._lib.casing',
    'to_single_spaces': 'textwarp._lib.cleaning',
    'to_snake_case': 'textwarp._lib.casing',
    'to_title_case': 'textwarp._lib.casing',
    'to_zalgo': 'textwarp._lib.effects',
    'unzalgo': 'textwarp._lib.effects',
    'widen': 'textwarp._lib.effects'
}

__all__ = list(_MODULE_MAP.keys())

if TYPE_CHECKING:
    from textwarp._lib.analysis import (
        calculate_time_to_read as calculate_time_to_read,
        calculate_ttr as calculate_ttr,
        count_chars as count_chars,
        count_entities as count_entities,
        count_lines as count_lines,
        count_mfws as count_mfws,
        count_pos as count_pos,
        count_sents as count_sents,
        count_words as count_words
    )
    from textwarp._lib.casing import (
        capitalize as capitalize,
        to_camel_case as to_camel_case,
        to_dot_case as to_dot_case,
        to_kebab_case as to_kebab_case,
        to_pascal_case as to_pascal_case,
        to_sentence_case as to_sentence_case,
        to_snake_case as to_snake_case,
        to_title_case as to_title_case
    )
    from textwarp._lib.cleaning import (
        strip_html as strip_html,
        to_single_spaces as to_single_spaces
    )
    from textwarp._lib.contractions import (
        expand_contractions as expand_contractions
    )
    from textwarp._lib.effects import (
        random_case as random_case,
        randomize as randomize,
        redact as redact,
        reverse as reverse,
        to_alternating_caps as to_alternating_caps,
        to_zalgo as to_zalgo,
        unzalgo as unzalgo,
        widen as widen
    )
    from textwarp._lib.encoding import (
        from_binary as from_binary,
        from_hexadecimal as from_hexadecimal,
        from_morse as from_morse,
        to_binary as to_binary,
        to_hexadecimal as to_hexadecimal,
        to_morse as to_morse
    )
    from textwarp._lib.numbers import (
        cardinal_to_ordinal as cardinal_to_ordinal,
        ordinal_to_cardinal as ordinal_to_cardinal
    )
    from textwarp._lib.punctuation import (
        curly_to_straight as curly_to_straight,
        hyphens_to_em as hyphens_to_em,
        hyphens_to_en as hyphens_to_en,
        punct_to_inside as punct_to_inside,
        punct_to_outside as punct_to_outside,
        straight_to_curly as straight_to_curly
    )


def __getattr__(name: str) -> Any:
    """Lazily load functions from submodules when accessed as package
    attributes.

    Args:
        name: The name of the accessed attribute.

    Raises:
        AttributeError: If the module has no such attribute.
    """
    if name in _MODULE_MAP:
        mod = importlib.import_module(_MODULE_MAP[name])
        attr = getattr(mod, name)
        globals()[name] = attr
        return attr

    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
