class HelpMessages:
    """
    Help messages for command-line arguments.

    Attributes:
        DESCRIPTION: Description for textwarp arguments

        ALTERNATING_CAPS: Help message for --alternating-caps argument
        BINARY: Help message for --binary argument
        CAMEL_CASE: Help message for --camel-case argument
        CAPITALIZE: Help message for --capitalize argument
        CARDINAL: Help message for --cardinals argument
        CURLY_QUOTES: Help message for --curly argument
        EXPAND_CONTRACTIONS: Help message for --expand-contractions
            argument
        HEXADECIMAL: Help message for --hexadecimal argument
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
        STRIKETHROUGH: Help message for --strikethrough argument
        STRIP: Help message for --strip argument
        TITLE_CASE: Help message for --title-case argument
        UPPERCASE: Help message for --uppercase argument
    """
    DESCRIPTION: str = (
        'Specify which text warping function to apply to the clipboard.'
    )

    ALTERNATING_CAPS: str = 'cOnVeRt To AlTeRnAtInG cApS'
    BINARY: str = 'convert to binary'
    CAMEL_CASE: str = 'convertToCamelCase'
    CAPITALIZE: str = 'Capitalize The First Character Of Each Word'
    CARDINAL: str = 'convert ordinal numbers to cardinal numbers'
    CURLY_QUOTES: str = 'convert "straight quotes" to “curly quotes”'
    EXPAND_CONTRACTIONS: str = 'expand contractions'
    HEXADECIMAL: str = 'convert to hexadecimal'
    HYPHENS_TO_EM: str = 'convert consecutive hyphens to em dashes'
    HYPHEN_TO_EN: str = 'convert hyphens to en dashes'
    KEBAB_CASE: str = 'convert-to-kebab-case'
    LOWERCASE: str = 'convert to lowercase'
    ORDINAL: str = 'convert cardinal numbers to ordinal numbers'
    PASCAL_CASE: str = 'ConvertToPascalCase'
    PUNCT_TO_INSIDE: str = '"move punctuation inside quotation marks."'
    PUNCT_TO_OUTSIDE: str = '"move punctuation outside quotation marks".'
    SENTENCE_CASE: str = 'Convert to sentence case.'
    SINGLE_SPACES: str = 'convert consecutive spaces to a single space'
    SNAKE_CASE: str = 'convert_to_snake_case'
    STRAIGHT_QUOTES: str = 'convert “curly quotes” to "straight quotes"'
    STRIKETHROUGH: str = 's̶t̶r̶i̶k̶e̶ ̶t̶h̶r̶o̶u̶g̶h̶ ̶t̶e̶x̶t̶'
    STRIP: str = 'remove leading and trailing whitespace'
    TITLE_CASE: str = 'Convert to Title Case'
    UPPERCASE: str = 'CONVERT TO UPPERCASE'

# Prompt for the user to enter any other text.
ANY_OTHER_TEXT_PROMPT: str = 'Any other text? (y/n) (Copy text to clipboard):'

# Prompt for when the previous response was invalid.
ENTER_VALID_RESPONSE_PROMPT: str = 'Please enter a valid response.'

# Inputs for exiting the program.
EXIT_INPUTS: str = {'quit', 'q', 'exit', 'e'}

# Message for when the user exits the program.
EXIT_MESSAGE: str = 'Exiting the program...'

# Message for when the program copies modified text to the clipboard.
MODIFIED_TEXT_COPIED: str = 'Modified text copied to clipboard.'

# Inputs for indicating a negative response.
NO_INPUTS: str = {'no', 'n'}

# Inputs for indicating an affirmative response.
YES_INPUTS: str = {'yes', 'y'}
