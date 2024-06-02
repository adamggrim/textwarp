class HelpMessages:
    """
    Help message strings for command-line arguments.

    Attributes:
        DESCRIPTION (STR): Description for textwarp arguments

        CHAR_COUNT (STR): Help message for --char-count argument
        MFWS (STR): Help message for --mfws argument
        POS_COUNT (STR): Help message for --pos-count argument
        TIME_TO_READ (STR): Help message for --time-to-read argument
    """
    DESCRIPTION = ('Specify the text analysis function to apply to the '
                   'clipboard.')

    CHAR_COUNT = 'count characters'
    MFWS = 'get most frequent words'
    POS_COUNT = 'count parts of speech'
    TIME_TO_READ = 'calculate time to read'

# String printed to prompt the user for any other text
ANY_OTHER_TEXT_STR = 'Any other text? (y/n) (Copy text to clipboard):'

# String printed when the previous response was invalid
ENTER_VALID_RESPONSE_STR = 'Please enter a valid response.'

# String printed when the user exits the program
EXIT_STR = 'Exiting the program...'

# Set of strings for indicating a negative response
NO_STRS = {'no', 'n'}

# Set of strings for exiting the program
QUIT_STRS = {'quit', 'q', 'exit', 'e'}

# Set of strings for indicating an affirmative response
YES_STRS = {'yes', 'y'}