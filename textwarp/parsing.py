import argparse
import sys
from typing import Callable

from textwarp.constants import HelpMessages
from textwarp.warping import (
    capitalize,
    cardinal_to_ordinal,
    curly_to_straight,
    expand_contractions,
    hyphens_to_em,
    hyphen_to_en,
    punct_to_inside,
    ordinal_to_cardinal,
    punct_to_outside,
    straight_to_curly,
    strikethrough,
    to_alternating_caps,
    to_binary,
    to_camel_case,
    to_hexadecimal,
    to_kebab_case,
    to_lowercase,
    to_pascal_case,
    to_sentence_case,
    to_single_spaces,
    to_snake_case,
    to_title_case,
    to_uppercase
)


def parse_args() -> Callable[[str], str]:
    """
    Parse command-line arguments for a text warping function.

    Returns:
        Callable[[str], str]: The text warping function corresponding
            to the specified command-line argument.
    """
    # A custom help formatter to align help messages neatly based on
    # the maximum argument length.
    formatter: Callable[[str], argparse.HelpFormatter] = (
        lambda prog: argparse.HelpFormatter(prog, max_help_position=25)
    )

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='textwarp',
        formatter_class=formatter,
        description=HelpMessages.DESCRIPTION,
        usage='%(prog)s [command]'
    )

    group: argparse._MutuallyExclusiveGroup = (
        parser.add_mutually_exclusive_group(required=True)
    )
    group.add_argument('--alternating-caps', action='store_true',
                       help=HelpMessages.ALTERNATING_CAPS)
    group.add_argument('--binary', action='store_true',
                       help=HelpMessages.BINARY)
    group.add_argument('--camel-case', action='store_true',
                       help=HelpMessages.CAMEL_CASE)
    group.add_argument('--capitalize', action='store_true',
                       help=HelpMessages.CAPITALIZE)
    group.add_argument('--cardinal', action='store_true',
                       help=HelpMessages.CARDINAL)
    group.add_argument('--curly-quotes', action='store_true',
                       help=HelpMessages.CURLY_QUOTES)
    group.add_argument('--expand-contractions', action='store_true',
                       help=HelpMessages.EXPAND_CONTRACTIONS)
    group.add_argument('--hexadecimal', action='store_true',
                       help=HelpMessages.HEXADECIMAL)
    group.add_argument('--hyphens-to-em', action='store_true',
                       help=HelpMessages.HYPHENS_TO_EM)
    group.add_argument('--hyphen-to-en', action='store_true',
                       help=HelpMessages.HYPHEN_TO_EN)
    group.add_argument('--kebab-case', action='store_true',
                       help=HelpMessages.KEBAB_CASE)
    group.add_argument('--lowercase', action='store_true',
                       help=HelpMessages.LOWERCASE)
    group.add_argument('--ordinal', action='store_true',
                       help=HelpMessages.ORDINAL)
    group.add_argument('--pascal-case', action='store_true',
                       help=HelpMessages.PASCAL_CASE)
    group.add_argument('--punct-to-inside', action='store_true',
                       help=HelpMessages.PUNCT_TO_INSIDE)
    group.add_argument('--punct-to-outside', action='store_true',
                       help=HelpMessages.PUNCT_TO_OUTSIDE)
    group.add_argument('--sentence-case', action='store_true',
                       help=HelpMessages.SENTENCE_CASE)
    group.add_argument('--single-spaces', action='store_true',
                       help=HelpMessages.SINGLE_SPACES)
    group.add_argument('--snake-case', action='store_true',
                       help=HelpMessages.SNAKE_CASE)
    group.add_argument('--straight-quotes', action='store_true',
                       help=HelpMessages.STRAIGHT_QUOTES)
    group.add_argument('--strikethrough', action='store_true',
                       help=HelpMessages.STRIKETHROUGH)
    group.add_argument('--strip', action='store_true',
                       help=HelpMessages.STRIP)
    group.add_argument('--title-case', action='store_true',
                       help=HelpMessages.TITLE_CASE)
    group.add_argument('--uppercase', action='store_true',
                       help=HelpMessages.UPPERCASE)

    # If the user enters the command name with no arguments, print the
    # help messages and exit.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args: argparse.Namespace = parser.parse_args()

    # Dictionary mapping argument names to text warping functions
    arg_func_map: dict[str, Callable[[str], str]] = {
        'alternating_caps': to_alternating_caps,
        'binary': to_binary,
        'camel_case': to_camel_case,
        'capitalize': capitalize,
        'cardinal': ordinal_to_cardinal,
        'curly_quotes': straight_to_curly,
        'expand_contractions': expand_contractions,
        'hexadecimal': to_hexadecimal,
        'hyphens_to_em': hyphens_to_em,
        'hyphen_to_en': hyphen_to_en,
        'kebab_case': to_kebab_case,
        'lowercase': to_lowercase,
        'ordinal': cardinal_to_ordinal,
        'pascal_case': to_pascal_case,
        'punct_to_inside': punct_to_inside,
        'punct_to_outside': punct_to_outside,
        'sentence_case': to_sentence_case,
        'single_spaces': to_single_spaces,
        'snake_case': to_snake_case,
        'straight_quotes': curly_to_straight,
        'strikethrough': strikethrough,
        'strip': lambda text: text.strip(),
        'title_case': to_title_case,
        'uppercase': to_uppercase
    }

    for arg_label, func in arg_func_map.items():
        if getattr(args, arg_label):
            return func


def _calculate_max_arg_width(commands: dict) -> int:
    """
    Calculate the length of the longest command string.

    Args:
        commands (dict): A dictionary mapping command names to their
            corresponding functions and help messages.

    Returns:
        int: The length of the longest command string, adjusted for
            formatting.
    """
    adjustment: int = 6 # Account for the '--' prefix and whitespace.
    return max(len(key) + adjustment for key in commands.keys())
