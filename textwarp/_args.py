from typing import Callable

from .warping import (
    capitalize,
    cardinal_to_ordinal,
    curly_to_straight,
    expand_contractions,
    from_hexadecimal,
    from_morse,
    hyphens_to_em,
    hyphen_to_en,
    ordinal_to_cardinal,
    punct_to_inside,
    punct_to_outside,
    randomize,
    redact,
    reverse,
    straight_to_curly,
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
    to_title_case
)


# A dictionary mapping command-line arguments to their corresponding
# functions and help messages.
ARGS_MAP: dict[str, tuple[Callable[[str], str], str]] = {
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
    'lowercase': (
        str.lower,
        'convert to lowercase'
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
    'punct-to-inside': (
        punct_to_inside,
        '"move punctuation inside quotation marks."'
    ),
    'punct-to-outside': (
        punct_to_outside,
        '"move punctuation outside quotation marks".'
    ),
    'randomize': (
        randomize,
        'randomize the characters in each word'
    ),
    'redact': (
        redact,
        'redact text'
    ),
    'reverse': (
        reverse,
        'reverse text'
    ),
    'sentence-case': (
        to_sentence_case,
        'Convert to sentence case.'
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
        'convert lowercase to UPPERCASE and vice versa'
    ),
    'title-case': (
        to_title_case,
        'Convert to Title Case'
    ),
    'uppercase': (
        str.upper,
        'CONVERT TO UPPERCASE'
    )
}
