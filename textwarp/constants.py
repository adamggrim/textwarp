# Prompt for the user to enter any other text.
ANY_OTHER_TEXT_PROMPT: str = 'Any other text? (y/n) (Copy text to clipboard):'

# Variants of 'd for contractions.
APOSTROPHE_D_VARIANTS: set[str] = {"'d", '’d', '‘d'}

# Variants of 's for contractions.
APOSTROPHE_S_VARIANTS: set[str] = {"'s", '’s', '‘s'}

# Variants of apostrophes.
APOSTROPHE_VARIANTS: set[str] = {"'", '’', '‘'}

# Message for any error accessing the clipboard.
CLIPBOARD_ACCESS_ERROR_MESSAGE: str = 'Error accessing clipboard: '

# Prompt for when the previous response was invalid.
ENTER_VALID_RESPONSE_PROMPT: str = 'Please enter a valid response.'

# Inputs for exiting the program.
EXIT_INPUTS: set[str] = {'quit', 'q', 'exit', 'e'}

# Message for when the user exits the program.
EXIT_MESSAGE: str = 'Exiting the program...'

# Help description for command-line arguments.
HELP_DESCRIPTION: str = (
    'Specify which text warping function to apply to the clipboard.'
)

# Message for when the program copies modified text to the clipboard.
MODIFIED_TEXT_COPIED: str = 'Modified text copied to clipboard.'

# Inputs for indicating a negative response.
NO_INPUTS: set[str] = {'no', 'n'}

# Part-of-speech tag for past participles.
PAST_PARTICIPLE_TAGS: set[str] = {'VBN', 'VBD'}

# Named entities that are typically proper nouns.
PROPER_NOUN_ENTITIES: set[str]= {
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

# Part-of-speech tag exceptions for title case capitalization.
TITLE_CASE_TAG_EXCEPTIONS: set[str] = {
    'CC',   # Coordinating conjunction (e.g., 'and', 'but')
    'DT',   # Determiner (e.g., 'a', 'an', 'the')
    'IN',   # Preposition or subordinating conjunction
            # (e.g., 'in', 'of', 'on')
    'RP',   # Particle (e.g., 'in' in 'give in')
    'TO',   # to (infinitive marker)
    'WDT',  # Wh-determiner (e.g., 'what')
}

# Message for unexpected errors.
UNEXPECTED_ERROR_MESSAGE: str = 'An unexpected error occurred: '

# Inputs for indicating an affirmative response.
YES_INPUTS: set[str] = {'yes', 'y'}
