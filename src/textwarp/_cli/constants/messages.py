"""Strings for displaying command-line messages."""

import gettext
from typing import Final

from textwarp._core.context import N_

_ = gettext.gettext

__all__ = [
    'ANY_OTHER_TEXT_PROMPT',
    'CASE_EMPTY_ERROR_MSG',
    'CASE_TO_REPLACE_NOT_FOUND_MSG',
    'CASE_WHITESPACE_ERROR_MSG',
    'CLIPBOARD_ACCESS_ERROR_MSG',
    'CLIPBOARD_CLEARED_MSG',
    'CLIPBOARD_EMPTY_ERROR_MSG',
    'CLIPBOARD_WHITESPACE_ERROR_MSG',
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
    'EXIT_MSG',
    'HELP_DESCRIPTION',
    'INTERACTIVE_CMD_ERROR_MSG',
    'INVALID_CASE_ERROR_MSG',
    'MODIFIED_TEXT_COPIED_MSG',
    'NO_ENTITIES_FOUND_MSG',
    'PIPED_INPUT_ERROR_MSG',
    'FILE_SIZE_LIMIT_ERROR_MSG',
    'REGEX_TO_REPLACE_NOT_FOUND_MSG',
    'REPLACEMENT_CMD_ERROR_MSG',
    'TEXT_EMPTY_ERROR_MSG',
    'TEXT_TO_REPLACE_NOT_FOUND_MSG',
    'UNEXPECTED_CLIPBOARD_ERROR_MSG'
]

ANALYSIS_ORDER_ERROR_MSG: Final = _(
    "Command '{cmd}' cannot follow an analysis command. Analysis commands "
    "must be placed at the end of the pipeline."
)
ANY_OTHER_TEXT_PROMPT: Final = N_(
    'Any other text? (y/n) (Copy text to clipboard):'
)
BINARY_FILE_ERROR_MSG: Final = _(
    "Error: '{input_file}' appears to be a binary file. Please provide a "
    "valid text file."
)
CASE_EMPTY_ERROR_MSG: Final = _('Case input is empty.')
CASE_TO_REPLACE_NOT_FOUND_MSG: Final = _('Case to replace not found.')
CASE_WHITESPACE_ERROR_MSG: Final = _('Case contains only whitespace.')
CLIPBOARD_ACCESS_ERROR_MSG: Final = _('Error accessing clipboard: ')
CLIPBOARD_CLEARED_MSG: Final = _('Clipboard text cleared.')
CLIPBOARD_EMPTY_ERROR_MSG: Final = _('Clipboard is empty.')
CLIPBOARD_WHITESPACE_ERROR_MSG: Final = _(
    'Clipboard contains only whitespace.'
)
ENTER_CASE_TO_REPLACE_PROMPT: Final = _('Enter a case to replace:')
ENTER_ENTITY_COUNT_PROMPT: Final = _('How many entities?')
ENTER_MFW_COUNT_PROMPT: Final = _('How many most frequent words?')
ENTER_REGEX_PROMPT: Final = _('Enter a regular expression to replace:')
ENTER_REPLACEMENT_CASE_PROMPT: Final = _('Enter a replacement case:')
ENTER_REPLACEMENT_TEXT_PROMPT: Final = _('Enter replacement text:')
ENTER_TEXT_TO_REPLACE_PROMPT: Final = _('Enter text to replace:')
ENTER_VALID_CASE_PROMPT: Final = _('Please enter a valid case.')
ENTER_VALID_NUMBER_PROMPT: Final = _('Please enter a valid number.')
ENTER_VALID_REGEX_PROMPT: Final = _('Please enter a valid regular expression.')
ENTER_VALID_RESPONSE_PROMPT: Final = _('Please enter a valid response (y/n).')
ENTER_VALID_TEXT_PROMPT: Final = _('Please enter valid text.')
ENTER_WPM_PROMPT: Final = _('How many words per minute?')
EXCLUSIVE_CMD_ERROR_MSG: Final = _(
    "Command '{cmd}' cannot be combined with other commands."
)
EXIT_MSG: Final = _('Exiting the program...')
FILE_ACCESS_ERROR_MSG: Final = _("Error accessing file '{file_path}': {error}")
FILE_WRITE_ERROR_MSG: Final = _('Error writing to output file: {error}')
FILE_SIZE_LIMIT_ERROR_MSG: Final = _(
    'File exceeds {limit}MB limit.'
)
FILE_WRITE_SUCCESS_MSG: Final = _(
    "Modified text successfully written to '{output_file}'."
)
FIND_REPLACE_ARG_ERROR_MSG: Final = _(
    'The --find (-f) and --replace (-r) arguments can only be used with '
    'replacement commands (replace-text, replace-case, replace-regex).'
)
HELP_DESCRIPTION: Final = _(
    'Specify a sequence of text warping or analysis commands to apply to the '
    'text.'
)
INTERACTIVE_CMD_ERROR_MSG: Final = _(
    "The '{cmd_name}' command requires interactive input and cannot be used "
    'in file or piped mode.'
)
INVALID_CASE_ERROR_MSG: Final = _('Invalid case.')
LINUX_XCLIP_WARNING_MSG: Final = _(
    "\nOn Linux, you may need to install 'xclip' or 'xsel' "
    '(e.g., sudo apt install xclip).'
)
MODIFIED_TEXT_COPIED_MSG: Final = _('Modified text copied to clipboard.')
MULTIPLE_MUTUALLY_EXCLUSIVE_ERROR_MSG: Final = _(
    'Cannot combine multiple mutually exclusive commands: {commands}'
)
MULTIPLE_REPLACEMENT_ERROR_MSG: Final = _(
    'Cannot combine multiple replacement commands: {commands}'
)
NO_ENTITIES_FOUND_MSG: Final = _('No entities found.')
PIPED_INPUT_ERROR_MSG: Final = _('Error processing input: {error}')
REGEX_EMPTY_ERROR_MSG: Final = _('Regex input is empty.')
REGEX_TO_REPLACE_NOT_FOUND_MSG: Final = _(
    'Regular expression to replace not found.'
)
REPLACEMENT_CMD_ERROR_MSG: Final = _(
    'Replacement commands require --find and --replace arguments when used '
    'in file or piped mode.'
)
TEXT_EMPTY_ERROR_MSG: Final = _('Text input is empty.')
TEXT_TO_REPLACE_NOT_FOUND_MSG: Final = _('Text to replace not found.')
UNEXPECTED_CLIPBOARD_ERROR_MSG: Final = _(
    'An unexpected error occurred while accessing the clipboard.'
)
