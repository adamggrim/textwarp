from typing import Tuple


class FormatCountLabels:
    """
    Label strings for count formatting.

    Attributes:
        CHAR: String specifying character count
        LINE: String specifying line count
        WORD: String specifying word count
    """
    CHAR: str = 'Character'
    LINE: str = 'Line'
    WORD: str = 'Word'


class HelpMessages:
    """
    Help message strings for command-line arguments.

    Attributes:
        DESCRIPTION: Description for textwarp arguments

        CHAR_COUNT: Help message for --char-count argument
        LINE_COUNT: Help message for --line-count argument
        MFWS: Help message for --mfws argument
        POS_COUNT: Help message for --pos-count argument
        TIME_TO_READ: Help message for --time-to-read argument
        WORD_COUNT: Help message for --word-count argument
    """
    DESCRIPTION: str = ('Specify the text analysis function to apply to the '
                   'clipboard.')

    CHAR_COUNT: str = 'count characters'
    LINE_COUNT: str = 'count lines'
    MFWS: str = 'get most frequent words'
    POS_COUNT: str = 'count parts of speech'
    TIME_TO_READ: str = 'calculate time to read'
    WORD_COUNT: str = 'count words'

# String printed to prompt the user for any other text
ANY_OTHER_TEXT_PROMPT: str = 'Any other text? (y/n) (Copy text to clipboard):'

# String printed to prompt the user for the number of most frequent words
ENTER_MFW_COUNT_PROMPT: str = 'How many most frequent words?'

# String printed when the user does not enter a number
ENTER_NUMBER_PROMPT: str = 'Please enter a number.'

# String printed when the previous response was invalid
ENTER_VALID_RESPONSE_PROMPT: str = 'Please enter a valid response.'

# String printed to prompt the user for words per minute
ENTER_WPM_PROMPT: str = 'How many words per minute?'

# Set of strings for exiting the program
EXIT_INPUTS: set[str] = {'quit', 'q', 'exit', 'e'}

# String printed when the user exits the program
EXIT_MESSAGE: str = 'Exiting the program...'

# Set of strings for indicating a negative response
NO_INPUTS: set[str] = {'no', 'n'}

# Tuple of tuples for parts of speech tags and their names
POS_TAGS: Tuple[Tuple[str, str], ...] = (
    ('ADJ', 'Adjectives'), 
    ('ADP', 'Adpositions'), 
    ('ADV', 'Adverbs'), 
    ('CONJ', 'Conjunctions'), 
    ('DET', 'Determiners'), 
    ('NOUN', 'Nouns'), 
    ('NUM', 'Numbers'), 
    ('PRT', 'Particles'), 
    ('PRON', 'Pronouns'), 
    ('VERB', 'Verbs'), 
    ('X', 'Other')
)

# Integer representing the length of the longest tag name in POS_TAGS
MAX_POS_LENGTH: int = max(len(tag_pair[1]) for tag_pair in POS_TAGS)

# Tuple of strings for POS tags representing words
POS_WORD_TAGS: Tuple[str, ...] = (
    'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRT', 'PRON', 'VERB'
)

# Set of strings for indicating an affirmative response
YES_INPUTS: set[str] = {'yes', 'y'}
