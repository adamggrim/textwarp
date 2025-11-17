"""
The main entry point for the package.

This module is responsible for:
1.  Parsing command-line arguments.
2.  Defining command groups (warping, analysis, replacement and
    clearing).
3.  Dispatching the parsed command to the relevant runner function.
"""

from ._args import ARGS_MAP
from ._commands import _analysis
from ._commands import _replacement
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

# A set of all warping, analysis, replacement and clearing function
# names, each converted from its hyphenated ARGS_MAP key to its
# underscored version.
ALL_FUNC_NAMES: set[str] = {
    key.replace('-', '_') for key in ARGS_MAP.keys()
}

# All function names for analysis commands.
ANALYSIS_FUNC_NAMES: set[str] = set(_analysis.__all__)

# All function names for replacement commands.
REPLACEMENT_FUNC_NAMES: set[str] = set(_replacement.__all__)

# Signal set to represent the ``clear_clipboard`` function with the
# ``clear`` command name.
CLEAR_FUNC_NAMES: set[str] = {'clear'}


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
