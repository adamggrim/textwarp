from textcount.input_output import (print_analysis, program_exit)
from textcount.parsing import parse_args
from textcount.printing import FormatPrinting


def main() -> None:
    """Initiates an instance of a text analysis function."""
    printing_function = parse_args()

    while True:
        try:
            print_analysis(printing_function)
        except KeyboardInterrupt:
            FormatPrinting.print_padding()
            program_exit()