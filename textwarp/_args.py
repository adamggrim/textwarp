"""
This module contains a central registry for all warping, analysis,
replacement and clearing commands.
"""

from typing import (
    Callable,
    Final
)

from ._commands import (
    char_count,
    line_count,
    mfws,
    pos_count,
    replace,
    replace_case,
    replace_regex,
    sentence_count,
    time_to_read,
    word_count
)
from ._helpers import (
    curly_to_straight,
    straight_to_curly
)
from .warping import (
    capitalize,
    cardinal_to_ordinal,
    expand_contractions,
    from_binary,
    from_hexadecimal,
    from_morse,
    hyphens_to_em,
    hyphen_to_en,
    ordinal_to_cardinal,
    punct_to_inside,
    punct_to_outside,
    random_case,
    randomize,
    redact,
    reverse,
    to_alternating_caps,
    to_binary,
    to_camel_case,
    to_dot_case,
    to_hexadecimal,
    to_kebab_case,
    to_morse,
    to_pascal_case,
    to_sentence_case,
    to_single_spaces,
    to_snake_case,
    to_title_case,
    widen
)


# A dictionary for all warping, analysis, replacement and
# clearing commands.

# This dictionary maps the public-facing command-line argument
# (e.g., 'word-count') to a tuple containing:
#   1. The function that performs the action (e.g., word_count).
#   2. The help message to display for that argument.
ARGS_MAP: Final[dict[str, tuple[Callable[[str], str], str]]] = {
    'alternating-caps': (
        to_alternating_caps,
        'cOnVeRt To AlTeRnAtInG cApS'
    ),
    'binary': (
        to_binary,
        'convert to binary'
    ),
    'camel-case': (
        to_camel_case,
        'convertToCamelCase'
    ),
    'capitalize': (
        capitalize,
        'Capitalize The First Character Of Each Word'
    ),
    'cardinal': (
        ordinal_to_cardinal,
        'convert ordinal numbers to cardinal numbers'
    ),
    'char-count': (
        char_count,
        'count characters'
    ),
    'clear': (
        lambda text: text, # Placeholder to match Callable signature
        'clear clipboard text'
    ),
    'curly-quotes': (
        straight_to_curly,
        'convert "straight quotes" to “curly quotes”'
    ),
    'dot-case': (
        to_dot_case,
        'convert.to.dot.case'
    ),
    'expand-contractions': (
        expand_contractions,
        'expand contractions'
    ),
    'from-binary': (
        from_binary,
        'convert from binary'
    ),
    'from-hexadecimal': (
        from_hexadecimal,
        'convert from hexadecimal'
    ),
    'from-morse': (
        from_morse,
        'convert from Morse code'
    ),
    'hexadecimal': (
        to_hexadecimal,
        'convert to hexadecimal'
    ),
    'hyphens-to-em': (
        hyphens_to_em,
        'convert consecutive hyphens to em dashes'
    ),
    'hyphen-to-en': (
        hyphen_to_en,
        'convert hyphens to en dashes'
    ),
    'kebab-case': (
        to_kebab_case,
        'convert-to-kebab-case'
    ),
    'line-count': (
        line_count,
        'count lines'
    ),
    'lowercase': (
        str.lower,
        'convert to lowercase'
    ),
    'mfws': (
        mfws,
        'get most frequent words'
    ),
    'morse': (
        to_morse,
        'convert to Morse code'
    ),
    'ordinal': (
        cardinal_to_ordinal,
        'convert cardinal numbers to ordinal numbers'
    ),
    'pascal-case': (
        to_pascal_case,
        'ConvertToPascalCase'
    ),
    'plain-text': (
        str,
        'convert to plain text'
    ),
    'pos-count': (
        pos_count,
        'count parts of speech'
    ),
    'punct-to-inside': (
        punct_to_inside,
        '"move punctuation inside quotation marks."'
    ),
    'punct-to-outside': (
        punct_to_outside,
        '"move punctuation outside quotation marks".'
    ),
    'random-case': (
        random_case,
        'randomize the casing of each character'
    ),
    'randomize': (
        randomize,
        'randomize characters'
    ),
    'redact': (
        redact,
        'redact text'
    ),
    'replace': (
        replace,
        'find and replace text'
    ),
    'replace-case': (
        replace_case,
        'find and replace a case'
    ),
    'replace-regex': (
        replace_regex,
        'find and replace a regular expression'
    ),
    'reverse': (
        reverse,
        'reverse text'
    ),
    'sentence-case': (
        to_sentence_case,
        'Convert to sentence case.'
    ),
    'sentence-count': (
        sentence_count,
        'count sentences'
    ),
    'single-spaces': (
        to_single_spaces,
        'convert consecutive spaces to a single space'
    ),
    'snake-case': (
        to_snake_case,
        'convert_to_snake_case'
    ),
    'straight-quotes': (
        curly_to_straight,
        'convert “curly quotes” to "straight quotes"'
    ),
    'strip': (
        str.strip,
        'remove leading and trailing whitespace'
    ),
    'swapcase': (
        str.swapcase,
        'convert LOWERCASE to all caps and vice versa'
    ),
    'time-to-read': (
        time_to_read,
        'calculate time to read'
    ),
    'title-case': (
        to_title_case,
        'Convert to Title Case'
    ),
    'uppercase': (
        str.upper,
        'CONVERT TO ALL CAPS'
    ),
    'word-count': (
        word_count,
        'count words'
    ),
    'widen': (
        widen,
        'w i d e n  t e x t'
    )
}
