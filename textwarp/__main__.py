from ._args import ARGS_MAP
from ._commands import _analysis as analysis_mod
from ._commands import _replacement as replacement_mod
from ._parsing import parse_args
from ._runners import (
    analyze_text,
    clear_clipboard,
    replace_text,
    warp_text
)
from ._ui import (
    print_padding,
    program_exit
)

ALL_COMMANDS: set[str] = set(ARGS_MAP.keys())
ANALYSIS_COMMANDS: set[str] = set(analysis_mod.__all__)
REPLACEMENT_COMMANDS: set[str] = set(replacement_mod.__all__)
CLEAR_COMMAND: set[str] = {'clear'}
WARPING_COMMANDS: set[str] = (
    ALL_COMMANDS - ANALYSIS_COMMANDS - REPLACEMENT_COMMANDS - CLEAR_COMMAND
)

def main() -> None:
    """Run the main loop for text transformation or analysis."""
    command_name: str = parse_args()

    try:
        if command_name in ANALYSIS_COMMANDS:
            analyze_text(command_name)
        elif command_name in REPLACEMENT_COMMANDS:
            replace_text(command_name)
        elif command_name == 'clear':
            clear_clipboard()
        elif command_name in ALL_COMMANDS:
            warp_text(command_name)
        else:
            print(f"\nCommand '{command_name}' not recognized.")
        program_exit()
    except KeyboardInterrupt:
        print_padding()
        program_exit()
