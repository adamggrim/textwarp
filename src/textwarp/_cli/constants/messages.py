"""Strings for displaying CLI messages."""

from typing import Final

from textwarp._core.context import N_

__all__ = [
    'ANALYSIS_ORDER_ERROR_MSG',
    'ANY_OTHER_TEXT_PROMPT',
    'BINARY_FILE_ERROR_MSG',
    'CASE_EMPTY_ERROR_MSG',
    'CASE_TO_REPLACE_NOT_FOUND_MSG',
    'CASE_WHITESPACE_ERROR_MSG',
    'CLIPBOARD_ACCESS_ERROR_MSG',
    'CLIPBOARD_CLEARED_MSG',
    'CLIPBOARD_EMPTY_ERROR_MSG',
    'CLIPBOARD_WHITESPACE_ERROR_MSG',
    'CMD_AFTER_FILE_ERROR_MSG',
    'ENTER_CASE_TO_REPLACE_PROMPT',
    'ENTER_ENTITY_COUNT_PROMPT',
    'ENTER_MFW_COUNT_PROMPT',
    'ENTER_REGEX_PROMPT',
    'ENTER_REPLACEMENT_CASE_PROMPT',
    'ENTER_REPLACEMENT_TEXT_PROMPT',
    'ENTER_TEXT_TO_REPLACE_PROMPT',
    'ENTER_VALID_CASE_PROMPT',
    'ENTER_VALID_NUMBER_PROMPT',
    'ENTER_VALID_REGEX_PROMPT',
    'ENTER_VALID_RESPONSE_PROMPT',
    'ENTER_VALID_TEXT_PROMPT',
    'ENTER_WPM_PROMPT',
    'EXCLUSIVE_CMD_ERROR_MSG',
    'EXIT_MSG',
    'FILE_ACCESS_ERROR_MSG',
    'FILE_NOT_FOUND_CMD_HINT_ERROR_MSG',
    'FILE_SIZE_LIMIT_ERROR_MSG',
    'FILE_WRITE_ERROR_MSG',
    'FILE_WRITE_SUCCESS_MSG',
    'FIND_REPLACE_ARG_ERROR_MSG',
    'HELP_DESCRIPTION',
    'INTERACTIVE_CMD_ERROR_MSG',
    'INVALID_CASE_ERROR_MSG',
    'LINUX_XCLIP_WARNING_MSG',
    'MODIFIED_TEXT_COPIED_MSG',
    'MULTIPLE_MUTUALLY_EXCLUSIVE_ERROR_MSG',
    'MULTIPLE_REPLACEMENT_ERROR_MSG',
    'NO_ENTITIES_FOUND_MSG',
    'PIPED_INPUT_ERROR_MSG',
    'POSITIVE_INT_ARG_ERROR_MSG',
    'REGEX_EMPTY_ERROR_MSG',
    'REGEX_TO_REPLACE_NOT_FOUND_MSG',
    'REPLACEMENT_CMD_ERROR_MSG',
    'TEXT_EMPTY_ERROR_MSG',
    'TEXT_TO_REPLACE_NOT_FOUND_MSG',
    'TOP_ARG_ERROR_MSG',
    'UNEXPECTED_CLIPBOARD_ERROR_MSG',
    'UNRECOGNIZED_CMD_ERROR_MSG',
    'UNRECOGNIZED_CMD_HINT_ERROR_MSG',
    'WPM_ARG_ERROR_MSG'
]

ANALYSIS_ORDER_ERROR_MSG: Final = N_(
    "Command '{cmd}' cannot follow an analysis command. Analysis commands "
    'belong at the end of the pipeline.'
)
ANY_OTHER_TEXT_PROMPT: Final = N_(
    'Any other text? (y/n) (Copy text to clipboard):'
)
BINARY_FILE_ERROR_MSG: Final = N_(
    "Error: '{input_file}' appears to be a binary file. Please provide a "
    "valid text file."
)
CASE_EMPTY_ERROR_MSG: Final = N_('Case input is empty.')
CASE_TO_REPLACE_NOT_FOUND_MSG: Final = N_('Case to replace not found.')
CASE_WHITESPACE_ERROR_MSG: Final = N_('Case contains only whitespace.')
CLIPBOARD_ACCESS_ERROR_MSG: Final = N_('Error accessing clipboard: ')
CLIPBOARD_CLEARED_MSG: Final = N_('Clipboard text cleared.')
CLIPBOARD_EMPTY_ERROR_MSG: Final = N_('Clipboard is empty.')
CLIPBOARD_WHITESPACE_ERROR_MSG: Final = N_(
    'Clipboard contains only whitespace.'
)
CMD_AFTER_FILE_ERROR_MSG: Final = N_(
    "Command '{cmd}' cannot follow an input file. Commands must "
    'precede input files.'
)
ENTER_CASE_TO_REPLACE_PROMPT: Final = N_('Enter a case to replace:')
ENTER_ENTITY_COUNT_PROMPT: Final = N_('How many entities?')
ENTER_MFW_COUNT_PROMPT: Final = N_('How many most frequent words?')
ENTER_REGEX_PROMPT: Final = N_('Enter a regular expression to replace:')
ENTER_REPLACEMENT_CASE_PROMPT: Final = N_('Enter a replacement case:')
ENTER_REPLACEMENT_TEXT_PROMPT: Final = N_('Enter replacement text:')
ENTER_TEXT_TO_REPLACE_PROMPT: Final = N_('Enter text to replace:')
ENTER_VALID_CASE_PROMPT: Final = N_('Please enter a valid case.')
ENTER_VALID_NUMBER_PROMPT: Final = N_('Please enter a valid number.')
ENTER_VALID_REGEX_PROMPT: Final = N_(
    'Please enter a valid regular expression.'
)
ENTER_VALID_RESPONSE_PROMPT: Final = N_('Please enter a valid response (y/n).')
ENTER_VALID_TEXT_PROMPT: Final = N_('Please enter valid text.')
ENTER_WPM_PROMPT: Final = N_('How many words per minute?')
EXCLUSIVE_CMD_ERROR_MSG: Final = N_(
    "Command '{cmd}' cannot be combined with other commands."
)
EXIT_MSG: Final = N_('Exiting the program...')
FILE_ACCESS_ERROR_MSG: Final = N_(
    "Error accessing file '{file_path}': {error}"
)
FILE_NOT_FOUND_CMD_HINT_ERROR_MSG: Final = N_(
    "File '{file}' not found. Did you mean command '{match}'?"
)
FILE_SIZE_LIMIT_ERROR_MSG: Final = N_(
    'File exceeds {limit}MB limit.'
)
FILE_WRITE_ERROR_MSG: Final = N_('Error writing to output file: {error}')
FILE_WRITE_SUCCESS_MSG: Final = N_(
    "Modified text successfully written to '{output_file}'."
)
FIND_REPLACE_ARG_ERROR_MSG: Final = N_(
    "The '--find (-f)' and '--replace (-r)' arguments can only be used with "
    "replacement commands ('replace-text', 'replace-case', 'replace-regex')."
)
HELP_DESCRIPTION: Final = N_(
    'Specify a sequence of text warping or analysis commands to apply to the '
    'text.'
)
INTERACTIVE_CMD_ERROR_MSG: Final = N_(
    "The '{cmd_name}' command requires interactive input and cannot be used "
    'in file or piped mode.'
)
INVALID_CASE_ERROR_MSG: Final = N_('Invalid case.')
LINUX_XCLIP_WARNING_MSG: Final = N_(
    "\nOn Linux, you may need to install 'xclip' or 'xsel' "
    '(e.g., sudo apt install xclip).'
)
MODIFIED_TEXT_COPIED_MSG: Final = N_('Modified text copied to clipboard.')
MULTIPLE_MUTUALLY_EXCLUSIVE_ERROR_MSG: Final = N_(
    'Cannot combine multiple mutually exclusive commands: {commands}'
)
MULTIPLE_REPLACEMENT_ERROR_MSG: Final = N_(
    'Cannot combine multiple replacement commands: {commands}'
)
NO_ENTITIES_FOUND_MSG: Final = N_('No entities found.')
PIPED_INPUT_ERROR_MSG: Final = N_('Error processing input: {error}')
POSITIVE_INT_ARG_ERROR_MSG: Final = N_(
    'The {flag} argument must be a positive integer.'
)
REGEX_EMPTY_ERROR_MSG: Final = N_('Regex input is empty.')
REGEX_TO_REPLACE_NOT_FOUND_MSG: Final = N_(
    'Regular expression to replace not found.'
)
REPLACEMENT_CMD_ERROR_MSG: Final = N_(
    "Replacement commands require '--find' and '--replace' arguments when "
    'used in file or piped mode.'
)
TEXT_EMPTY_ERROR_MSG: Final = N_('Text input is empty.')
TEXT_TO_REPLACE_NOT_FOUND_MSG: Final = N_('Text to replace not found.')
TOP_ARG_ERROR_MSG: Final = N_(
    "The --top (-n) argument can only be used with 'entity-counts' or 'mfws'."
)
UNEXPECTED_CLIPBOARD_ERROR_MSG: Final = N_(
    'An unexpected error occurred while accessing the clipboard.'
)
UNRECOGNIZED_CMD_ERROR_MSG: Final = N_(
    "Unrecognized command: '{cmd}'."
)
UNRECOGNIZED_CMD_HINT_ERROR_MSG: Final = N_(
    "Unrecognized command: '{cmd}'. Did you mean '{match}'?"
)
WPM_ARG_ERROR_MSG: Final = N_(
    "The --wpm (-w) argument can only be used with 'time-to-read'."
)
