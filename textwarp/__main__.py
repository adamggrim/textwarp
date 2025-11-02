from textwarp._parsing import parse_args
from textwarp._ui import (
    warp_text,
    print_padding,
    program_exit
)


def main() -> None:
    """Run the main loop for text warping."""
    warping_function: str = parse_args()

    try:
        warp_text(warping_function)
        program_exit()
    except KeyboardInterrupt:
        print_padding()
        program_exit()
