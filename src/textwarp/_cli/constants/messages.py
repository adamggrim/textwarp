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
    'REGEX_NOT_FOUND_MSG',
    'TEXT_NOT_FOUND_MSG'
]

ANY_OTHER_TEXT_PROMPT: Final = N_(
    'Any other text? (y/n) (Copy text to clipboard):'
)

ENTER_CASE_TO_REPLACE_PROMPT: Final = _('Enter a case to replace:')
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
REGEX_NOT_FOUND_MSG: Final = _('Regular expression not found.')
TEXT_NOT_FOUND_MSG: Final = _('Text not found.')

CLIPBOARD_ACCESS_ERROR_MSG: Final = _('Error accessing clipboard: ')
CLIPBOARD_CLEARED_MSG: Final = _('Clipboard text cleared.')

EXIT_MSG: Final = _('Exiting the program...')

HELP_DESCRIPTION: Final = _(
    'Specify which text warping function to apply to the clipboard.'
)
MODIFIED_TEXT_COPIED_MSG: Final = _('Modified text copied to clipboard.')
