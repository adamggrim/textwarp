"""A map of command-line arguments to functions and help messages."""

import importlib
from types import ModuleType
from typing import Callable, Final

from textwarp._core.context import N_

__all__ = [
    'ARGS_MAP',
    'CASING_COMMANDS',
    'MUTUALLY_EXCLUSIVE_COMMANDS',
    'REPLACEMENT_COMMANDS',
    'SEPARATOR_COMMANDS'
]


def _lazy_load(module_name: str, func_name: str) -> Callable[..., str]:
    """Import a module and function only when called."""
    def wrapper(*args, **kwargs) -> str:
        mod: ModuleType = importlib.import_module(
            module_name, package=__package__
        )
        return getattr(mod, func_name)(*args, **kwargs)
    return wrapper


# A dictionary for all warping, analysis, replacement and
# clearing commands.
ARGS_MAP: Final[dict[str, tuple[Callable[[str], str], str]]] = {
    'alternating-caps': (
        _lazy_load('..warping', 'to_alternating_caps'),
        N_('cOnVeRt To AlTeRnAtInG cApS')
    ),
    'binary': (
        _lazy_load('..warping', 'to_binary'),
        N_('convert to binary')
    ),
    'camel-case': (
        _lazy_load('..warping', 'to_camel_case'),
        N_('convertToCamelCase')
    ),
    'capitalize': (
        _lazy_load('..warping', 'capitalize'),
        N_('Capitalize The First Character Of Each Word')
    ),
    'cardinal': (
        _lazy_load('..warping', 'ordinal_to_cardinal'),
        N_('convert ordinal numbers to cardinal numbers')
    ),
    'char-count': (
        _lazy_load('.._commands.analysis', 'char_count'),
        N_('count characters')
    ),
    'clear': (
        lambda text: text,
        N_('clear clipboard text')
    ),
    'curly-quotes': (
        _lazy_load('.._lib.punctuation', 'straight_to_curly'),
        N_('convert "straight quotes" to “curly quotes”')
    ),
    'dot-case': (
        _lazy_load('..warping', 'to_dot_case'),
        N_('convert.to.dot.case')
    ),
    'expand-contractions': (
        _lazy_load('..warping', 'expand_contractions'),
        N_('expand contractions')
    ),
    'from-binary': (
        _lazy_load('..warping', 'from_binary'),
        N_('convert from binary')
    ),
    'from-hexadecimal': (
        _lazy_load('..warping', 'from_hexadecimal'),
        N_('convert from hexadecimal')
    ),
    'from-morse': (
        _lazy_load('..warping', 'from_morse'),
        N_('convert from Morse code')
    ),
    'hexadecimal': (
        _lazy_load('..warping', 'to_hexadecimal'),
        N_('convert to hexadecimal')
    ),
    'hyphen-to-en': (
        _lazy_load('..warping', 'hyphen_to_en'),
        N_('convert hyphens to en dashes')
    ),
    'hyphens-to-em': (
        _lazy_load('..warping', 'hyphens_to_em'),
        N_('convert consecutive hyphens to em dashes')
    ),
    'kebab-case': (
        _lazy_load('..warping', 'to_kebab_case'),
        N_('convert-to-kebab-case')
    ),
    'line-count': (
        _lazy_load('.._commands.analysis', 'line_count'),
        N_('count lines')
    ),
    'lowercase': (
        str.lower,
        N_('convert to lowercase')
    ),
    'mfws': (
        _lazy_load('.._commands.analysis', 'mfws'),
        N_('get most frequent words')
    ),
    'morse': (
        _lazy_load('..warping', 'to_morse'),
        N_('convert to Morse code')
    ),
    'ordinal': (
        _lazy_load('..warping', 'cardinal_to_ordinal'),
        N_('convert cardinal numbers to ordinal numbers')
    ),
    'pascal-case': (
        _lazy_load('..warping', 'to_pascal_case'),
        N_('ConvertToPascalCase')
    ),
    'plain-text': (
        str,
        N_('convert to plain text')
    ),
    'pos-counts': (
        _lazy_load('.._commands.analysis', 'pos_counts'),
        N_('count parts of speech')
    ),
    'punct-to-inside': (
        _lazy_load('..warping', 'punct_to_inside'),
        N_('"move punctuation inside quotation marks."')
    ),
    'punct-to-outside': (
        _lazy_load('..warping', 'punct_to_outside'),
        N_('"move punctuation outside quotation marks".')
    ),
    'random-case': (
        _lazy_load('..warping', 'random_case'),
        N_('randomize the casing of each character')
    ),
    'randomize': (
        _lazy_load('..warping', 'randomize'),
        N_('randomize characters')
    ),
    'redact': (
        _lazy_load('..warping', 'redact'),
        N_('redact text')
    ),
    'replace': (
        _lazy_load('.._commands.replacement', 'replace'),
        N_('find and replace text')
    ),
    'replace-case': (
        _lazy_load('.._commands.replacement', 'replace_case'),
        N_('find and replace a case')
    ),
    'replace-regex': (
        _lazy_load('.._commands.replacement', 'replace_regex'),
        N_('find and replace a regular expression')
    ),
    'reverse': (
        _lazy_load('..warping', 'reverse'),
        N_('reverse text')
    ),
    'sentence-case': (
        _lazy_load('..warping', 'to_sentence_case'),
        N_('Convert to sentence case.')
    ),
    'sentence-count': (
        _lazy_load('.._commands.analysis', 'sentence_count'),
        N_('count sentences')
    ),
    'single-spaces': (
        _lazy_load('..warping', 'to_single_spaces'),
        N_('convert consecutive spaces to a single space')
    ),
    'snake-case': (
        _lazy_load('..warping', 'to_snake_case'),
        N_('convert_to_snake_case')
    ),
    'straight-quotes': (
        _lazy_load('.._lib.punctuation', 'curly_to_straight'),
        N_('convert “curly quotes” to "straight quotes"')
    ),
    'strip': (
        str.strip,
        N_('remove leading and trailing whitespace')
    ),
    'swapcase': (
        str.swapcase,
        N_('swap the case of all alphabetical characters')
    ),
    'time-to-read': (
        _lazy_load('.._commands.analysis', 'time_to_read'),
        N_('calculate time to read')
    ),
    'title-case': (
        _lazy_load('..warping', 'to_title_case'),
        N_('Convert to Title Case')
    ),
    'uppercase': (
        str.upper,
        N_('CONVERT TO ALL CAPS')
    ),
    'word-count': (
        _lazy_load('.._commands.analysis', 'word_count'),
        N_('count words')
    ),
    'widen': (
        _lazy_load('..warping', 'widen'),
        N_('w i d e n  t e x t')
    )
}

# Can be combined with `SEPARATOR_COMMANDS`. Mutually exclusive with
# each other.
CASING_COMMANDS: Final[frozenset[str]] = frozenset({
    'alternating-caps', 'capitalize', 'lowercase', 'random-case',
    'sentence-case', 'swapcase', 'title-case', 'uppercase'
})

# Cannot be combined with any other warping or analysis commands.
MUTUALLY_EXCLUSIVE_COMMANDS: Final[frozenset[str]] = frozenset({
    'binary', 'from-binary', 'hexadecimal', 'from-hexadecimal',
    'morse', 'from-morse', 'char-count', 'line-count', 'mfws',
    'pos-counts', 'sentence-count', 'time-to-read', 'word-count'
})

# Commands that use `--find` and `--replace` arguments.
REPLACEMENT_COMMANDS: Final[frozenset[str]] = frozenset({
    'replace', 'replace-case', 'replace-regex'
})

# Can be combined with `CASING_COMMANDS`. Mutually exclusive with
# each other.
SEPARATOR_COMMANDS: Final[frozenset[str]] = frozenset({
    'camel-case', 'dot-case', 'kebab-case', 'pascal-case',
    'snake-case', 'single-spaces', 'widen'
})
