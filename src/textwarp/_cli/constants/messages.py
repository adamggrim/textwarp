"""Strings for displaying command-line messages."""

import gettext
from typing import Final

from textwarp._core.context import N_

_ = gettext.gettext

__all__ = [
    'ANY_OTHER_TEXT_PROMPT',
    'CASE_NOT_FOUND_MSG',
    'CLIPBOARD_ACCESS_ERROR_MSG',
    'CLIPBOARD_CLEARED_MSG',
    'ENTER_CASE_TO_REPLACE_PROMPT',
    'ENTER_ENTITY_COUNT_PROMPT',
    'ENTER_MFW_COUNT_PROMPT',
    'ENTER_VALID_NUMBER_PROMPT',
    'ENTER_REGEX_PROMPT',
    'ENTER_REPLACEMENT_CASE_PROMPT',
    'ENTER_REPLACEMENT_TEXT_PROMPT',
    'ENTER_TEXT_TO_REPLACE_PROMPT',
    'ENTER_VALID_CASE_PROMPT',
    'ENTER_VALID_REGEX_PROMPT',
    'ENTER_VALID_RESPONSE_PROMPT',
    'ENTER_VALID_TEXT_PROMPT',
    'ENTER_WPM_PROMPT',
    'EXIT_MSG',
    'HELP_DESCRIPTION',
    'MODIFIED_TEXT_COPIED_MSG',
    'NO_ENTITIES_FOUND_MSG',
    'REGEX_NOT_FOUND_MSG',
    'TEXT_NOT_FOUND_MSG'
]

ANY_OTHER_TEXT_PROMPT: Final = N_(
    'Any other text? (y/n) (Copy text to clipboard):'
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

CASE_NOT_FOUND_MSG: Final = _('Case not found.')
NO_ENTITIES_FOUND_MSG: Final = _('No entities found.')
REGEX_NOT_FOUND_MSG: Final = _('Regular expression not found.')
TEXT_NOT_FOUND_MSG: Final = _('Text not found.')

CLIPBOARD_ACCESS_ERROR_MSG: Final = _('Error accessing clipboard: ')
CLIPBOARD_CLEARED_MSG: Final = _('Clipboard text cleared.')
EXIT_MSG: Final = _('Exiting the program...')
HELP_DESCRIPTION: Final = _(
    'Specify a sequence of text warping or analysis commands to apply to the '
    'text.'
)
MODIFIED_TEXT_COPIED_MSG: Final = _('Modified text copied to clipboard.')

ANALYSIS_ORDER_ERROR_MSG: Final = _(
    "Command '{cmd}' cannot follow an analysis command. Analysis commands "
    "must be placed at the end of the pipeline."
)
BINARY_FILE_ERROR_MSG: Final = _(
    "Error: '{input_file}' appears to be a binary file. Please provide a "
    "valid text file."
)
EXCLUSIVE_CMD_ERROR_MSG: Final = _(
    "Command '{cmd}' cannot be combined with other commands."
)
FILE_ACCESS_ERROR_MSG: Final = _("Error accessing file '{file_path}': {error}")
FILE_WRITE_ERROR_MSG: Final = _('Error writing to output file: {error}')
FILE_WRITE_SUCCESS_MSG: Final = _(
    "Modified text successfully written to '{output_file}'."
)
FIND_REPLACE_ARG_ERROR_MSG: Final = _(
    'The --find (-f) and --replace (-r) arguments can only be used with '
    'replacement commands (replace-text, replace-case, replace-regex).'
)
INTERACTIVE_CMD_ERROR_MSG: Final = _(
    "The '{cmd_name}' command requires interactive input and cannot be used "
    "in file or piped mode."
)
MULTIPLE_MUTUALLY_EXCLUSIVE_ERROR_MSG: Final = _(
    'Cannot combine multiple mutually exclusive commands: {commands}'
)
MULTIPLE_REPLACEMENT_ERROR_MSG: Final = _(
    'Cannot combine multiple replacement commands: {commands}'
)
PIPED_INPUT_ERROR_MSG: Final = _('Error processing input: {error}')
REPLACEMENT_CMD_ERROR_MSG: Final = _(
    'Replacement commands require --find and --replace arguments when used '
    'in file or piped mode.'
)
