"""
This module contains constants of various types used across the package.
"""

from typing import Final

# Variants of 's for contractions.
AIN_T_SUFFIX_VARIANTS: Final = {"n't", 'n’t', 'n‘t'}

# Prompt for the user to enter any other text.
ANY_OTHER_TEXT_PROMPT: Final = (
    'Any other text? (y/n) (Copy text to clipboard):'
)

# Variants of 'd for contractions.
APOSTROPHE_D_VARIANTS: Final = {"'d", '’d', '‘d'}

# Variants of 's for contractions.
APOSTROPHE_S_VARIANTS: Final = {"'s", '’s', '‘s'}

# Variants of apostrophes.
APOSTROPHE_VARIANTS: Final = {"'", '’', '‘'}

# Message for any error accessing the clipboard.
CLIPBOARD_ACCESS_ERROR_MESSAGE: Final = 'Error accessing clipboard: '

# Message for when the clipboard is cleared.
CLIPBOARD_CLEARED_MESSAGE: Final = 'Clipboard text cleared.'

# Prompt for the user to enter a case to replace.
ENTER_CASE_TO_REPLACE_PROMPT: Final = 'Enter the case to replace:'

# Prompt for the user to enter the number of most frequent words.
ENTER_MFW_COUNT_PROMPT: Final = 'How many most frequent words?'

# Prompt for when the previous response was not a number.
ENTER_NUMBER_PROMPT: Final = 'Please enter a number.'

# Prompt for the user to enter a regular expression to find.
ENTER_REGEX_PROMPT: Final = 'Enter a regular expression to replace:'

# Prompt for the user to enter a replacement case.
ENTER_REPLACEMENT_CASE_PROMPT: Final = 'Enter replacement case:'

# Prompt for the user to enter replacement text.
ENTER_REPLACEMENT_TEXT_PROMPT: Final = 'Enter replacement text:'

# Prompt for the user to enter text to find.
ENTER_TEXT_TO_REPLACE_PROMPT: Final = 'Enter text to replace:'

# Prompt for when the previous response was invalid.
ENTER_VALID_RESPONSE_PROMPT: Final = 'Please enter a valid response (y/n).'

# Prompt for the user to enter the words per minute.
ENTER_WPM_PROMPT: Final = 'How many words per minute?'

# Inputs for exiting the program.
EXIT_INPUTS: Final = {'quit', 'q', 'exit', 'e'}

# Message for when the user exits the program.
EXIT_MESSAGE: Final = 'Exiting the program...'

# Help description for command-line arguments.
HELP_DESCRIPTION: Final = (
    'Specify which text warping function to apply to the clipboard.'
)

# Message for when the program copies modified text to the clipboard.
MODIFIED_TEXT_COPIED_MESSAGE: Final = 'Modified text copied to clipboard.'

# Inputs for indicating a negative response.
NO_INPUTS: Final = {'no', 'n'}

# Opening quote characters.
OPEN_QUOTES: Final = {'"', '“', "'", '‘'}

# Tuple of tuples for all part-of-speech tags and their names.
POS_TAGS: Final[tuple[tuple[str, str], ...]] = (
    ('ADJ', 'Adjectives'),
    ('ADP', 'Adpositions'),
    ('ADV', 'Adverbs'),
    ('CONJ', 'Conjunctions'),
    ('DET', 'Determiners'),
    ('NOUN', 'Nouns'),
    ('NUM', 'Numbers'),
    ('PART', 'Particles'),
    ('PRON', 'Pronouns'),
    ('VERB', 'Verbs'),
    ('X', 'Other')
)

# Tuple of strings for all part-of-speech tags representing words.
POS_WORD_TAGS: Final[tuple[str, ...]] = tuple(
    item[0] for item in POS_TAGS if item[0] != 'X'
)

# Named entities that are typically proper nouns.
PROPER_NOUN_ENTITIES: Final = {
    'PERSON',
    'GPE',
    'ORG',
    'NORP',
    'FAC',
    'LOC',
    'PRODUCT',
    'EVENT',
    'WORK_OF_ART',
    'LAW'
}

# Message for when the text to replace is not found in the text.
TEXT_TO_REPLACE_NOT_FOUND_MESSAGE: Final = 'Text to replace not found.'

# Part-of-speech tag exceptions for title case capitalization.
TITLE_CASE_TAG_EXCEPTIONS: Final = {
    'CC',   # Coordinating conjunction (e.g., 'and', 'but')
    'DT',   # Determiner (e.g., 'a', 'an', 'the')
    'IN',   # Preposition or subordinating conjunction
            # (e.g., 'in', 'of', 'on')
    'RP',   # Particle (e.g., 'in' in 'give in')
    'TO',   # to (infinitive marker)
    'WDT',  # Wh-determiner (e.g., 'what')
}

# Inputs for indicating an affirmative response.
YES_INPUTS: Final = {'yes', 'y'}
