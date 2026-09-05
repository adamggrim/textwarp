"""A map of command-line arguments to functions and help messages."""

import importlib
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from types import ModuleType
from typing import Any, Final

from textwarp._core.context import N_

__all__ = ['ARGS_MAP', 'CLICommand', 'CommandType']


class CommandType(Enum):
    """Categories for pipeline commands."""
    ANALYSIS = auto()
    REPLACEMENT = auto()
    STANDALONE = auto()
    WARPING = auto()


@dataclass(frozen=True)
class CLICommand:
    """A single piipeline command and its configuration."""
    name: str
    func: Callable[..., Any]
    help_text: str
    command_type: CommandType
    requires_intermediate_input: bool = False
    requires_spacy: bool = False


def _lazy_load(module_name: str, func_name: str) -> Callable[..., str]:
    """Import a module and function only when called."""
    def wrapper(*args: Any, **kwargs: Any) -> str:
        mod: ModuleType = importlib.import_module(
            module_name, package=__package__
        )
        return getattr(mod, func_name)(*args, **kwargs)
    return wrapper


# A dictionary for all warping, analysis, replacement and
# standalone commands.
ARGS_MAP: Final[dict[str, CLICommand]] = {
    'alternating-caps': CLICommand(
        name='alternating-caps',
        func=_lazy_load('.._lib.effects', 'to_alternating_caps'),
        help_text=N_('cOnVeRt To AlTeRnAtInG cApS'),
        command_type=CommandType.WARPING
    ),
    'binary': CLICommand(
        name='binary',
        func=_lazy_load('.._lib.encoding', 'to_binary'),
        help_text=N_('convert to binary'),
        command_type=CommandType.WARPING
    ),
    'camel-case': CLICommand(
        name='camel-case',
        func=_lazy_load('.._lib.casing', 'to_camel_case'),
        help_text=N_('convertToCamelCase'),
        command_type=CommandType.WARPING
    ),
    'capitalize': CLICommand(
        name='capitalize',
        func=_lazy_load('.._lib.casing', 'capitalize'),
        help_text=N_('Capitalize The First Character Of Each Word'),
        command_type=CommandType.WARPING,
        requires_spacy=True
    ),
    'cardinal': CLICommand(
        name='cardinal',
        func=_lazy_load('.._lib.numbers', 'ordinal_to_cardinal'),
        help_text=N_('convert ordinal numbers to cardinal numbers'),
        command_type=CommandType.WARPING,
        requires_spacy=True
    ),
    'char-count': CLICommand(
        name='char-count',
        func=_lazy_load('.._commands.analysis', 'char_count'),
        help_text=N_('count characters'),
        command_type=CommandType.ANALYSIS
    ),
    'clear': CLICommand(
        name='clear',
        func=lambda text: '',
        help_text=N_('clear clipboard text'),
        command_type=CommandType.STANDALONE
    ),
    'curly-quotes': CLICommand(
        name='curly-quotes',
        func=_lazy_load('.._lib.punctuation', 'straight_to_curly'),
        help_text=N_('convert "straight quotes" to “curly quotes”'),
        command_type=CommandType.WARPING
    ),
    'dot-case': CLICommand(
        name='dot-case',
        func=_lazy_load('.._lib.casing', 'to_dot_case'),
        help_text=N_('convert.to.dot.case'),
        command_type=CommandType.WARPING
    ),
    'entity-counts': CLICommand(
        name='entity-counts',
        func=_lazy_load('.._commands.analysis', 'entity_counts'),
        help_text=N_('get most frequent entities'),
        command_type=CommandType.ANALYSIS,
        requires_intermediate_input=True,
        requires_spacy=True
    ),
    'expand-contractions': CLICommand(
        name='expand-contractions',
        func=_lazy_load('.._lib.contractions', 'expand_contractions'),
        help_text=N_('expand contractions'),
        command_type=CommandType.WARPING,
        requires_spacy=True
    ),
    'from-binary': CLICommand(
        name='from-binary',
        func=_lazy_load('.._lib.encoding', 'from_binary'),
        help_text=N_('convert from binary'),
        command_type=CommandType.WARPING
    ),
    'from-hexadecimal': CLICommand(
        name='from-hexadecimal',
        func=_lazy_load('.._lib.encoding', 'from_hexadecimal'),
        help_text=N_('convert from hexadecimal'),
        command_type=CommandType.WARPING
    ),
    'from-morse': CLICommand(
        name='from-morse',
        func=_lazy_load('.._lib.encoding', 'from_morse'),
        help_text=N_('convert from Morse code'),
        command_type=CommandType.WARPING
    ),
    'hexadecimal': CLICommand(
        name='hexadecimal',
        func=_lazy_load('.._lib.encoding', 'to_hexadecimal'),
        help_text=N_('convert to hexadecimal'),
        command_type=CommandType.WARPING
    ),
    'hyphens-to-em': CLICommand(
        name='hyphens-to-em',
        func=_lazy_load('.._lib.punctuation', 'hyphens_to_em'),
        help_text=N_('convert consecutive hyphens to em dashes'),
        command_type=CommandType.WARPING
    ),
    'hyphens-to-en': CLICommand(
        name='hyphens-to-en',
        func=_lazy_load('.._lib.punctuation', 'hyphens_to_en'),
        help_text=N_('convert hyphens to en dashes'),
        command_type=CommandType.WARPING
    ),
    'kebab-case': CLICommand(
        name='kebab-case',
        func=_lazy_load('.._lib.casing', 'to_kebab_case'),
        help_text=N_('convert-to-kebab-case'),
        command_type=CommandType.WARPING
    ),
    'line-count': CLICommand(
        name='line-count',
        func=_lazy_load('.._commands.analysis', 'line_count'),
        help_text=N_('count lines'),
        command_type=CommandType.ANALYSIS
    ),
    'lowercase': CLICommand(
        name='lowercase',
        func=str.lower,
        help_text=N_('convert to lowercase'),
        command_type=CommandType.WARPING
    ),
    'mfws': CLICommand(
        name='mfws',
        func=_lazy_load('.._commands.analysis', 'mfws'),
        help_text=N_('get most frequent words'),
        command_type=CommandType.ANALYSIS,
        requires_intermediate_input=True
    ),
    'morse': CLICommand(
        name='morse',
        func=_lazy_load('.._lib.encoding', 'to_morse'),
        help_text=N_('convert to Morse code'),
        command_type=CommandType.WARPING
    ),
    'ordinal': CLICommand(
        name='ordinal',
        func=_lazy_load('.._lib.numbers', 'cardinal_to_ordinal'),
        help_text=N_('convert cardinal numbers to ordinal numbers'),
        command_type=CommandType.WARPING,
        requires_spacy=True
    ),
    'pascal-case': CLICommand(
        name='pascal-case',
        func=_lazy_load('.._lib.casing', 'to_pascal_case'),
        help_text=N_('ConvertToPascalCase'),
        command_type=CommandType.WARPING
    ),
    'plain-text': CLICommand(
        name='plain-text',
        func=str,
        help_text=N_('convert to plain text'),
        command_type=CommandType.WARPING
    ),
    'pos-counts': CLICommand(
        name='pos-counts',
        func=_lazy_load('.._commands.analysis', 'pos_counts'),
        help_text=N_('count parts of speech'),
        command_type=CommandType.ANALYSIS,
        requires_spacy=True
    ),
    'punct-to-inside': CLICommand(
        name='punct-to-inside',
        func=_lazy_load('.._lib.punctuation', 'punct_to_inside'),
        help_text=N_('"move punctuation inside quotation marks."'),
        command_type=CommandType.WARPING
    ),
    'punct-to-outside': CLICommand(
        name='punct-to-outside',
        func=_lazy_load('.._lib.punctuation', 'punct_to_outside'),
        help_text=N_('"move punctuation outside quotation marks".'),
        command_type=CommandType.WARPING
    ),
    'random-case': CLICommand(
        name='random-case',
        func=_lazy_load('.._lib.effects', 'random_case'),
        help_text=N_('randomize the casing of each character'),
        command_type=CommandType.WARPING
    ),
    'randomize': CLICommand(
        name='randomize',
        func=_lazy_load('.._lib.effects', 'randomize'),
        help_text=N_('randomize characters'),
        command_type=CommandType.WARPING
    ),
    'redact': CLICommand(
        name='redact',
        func=_lazy_load('.._lib.effects', 'redact'),
        help_text=N_('redact text'),
        command_type=CommandType.WARPING
    ),
    'replace-case': CLICommand(
        name='replace-case',
        func=_lazy_load('.._commands.replacement', 'replace_case'),
        help_text=N_('find and replace a case'),
        command_type=CommandType.REPLACEMENT
    ),
    'replace-regex': CLICommand(
        name='replace-regex',
        func=_lazy_load('.._commands.replacement', 'replace_regex'),
        help_text=N_('find and replace a regular expression'),
        command_type=CommandType.REPLACEMENT
    ),
    'replace-text': CLICommand(
        name='replace-text',
        func=_lazy_load('.._commands.replacement', 'replace_text'),
        help_text=N_('find and replace text'),
        command_type=CommandType.REPLACEMENT
    ),
    'reverse': CLICommand(
        name='reverse',
        func=_lazy_load('.._lib.effects', 'reverse'),
        help_text=N_('reverse text'),
        command_type=CommandType.WARPING
    ),
    'sentence-case': CLICommand(
        name='sentence-case',
        func=_lazy_load('.._lib.casing', 'to_sentence_case'),
        help_text=N_('Convert to sentence case.'),
        command_type=CommandType.WARPING,
        requires_spacy=True
    ),
    'sentence-count': CLICommand(
        name='sentence-count',
        func=_lazy_load('.._commands.analysis', 'sentence_count'),
        help_text=N_('count sentences'),
        command_type=CommandType.ANALYSIS,
        requires_spacy=True
    ),
    'single-spaces': CLICommand(
        name='single-spaces',
        func=_lazy_load('.._lib.cleaning', 'to_single_spaces'),
        help_text=N_('convert consecutive spaces to a single space'),
        command_type=CommandType.WARPING
    ),
    'snake-case': CLICommand(
        name='snake-case',
        func=_lazy_load('.._lib.casing', 'to_snake_case'),
        help_text=N_('convert_to_snake_case'),
        command_type=CommandType.WARPING
    ),
    'straight-quotes': CLICommand(
        name='straight-quotes',
        func=_lazy_load('.._lib.punctuation', 'curly_to_straight'),
        help_text=N_('convert “curly quotes” to "straight quotes"'),
        command_type=CommandType.WARPING
    ),
    'strip': CLICommand(
        name='strip',
        func=str.strip,
        help_text=N_('strip leading and trailing whitespace'),
        command_type=CommandType.WARPING
    ),
    'strip-html': CLICommand(
        name='strip-html',
        func=_lazy_load('.._lib.cleaning', 'strip_html'),
        help_text=N_('strip HTML tags'),
        command_type=CommandType.WARPING
    ),
    'swapcase': CLICommand(
        name='swapcase',
        func=str.swapcase,
        help_text=N_('swap the case of all alphabetical characters'),
        command_type=CommandType.WARPING
    ),
    'time-to-read': CLICommand(
        name='time-to-read',
        func=_lazy_load('.._commands.analysis', 'time_to_read'),
        help_text=N_('calculate time to read'),
        command_type=CommandType.ANALYSIS,
        requires_intermediate_input=True
    ),
    'title-case': CLICommand(
        name='title-case',
        func=_lazy_load('.._lib.casing', 'to_title_case'),
        help_text=N_('Convert to Title Case'),
        command_type=CommandType.WARPING,
        requires_spacy=True
    ),
    'ttr': CLICommand(
        name='ttr',
        func=_lazy_load('.._commands.analysis', 'ttr'),
        help_text=N_('calculate type-token ratio'),
        command_type=CommandType.ANALYSIS
    ),
    'unzalgo': CLICommand(
        name='unzalgo',
        func=_lazy_load('.._lib.effects', 'unzalgo'),
        help_text=N_('remove Zalgo diacritics'),
        command_type=CommandType.WARPING
    ),
    'uppercase': CLICommand(
        name='uppercase',
        func=str.upper,
        help_text=N_('CONVERT TO ALL CAPS'),
        command_type=CommandType.WARPING
    ),
    'widen': CLICommand(
        name='widen',
        func=_lazy_load('.._lib.effects', 'widen'),
        help_text=N_('w i d e n  t e x t'),
        command_type=CommandType.WARPING
    ),
    'word-count': CLICommand(
        name='word-count',
        func=_lazy_load('.._commands.analysis', 'word_count'),
        help_text=N_('count words'),
        command_type=CommandType.ANALYSIS
    ),
    'zalgo': CLICommand(
        name='zalgo',
        func=_lazy_load('.._lib.effects', 'to_zalgo'),
        help_text=N_('c̵̼̝̦̗ͦ̑̓ö̶̧̹͈́̇n̷̹̟͗͒̇̚v̴̠̟̕e͖͖̺̮̟̐ȑ̺̻̳͚̩̊t̵ͣͮ͛ t̷̰̪̊͒o̵̻̠͂̀ Z̛̻͙̪̉̕ȃ̸̧͔̼͚͐l̸̵͇̪̅ḡ̡̻̟̜̍̄ǫ̵͔ͨ̆ t̸̶̢̤̲̎̋e̶̜͉̎̌x̴̷̨͇͇ͬẗ̸̡̝ͦ'),
        command_type=CommandType.WARPING
    )
}
