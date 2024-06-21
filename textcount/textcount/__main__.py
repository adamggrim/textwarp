from textcount.formatting import FormatPrinting
from textcount.input_output import process_analysis, program_exit
from textcount.parsing import parse_args


def main() -> None:
    """Initiates an instance of a text analysis function."""
    processing_function = parse_args()

    while True:
        try:
            process_analysis(processing_function)
        except KeyboardInterrupt:
            FormatPrinting.print_padding()
            program_exit()