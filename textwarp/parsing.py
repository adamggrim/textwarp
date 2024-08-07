import argparse
from typing import Callable

from textwarp.constants import HelpMessages
from textwarp.warping import (capitalize, cardinal_to_ordinal, 
                              curly_to_straight, hyphens_to_em, hyphen_to_en,
                              punct_to_inside, punct_to_outside, 
                              straight_to_curly, to_alternating_caps, 
                              to_camel_case, to_kebab_case, to_lowercase, 
                              to_pascal_case, to_snake_case, to_title_case, 
                              to_uppercase)


def parse_args() -> Callable[[str], str]:
    """
    Parses command-line arguments for a text warping function 
        specification.

    Returns:
        Callable[[str], str]: The text warping function corresponding 
            to the specified command-line argument.
    """
    parser = argparse.ArgumentParser(description=HelpMessages.DESCRIPTION)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--alternating-caps', action='store_true', 
                       help=HelpMessages.ALTERNATING_CAPS)
    group.add_argument('--camel-case', action='store_true', 
                       help=HelpMessages.CAMEL_CASE)
    group.add_argument('--capitalize', action='store_true', 
                       help=HelpMessages.CAPITALIZE)
    group.add_argument('--cardinal-to-ordinal', action='store_true', 
                       help=HelpMessages.CARDINAL_TO_ORDINAL)
    group.add_argument('--curly-to-straight', action='store_true', 
                       help=HelpMessages.CURLY_TO_STRAIGHT)
    group.add_argument('--hyphens-to-em', action='store_true', 
                       help=HelpMessages.HYPHENS_TO_EM)
    group.add_argument('--hyphen-to-en', action='store_true', 
                       help=HelpMessages.HYPHEN_TO_EN)
    group.add_argument('--kebab-case', action='store_true', 
                       help=HelpMessages.KEBAB_CASE)
    group.add_argument('--lowercase', action='store_true', 
                       help=HelpMessages.LOWERCASE)
    group.add_argument('--pascal-case', action='store_true', 
                       help=HelpMessages.PASCAL_CASE)
    group.add_argument('--punct-to-inside', action='store_true', 
                       help=HelpMessages.PUNCT_TO_INSIDE)
    group.add_argument('--punct-to-outside', action='store_true', 
                       help=HelpMessages.PUNCT_TO_OUTSIDE)
    group.add_argument('--snake-case', action='store_true', 
                       help=HelpMessages.SNAKE_CASE)
    group.add_argument('--straight-to-curly', action='store_true', 
                       help=HelpMessages.STRAIGHT_TO_CURLY)
    group.add_argument('--title-case', action='store_true', 
                       help=HelpMessages.TITLE_CASE)
    group.add_argument('--uppercase', action='store_true', 
                       help=HelpMessages.UPPERCASE)
    args = parser.parse_args()

    # Dictionary mapping argument names to text warping functions
    arg_func_dict = {
        'alternating_caps': to_alternating_caps,
        'camel_case': to_camel_case,
        'capitalize': capitalize,
        'cardinal_to_ordinal': cardinal_to_ordinal,
        'curly_to_straight': curly_to_straight,
        'hyphens_to_em': hyphens_to_em,
        'hyphen_to_en': hyphen_to_en,
        'kebab_case': to_kebab_case,
        'lowercase': to_lowercase,
        'pascal_case': to_pascal_case,
        'punct_to_inside': punct_to_inside,
        'punct_to_outside': punct_to_outside,
        'snake_case': to_snake_case,
        'straight_to_curly': straight_to_curly,
        'title_case': to_title_case,
        'uppercase': to_uppercase
    }

    for arg_str, func in arg_func_dict.items():
        if getattr(args, arg_str):
            return func
