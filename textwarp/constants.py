class HelpMessages:
    """
    Help message strings for command-line arguments.

    Attributes:
        DESCRIPTION: Description for textwarp arguments

        ALTERNATING_CAPS: Help message for --alternating-caps argument
        CAMEL_CASE: Help message for --camel-case argument
        CAPITALIZE: Help message for --capitalize argument
        CARDINAL: Help message for --cardinals argument
        CURLY_QUOTES: Help message for --curly argument
        HYPHENS_TO_EM: Help message for --hyphens-to-em argument
        HYPHENS_TO_EN: Help message for --hyphens-to-en argument
        KEBAB_CASE: Help message for --kebab-case argument
        LOWERCASE: Help message for --lowercase argument
        ORDINAL: Help message for --ordinals argument
        PASCAL_CASE: Help message for --pascal-case argument
        PUNCT_TO_INSIDE: Help message for --punct-to-inside argument
        PUNCT_TO_OUTSIDE: Help message for --punct-to-outside argument
        SNAKE_CASE: Help message for --snake-case argument
        STRAIGHT_QUOTES: Help message for --straight argument
        TITLE_CASE: Help message for --title-case argument
        UPPERCASE: Help message for --uppercase argument
    """
    DESCRIPTION: str = (
        'Specify which text warping function to apply to the clipboard.'
    )

    ALTERNATING_CAPS: str = 'convert to alternating caps'
    CAMEL_CASE: str = 'convert to camel case'
    CAPITALIZE: str = 'capitalize the first character of each word'
    CARDINAL: str = 'convert ordinal numbers to cardinal numbers'
    CURLY_QUOTES: str = 'convert straight quotes to curly quotes'
    HYPHENS_TO_EM: str = 'convert consecutive hyphens to em dashes'
    HYPHEN_TO_EN: str = 'convert hyphens to en dashes'
    KEBAB_CASE: str = 'convert to kebab case'
    LOWERCASE: str = 'convert to lowercase'
    ORDINAL: str = 'convert cardinal numbers to ordinal numbers'
    PASCAL_CASE: str = 'convert to Pascal case'
    PUNCT_TO_INSIDE: str = 'move punctuation inside quotation marks'
    PUNCT_TO_OUTSIDE: str = 'move punctuation outside quotation marks'
    SNAKE_CASE: str = 'convert to snake case'
    STRAIGHT_QUOTES: str = 'convert curly quotes to straight quotes'
    TITLE_CASE: str = 'convert to title case'
    UPPERCASE: str = 'convert to uppercase'

# String printed to prompt the user for any other text
ANY_OTHER_TEXT_PROMPT: str = 'Any other text? (y/n) (Copy text to clipboard):'

# String printed when the previous response was invalid
ENTER_VALID_RESPONSE_PROMPT: str = 'Please enter a valid response.'

# Set of strings for exiting the program
EXIT_INPUTS: str = {'quit', 'q', 'exit', 'e'}

# String printed when the user exits the program
EXIT_MESSAGE: str = 'Exiting the program...'

# String printed when the program copies modified text to the clipboard
MODIFED_TEXT_MESSAGE: str = 'Modified text copied to clipboard.'

# Set of strings for indicating a negative response
NO_INPUTS: str = {'no', 'n'}

# Set of strings for indicating an affirmative response
YES_INPUTS: str = {'yes', 'y'}
