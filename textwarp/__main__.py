"""The main entry point for the package, containing the main loop."""

from ._cli.args import ARGS_MAP
from ._cli.parsing import parse_args
from ._cli.runners import (
    analyze_text,
    clear_clipboard,
    replace_text,
    warp_text
)
from ._cli.ui import (
    print_padding,
    program_exit
)
from ._commands import analysis
from ._commands import replacement

# A set of all warping, analysis, replacement and clearing function
# names, each converted from its hyphenated ARGS_MAP key to its
# underscored version.
_ALL_FUNC_NAMES: set[str] = {
    key.replace('-', '_') for key in ARGS_MAP.keys()
}

# All function names for analysis commands.
_ANALYSIS_FUNC_NAMES: set[str] = set(analysis.__all__)

# All function names for replacement commands.
_REPLACEMENT_FUNC_NAMES: set[str] = set(replacement.__all__)

# Signal set to represent the ``clear_clipboard`` function with the
# ``clear`` command name.
_CLEAR_FUNC_NAMES: set[str] = {'clear'}


def main() -> None:
    """Run the main loop for text transformation or analysis."""
    command_name: str # Hyphenated command name
    func_name: str # Underscored function name
    command_name, func_name = parse_args()

    try:
        if func_name in _ANALYSIS_FUNC_NAMES:
            analyze_text(func_name)
        elif func_name in _REPLACEMENT_FUNC_NAMES:
            replace_text(func_name)
        elif func_name in _CLEAR_FUNC_NAMES:
            clear_clipboard()
        # Any function that is not for analysis, replacement or clearing
        # is for warping.
        elif func_name in _ALL_FUNC_NAMES:
            warp_text(func_name)
        else:
            # Print the user-facing command name in the error.
            print(f"\nCommand '{command_name}' not recognized.")
        program_exit()
    except KeyboardInterrupt:
        print_padding()
        program_exit()
