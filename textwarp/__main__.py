from textwarp.input_output import (
    convert_text,
    print_padding,
    program_exit
)
from textwarp.parsing import parse_args


def main() -> None:
    """Runs the main loop for text conversion."""
    conversion_function: str = parse_args()

    try:
        convert_text(conversion_function)
        program_exit()
    except KeyboardInterrupt:
        print_padding()
        program_exit()
