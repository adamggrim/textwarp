from textwarp.input_output import (
    warp_text,
    print_padding,
    program_exit
)
from textwarp.parsing import parse_args


def main() -> None:
    """Run the main loop for text warping."""
    warping_function: str = parse_args()

    try:
        warp_text(warping_function)
        program_exit()
    except KeyboardInterrupt:
        print_padding()
        program_exit()
