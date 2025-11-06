import textwarp._analysis_commands as analysis_mod
import textwarp.warping as warping_mod

from ._parsing import parse_args
from ._runners import (
    analyze_text,
    warp_text
)
from ._ui import (
    print_padding,
    program_exit
)

WARPING_COMMANDS: set[str] = set(warping_mod.__all__)
ANALYSIS_COMMANDS: set[str] = set(analysis_mod.__all__)


def main() -> None:
    """Run the main loop for text warping."""
    command_name: str = parse_args()

    try:
        if command_name in WARPING_COMMANDS:
            warp_text(command_name)
        elif command_name in ANALYSIS_COMMANDS:
            analyze_text(command_name)
        else:
            print(f"Command '{command_name}' not recognized.")
        program_exit()
    except KeyboardInterrupt:
        print_padding()
        program_exit()
