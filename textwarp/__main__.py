"""
The main entry point for the package.

This module is responsible for:
1.  Parsing command-line arguments.
2.  Defining command groups (warping, analysis, replacement and
    clearing).
3.  Dispatching the parsed command to the relevant runner function.
"""

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
    command_name: str # Hyphenated command name
    func_name: str # Underscored function name
    command_name, func_name = parse_args()

    try:
        if func_name in ANALYSIS_FUNC_NAMES:
            analyze_text(func_name)
        elif func_name in REPLACEMENT_FUNC_NAMES:
            replace_text(func_name)
        elif func_name in CLEAR_FUNC_NAMES:
            clear_clipboard()
        # Any function that is not for analysis, replacement or clearing
        # is for warping.
        elif func_name in ALL_FUNC_NAMES:
            warp_text(func_name)
        else:
            # Print the user-facing command name in the error.
            print(f"\nCommand '{command_name}' not recognized.")
        program_exit()
    except KeyboardInterrupt:
        print_padding()
        program_exit()
