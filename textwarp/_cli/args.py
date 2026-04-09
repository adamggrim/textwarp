"""A map of command-line arguments to functions and help messages."""

import gettext
import importlib
from types import ModuleType
from typing import Callable, Final

_ = gettext.gettext

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
ARGS_MAP: Final[dict[str, tuple[Callable[[str], str], str]]] = {
    'alternating-caps': (
        _lazy_load('..warping', 'to_alternating_caps'),
        _('cOnVeRt To AlTeRnAtInG cApS')
    ),
    'binary': (
        _lazy_load('..warping', 'to_binary'),
        _('convert to binary')
    ),
    'camel-case': (
        _lazy_load('..warping', 'to_camel_case'),
        _('convertToCamelCase')
    ),
    'capitalize': (
        _lazy_load('..warping', 'capitalize'),
        _('Capitalize The First Character Of Each Word')
    ),
    'cardinal': (
        _lazy_load('..warping', 'ordinal_to_cardinal'),
        _('convert ordinal numbers to cardinal numbers')
    ),
    'char-count': (
        _lazy_load('.._commands.analysis', 'char_count'),
        _('count characters')
    ),
    'clear': (
        lambda text: text,
        _('clear clipboard text')
    ),
    'curly-quotes': (
        _lazy_load('.._lib.punctuation', 'straight_to_curly'),
        _('convert "straight quotes" to “curly quotes”')
    ),
    'dot-case': (
        _lazy_load('..warping', 'to_dot_case'),
        _('convert.to.dot.case')
    ),
    'expand-contractions': (
        _lazy_load('..warping', 'expand_contractions'),
        _('expand contractions')
    ),
    'from-binary': (
        _lazy_load('..warping', 'from_binary'),
        _('convert from binary')
    ),
    'from-hexadecimal': (
        _lazy_load('..warping', 'from_hexadecimal'),
        _('convert from hexadecimal')
    ),
    'from-morse': (
        _lazy_load('..warping', 'from_morse'),
        _('convert from Morse code')
    ),
    'hexadecimal': (
        _lazy_load('..warping', 'to_hexadecimal'),
        _('convert to hexadecimal')
    ),
    'hyphen-to-en': (
        _lazy_load('..warping', 'hyphen_to_en'),
        _('convert hyphens to en dashes')
    ),
    'hyphens-to-em': (
        _lazy_load('..warping', 'hyphens_to_em'),
        _('convert consecutive hyphens to em dashes')
    ),
    'kebab-case': (
        _lazy_load('..warping', 'to_kebab_case'),
        _('convert-to-kebab-case')
    ),
    'line-count': (
        _lazy_load('.._commands.analysis', 'line_count'),
        _('count lines')
    ),
    'lowercase': (
        str.lower,
        _('convert to lowercase')
    ),
    'mfws': (
        _lazy_load('.._commands.analysis', 'mfws'),
        _('get most frequent words')
    ),
    'morse': (
        _lazy_load('..warping', 'to_morse'),
        _('convert to Morse code')
    ),
    'ordinal': (
        _lazy_load('..warping', 'cardinal_to_ordinal'),
        _('convert cardinal numbers to ordinal numbers')
    ),
    'pascal-case': (
        _lazy_load('..warping', 'to_pascal_case'),
        _('ConvertToPascalCase')
    ),
    'plain-text': (
        str,
        _('convert to plain text')
    ),
    'pos-count': (
        _lazy_load('.._commands.analysis', 'pos_count'),
        _('count parts of speech')
    ),
    'punct-to-inside': (
        _lazy_load('..warping', 'punct_to_inside'),
        _('"move punctuation inside quotation marks."')
    ),
    'punct-to-outside': (
        _lazy_load('..warping', 'punct_to_outside'),
        _('"move punctuation outside quotation marks".')
    ),
    'random-case': (
        _lazy_load('..warping', 'random_case'),
        _('randomize the casing of each character')
    ),
    'randomize': (
        _lazy_load('..warping', 'randomize'),
        _('randomize characters')
    ),
    'redact': (
        _lazy_load('..warping', 'redact'),
        _('redact text')
    ),
    'replace': (
        _lazy_load('.._commands.replacement', 'replace'),
        _('find and replace text')
    ),
    'replace-case': (
        _lazy_load('.._commands.replacement', 'replace_case'),
        _('find and replace a case')
    ),
    'replace-regex': (
        _lazy_load('.._commands.replacement', 'replace_regex'),
        _('find and replace a regular expression')
    ),
    'reverse': (
        _lazy_load('..warping', 'reverse'),
        _('reverse text')
    ),
    'sentence-case': (
        _lazy_load('..warping', 'to_sentence_case'),
        _('Convert to sentence case.')
    ),
    'sentence-count': (
        _lazy_load('.._commands.analysis', 'sentence_count'),
        _('count sentences')
    ),
    'single-spaces': (
        _lazy_load('..warping', 'to_single_spaces'),
        _('convert consecutive spaces to a single space')
    ),
    'snake-case': (
        _lazy_load('..warping', 'to_snake_case'),
        _('convert_to_snake_case')
    ),
    'straight-quotes': (
        _lazy_load('.._lib.punctuation', 'curly_to_straight'),
        _('convert “curly quotes” to "straight quotes"')
    ),
    'strip': (
        str.strip,
        _('remove leading and trailing whitespace')
    ),
    'swapcase': (
        str.swapcase,
        _('swap the case of all alphabetical characters')
    ),
    'time-to-read': (
        _lazy_load('.._commands.analysis', 'time_to_read'),
        _('calculate time to read')
    ),
    'title-case': (
        _lazy_load('..warping', 'to_title_case'),
        _('Convert to Title Case')
    ),
    'uppercase': (
        str.upper,
        _('CONVERT TO ALL CAPS')
    ),
    'word-count': (
        _lazy_load('.._commands.analysis', 'word_count'),
        _('count words')
    ),
    'widen': (
        _lazy_load('..warping', 'widen'),
        _('w i d e n  t e x t')
    )
}

# Can be combined with `SEPARATOR_COMMANDS`. Mutually exclusive with
# each other.
CASING_COMMANDS: Final[frozenset[str]] = frozenset({
    'alternating-caps', 'capitalize', 'lowercase', 'random-case',
    'sentence-case', 'swapcase', 'title-case', 'uppercase'
})

# Can be combined with `CASING_COMMANDS`. Mutually exclusive with
# each other.
SEPARATOR_COMMANDS: Final[frozenset[str]] = frozenset({
    'camel-case', 'dot-case', 'kebab-case', 'pascal-case',
    'snake-case', 'single-spaces', 'widen'
})

# Cannot be combined with any other warping or analysis commands.
MUTUALLY_EXCLUSIVE_COMMANDS: Final[frozenset[str]] = frozenset({
    'binary', 'from-binary', 'hexadecimal', 'from-hexadecimal',
    'morse', 'from-morse', 'char-count', 'line-count', 'mfws',
    'pos-count', 'sentence-count', 'time-to-read', 'word-count'
})
