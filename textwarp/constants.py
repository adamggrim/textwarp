# Prompt for the user to enter any other text.
ANY_OTHER_TEXT_PROMPT: str = 'Any other text? (y/n) (Copy text to clipboard):'

# Variants of 'd for contractions.
APOSTROPHE_D_VARIANTS: set[str] = {"'d", '’d', '‘d'}

# Variants of 's for contractions.
APOSTROPHE_S_VARIANTS: set[str] = {"'s", '’s', '‘s'}

# Variants of apostrophes.
APOSTROPHE_VARIANTS = {"'", '’', '‘'}

# Prompt for when the previous response was invalid.
ENTER_VALID_RESPONSE_PROMPT: str = 'Please enter a valid response.'

# Inputs for exiting the program.
EXIT_INPUTS: str = {'quit', 'q', 'exit', 'e'}

# Message for when the user exits the program.
EXIT_MESSAGE: str = 'Exiting the program...'

# Help description for command-line arguments.
HELP_DESCRIPTION: str = (
    'Specify which text warping function to apply to the clipboard.'
)

# Message for when the program copies modified text to the clipboard.
MODIFIED_TEXT_COPIED: str = 'Modified text copied to clipboard.'

# Inputs for indicating a negative response.
NO_INPUTS: str = {'no', 'n'}

# Part-of-speech tag for past participles.
PAST_PARTICIPLE_TAGS: set[str] = {'VBN', 'VBD'}

# Inputs for indicating an affirmative response.
YES_INPUTS: str = {'yes', 'y'}
