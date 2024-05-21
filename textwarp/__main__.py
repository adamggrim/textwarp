# from textwarp.constants import ENTER_ARGUMENT_STR
from textwarp.input_output import (convert_text, print_padding, print_wrapped, 
                                   program_exit)
from textwarp.parsing import parse_args


def main() -> None:
    """Initiates an instance of a text warping function."""
    conversion_function = parse_args()

    # if conversion_function is None:
    #     print_wrapped(ENTER_ARGUMENT_STR)

    while True:
        try:
            convert_text(conversion_function)
        except KeyboardInterrupt:
            print_padding()
            program_exit()