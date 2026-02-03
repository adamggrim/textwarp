"""
A mapping of command-line arguments to functions and help messages.
"""

import importlib
from types import ModuleType
from typing import (
    Callable,
    Final
)

__all__ = [
    'ARGS_MAP',
    'CASING_COMMANDS',
    'MUTUALLY_EXCLUSIVE_COMMANDS',
    'SEPARATOR_COMMANDS'
]


def _lazy_load(module_name: str, func_name: str) -> Callable[[str], str]:
    """Import a module and function only when called."""
    def wrapper(text: str) -> str:
        mod: ModuleType = importlib.import_module(
            module_name, package=__package__
        )
        return getattr(mod, func_name)(text)
    return wrapper


# A dictionary for all warping, analysis, replacement and
# clearing commands.

# This dictionary maps each public-facing command-line argument to a
# tuple containing:
#   1. The function that performs the action.
#   2. The help message to display for the argument.
ARGS_MAP: Final[dict[str, tuple[Callable[[str], str], str]]] = {
    'alternating-caps': (
        _lazy_load('..warping', 'to_alternating_caps'),
        'cOnVeRt To AlTeRnAtInG cApS'
    ),
    'binary': (
        _lazy_load('..warping', 'to_binary'),
        'convert to binary'
    ),
    'camel-case': (
        _lazy_load('..warping', 'to_camel_case'),
        'convertToCamelCase'
    ),
    'capitalize': (
        _lazy_load('..warping', 'capitalize'),
        'Capitalize The First Character Of Each Word'
    ),
    'cardinal': (
        _lazy_load('..warping', 'ordinal_to_cardinal'),
        'convert ordinal numbers to cardinal numbers'
    ),
    'char-count': (
        _lazy_load('.._commands.analysis', 'char_count'),
        'count characters'
    ),
    'clear': (
        lambda text: text,
        'clear clipboard text'
    ),
    'curly-quotes': (
        _lazy_load('.._lib.punctuation', 'straight_to_curly'),
        'convert "straight quotes" to “curly quotes”'
    ),
    'dot-case': (
        _lazy_load('..warping', 'to_dot_case'),
        'convert.to.dot.case'
    ),
    'expand-contractions': (
        _lazy_load('..warping', 'expand_contractions'),
        'expand contractions'
    ),
    'from-binary': (
        _lazy_load('..warping', 'from_binary'),
        'convert from binary'
    ),
    'from-hexadecimal': (
        _lazy_load('..warping', 'from_hexadecimal'),
        'convert from hexadecimal'
    ),
    'from-morse': (
        _lazy_load('..warping', 'from_morse'),
        'convert from Morse code'
    ),
    'hexadecimal': (
        _lazy_load('..warping', 'to_hexadecimal'),
        'convert to hexadecimal'
    ),
    'hyphens-to-em': (
        _lazy_load('..warping', 'hyphens_to_em'),
        'convert consecutive hyphens to em dashes'
    ),
    'hyphen-to-en': (
        _lazy_load('..warping', 'hyphen_to_en'),
        'convert hyphens to en dashes'
    ),
    'kebab-case': (
        _lazy_load('..warping', 'to_kebab_case'),
        'convert-to-kebab-case'
    ),
    'line-count': (
        _lazy_load('.._commands.analysis', 'line_count'),
        'count lines'
    ),
    'lowercase': (
        str.lower,
        'convert to lowercase'
    ),
    'mfws': (
        _lazy_load('.._commands.analysis', 'mfws'),
        'get most frequent words'
    ),
    'morse': (
        _lazy_load('..warping', 'to_morse'),
        'convert to Morse code'
    ),
    'ordinal': (
        _lazy_load('..warping', 'cardinal_to_ordinal'),
        'convert cardinal numbers to ordinal numbers'
    ),
    'pascal-case': (
        _lazy_load('..warping', 'to_pascal_case'),
        'ConvertToPascalCase'
    ),
    'plain-text': (
        str,
        'convert to plain text'
    ),
    'pos-count': (
        _lazy_load('.._commands.analysis', 'pos_count'),
        'count parts of speech'
    ),
    'punct-to-inside': (
        _lazy_load('..warping', 'punct_to_inside'),
        '"move punctuation inside quotation marks."'
    ),
    'punct-to-outside': (
        _lazy_load('..warping', 'punct_to_outside'),
        '"move punctuation outside quotation marks".'
    ),
    'random-case': (
        _lazy_load('..warping', 'random_case'),
        'randomize the casing of each character'
    ),
    'randomize': (
        _lazy_load('..warping', 'randomize'),
        'randomize characters'
    ),
    'redact': (
        _lazy_load('..warping', 'redact'),
        'redact text'
    ),
    'replace': (
        _lazy_load('.._commands.replacement', 'replace'),
        'find and replace text'
    ),
    'replace-case': (
        _lazy_load('.._commands.replacement', 'replace_case'),
        'find and replace a case'
    ),
    'replace-regex': (
        _lazy_load('.._commands.replacement', 'replace_regex'),
        'find and replace a regular expression'
    ),
    'reverse': (
        _lazy_load('..warping', 'reverse'),
        'reverse text'
    ),
    'sentence-case': (
        _lazy_load('..warping', 'to_sentence_case'),
        'Convert to sentence case.'
    ),
    'sentence-count': (
        _lazy_load('.._commands.analysis', 'sentence_count'),
        'count sentences'
    ),
    'single-spaces': (
        _lazy_load('..warping', 'to_single_spaces'),
        'convert consecutive spaces to a single space'
    ),
    'snake-case': (
        _lazy_load('..warping', 'to_snake_case'),
        'convert_to_snake_case'
    ),
    'straight-quotes': (
        _lazy_load('.._lib.punctuation', 'curly_to_straight'),
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
        _lazy_load('.._commands.analysis', 'time_to_read'),
        'calculate time to read'
    ),
    'title-case': (
        _lazy_load('..warping', 'to_title_case'),
        'Convert to Title Case'
    ),
    'uppercase': (
        str.upper,
        'CONVERT TO ALL CAPS'
    ),
    'word-count': (
        _lazy_load('.._commands.analysis', 'word_count'),
        'count words'
    ),
    'widen': (
        _lazy_load('..warping', 'widen'),
        'w i d e n  t e x t'
    )
}

# Can be combined with ``SEPARATOR_COMMANDS``. Mutually exclusive with
# each other.
CASING_COMMANDS: Final[set[str]] = {
    'alternating-caps', 'capitalize', 'lowercase', 'random-case',
    'sentence-case', 'swapcase', 'title-case', 'uppercase'
}

# Can be combined with ``CASING_COMMANDS``. Mutually exclusive with
# each other.
SEPARATOR_COMMANDS: Final[set[str]] = {
    'camel-case', 'dot-case', 'kebab-case', 'pascal-case',
    'snake-case', 'single-spaces', 'widen'
}

# Cannot be combined with any other warping or analysis commands.
MUTUALLY_EXCLUSIVE_COMMANDS: Final[set[str]] = {
    'binary', 'from-binary', 'hexadecimal', 'from-hexadecimal',
    'morse', 'from-morse', 'char-count', 'line-count', 'mfws',
    'pos-count', 'sentence-count', 'time-to-read', 'word-count'
}
