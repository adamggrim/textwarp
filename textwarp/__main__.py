from textwarp.input_output import (
    convert_text, 
    print_padding, 
    program_exit
)
from textwarp.parsing import parse_args


def main() -> None:
    """Initiates an instance of a text warping function."""
    conversion_function = parse_args()

    while True:
        try:
            convert_text(conversion_function)
        except KeyboardInterrupt:
            print_padding()
            program_exit()
