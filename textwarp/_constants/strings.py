"""
This module contains strings used across the package.
"""

from typing import Final

__all__ = [
    'ANY_OTHER_TEXT_PROMPT',
    'CLIPBOARD_ACCESS_ERROR_MESSAGE',
    'CLIPBOARD_CLEARED_MESSAGE',
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
    'EXIT_MESSAGE',
    'HELP_DESCRIPTION',
    'MODIFIED_TEXT_COPIED_MESSAGE',
    'TEXT_TO_REPLACE_NOT_FOUND_MESSAGE'
]

# Prompt for the user to enter any other text.
ANY_OTHER_TEXT_PROMPT: Final = (
    'Any other text? (y/n) (Copy text to clipboard):'
)

# Message for any error accessing the clipboard.
CLIPBOARD_ACCESS_ERROR_MESSAGE: Final = 'Error accessing clipboard: '

# Message for when the clipboard is cleared.
CLIPBOARD_CLEARED_MESSAGE: Final = 'Clipboard text cleared.'

# Prompt for the user to enter a case to replace.
ENTER_CASE_TO_REPLACE_PROMPT: Final = 'Enter a case to replace:'

# Prompt for the user to enter the number of most frequent words.
ENTER_MFW_COUNT_PROMPT: Final = 'How many most frequent words?'

# Prompt for the user to enter a regular expression to find.
ENTER_REGEX_PROMPT: Final = 'Enter a regular expression to replace:'

# Prompt for the user to enter a replacement case.
ENTER_REPLACEMENT_CASE_PROMPT: Final = 'Enter a replacement case:'

# Prompt for the user to enter replacement text.
ENTER_REPLACEMENT_TEXT_PROMPT: Final = 'Enter replacement text:'

# Prompt for the user to enter text to find.
ENTER_TEXT_TO_REPLACE_PROMPT: Final = 'Enter text to replace:'

# Prompt for when the previous case name was invalid.
ENTER_VALID_CASE_PROMPT: Final = 'Please enter a valid case.'

# Prompt for when the previous response was not a number.
ENTER_VALID_NUMBER_PROMPT: Final = 'Please enter a valid number.'

# Prompt for when the previous regex was invalid.
ENTER_VALID_REGEX_PROMPT: Final = 'Please enter a valid regular expression.'

# Prompt for when the previous response was invalid.
ENTER_VALID_RESPONSE_PROMPT: Final = 'Please enter a valid response (y/n).'

# Prompt for when the previous text was invalid.
ENTER_VALID_TEXT_PROMPT: Final = 'Please enter valid text.'

# Prompt for the user to enter the words per minute.
ENTER_WPM_PROMPT: Final = 'How many words per minute?'

# Message for when the user exits the program.
EXIT_MESSAGE: Final = 'Exiting the program...'

# Help description for command-line arguments.
HELP_DESCRIPTION: Final = (
    'Specify which text warping function to apply to the clipboard.'
)

# Message for when the program copies modified text to the clipboard.
MODIFIED_TEXT_COPIED_MESSAGE: Final = 'Modified text copied to clipboard.'

# Message for when the text to replace is not found in the text.
TEXT_TO_REPLACE_NOT_FOUND_MESSAGE: Final = 'Text to replace not found.'
