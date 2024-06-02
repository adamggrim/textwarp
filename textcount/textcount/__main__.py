from textcount.input_output import (analyze_text, print_padding, 
                                   program_exit)
from textcount.parsing import parse_args


def main() -> None:
    """Initiates an instance of a text analysis function."""
    analysis_function = parse_args()

    while True:
        try:
            analyze_text(analysis_function)
        except KeyboardInterrupt:
            print_padding()
            program_exit()