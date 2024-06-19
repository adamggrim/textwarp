from textcount.input_output import (print_analysis, print_padding, 
                                   program_exit)
from textcount.parsing import parse_args


def main() -> None:
    """Initiates an instance of a text analysis function."""
    printing_function = parse_args()

    while True:
        try:
            print_analysis(printing_function)
        except KeyboardInterrupt:
            print_padding()
            program_exit()