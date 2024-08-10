class HelpMessages:
    """
    Help message strings for command-line arguments.

    Attributes:
        DESCRIPTION (STR): Description for textwarp arguments

        ALTERNATING_CAPS (STR): Help message for --alternating-caps 
            argument
        CAMEL_CASE (STR): Help message for --camel-case argument
        CAPITALIZE (STR): Help message for --capitalize argument
        CARDINALS (STR): Help message for --cardinals argument
        CURLY_QUOTES (STR): Help message for --curly argument
        HYPHENS_TO_EM (STR): Help message for --hyphens-to-em argument
        HYPHENS_TO_EN (STR): Help message for --hyphens-to-en argument
        KEBAB_CASE (STR): Help message for --kebab-case argument
        LOWERCASE (STR): Help message for --lowercase argument
        ORDINALS (STR): Help message for --ordinals argument
        PASCAL_CASE (STR): Help message for --pascal-case argument
        PUNCT_TO_INSIDE (STR): Help message for --punct-to-inside 
            argument
        PUNCT_TO_OUTSIDE (STR): Help message for --punct-to-outside 
            argument
        SNAKE_CASE (STR): Help message for --snake-case argument
        STRAIGHT_QUOTES (STR): Help message for --straight argument
        TITLE_CASE (STR): Help message for --title-case argument
        UPPERCASE (STR): Help message for --uppercase argument
    """
    DESCRIPTION = ('Specify the text warping function to apply to the '
                   'clipboard.')

    ALTERNATING_CAPS = 'convert to alternating caps'
    CAMEL_CASE = 'convert to camel case'
    CAPITALIZE = 'capitalize the first character of each word'
    CARDINALS = 'convert ordinal numbers to cardinal numbers'
    CURLY_QUOTES = 'convert straight quotes to curly quotes'
    HYPHENS_TO_EM = 'convert consecutive hyphens to em dashes'
    HYPHEN_TO_EN = 'convert hyphens to en dashes'
    KEBAB_CASE = 'convert to kebab case'
    LOWERCASE = 'convert to lowercase'
    ORDINALS = 'convert cardinal numbers to ordinal numbers'
    PASCAL_CASE = 'convert to Pascal case'
    PUNCT_TO_INSIDE = 'move punctuation inside quotation marks'
    PUNCT_TO_OUTSIDE = 'move punctuation outside quotation marks'
    SNAKE_CASE = 'convert to snake case'
    STRAIGHT_QUOTES = 'convert curly quotes to straight quotes'
    TITLE_CASE = 'convert to title case'
    UPPERCASE = 'convert to uppercase'

# String printed to prompt the user for any other text
ANY_OTHER_TEXT_STR = 'Any other text? (y/n) (Copy text to clipboard):'

# String printed when the previous response was invalid
ENTER_VALID_RESPONSE_STR = 'Please enter a valid response.'

# String printed when the user exits the program
EXIT_STR = 'Exiting the program...'

# String printed when the program copies modified text to the clipboard
MODIFED_TEXT_STR = 'Modified text copied to clipboard.'

# Set of strings for indicating a negative response
NO_STRS = {'no', 'n'}

# Set of strings for exiting the program
QUIT_STRS = {'quit', 'q', 'exit', 'e'}

# Set of strings for indicating an affirmative response
YES_STRS = {'yes', 'y'}
