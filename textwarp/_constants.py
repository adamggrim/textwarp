from typing import Final

# Variants of 's for contractions.
AINT_SUFFIX_VARIANTS: Final[set[str]] = {"n't", 'n’t', 'n‘t'}

# Prompt for the user to enter any other text.
ANY_OTHER_TEXT_PROMPT: Final[str] = (
    'Any other text? (y/n) (Copy text to clipboard):'
)

# Variants of 'd for contractions.
APOSTROPHE_D_VARIANTS: Final[set[str]] = {"'d", '’d', '‘d'}

# Variants of 's for contractions.
APOSTROPHE_S_VARIANTS: Final[set[str]] = {"'s", '’s', '‘s'}

# Variants of apostrophes.
APOSTROPHE_VARIANTS: Final[set[str]] = {"'", '’', '‘'}

# Message for any error accessing the clipboard.
CLIPBOARD_ACCESS_ERROR_MESSAGE: Final[str] = 'Error accessing clipboard: '

# Message for when the clipboard is cleared.
CLIPBOARD_CLEARED_MESSAGE: Final[str] = 'Clipboard text cleared.'

# Prompt for the user to enter the number of most frequent words.
ENTER_MFW_COUNT_PROMPT: str = 'How many most frequent words?'

# Prompt for when the previous response was not a number.
ENTER_NUMBER_PROMPT: str = 'Please enter a number.'

# Prompt for when the previous response was invalid.
ENTER_VALID_RESPONSE_PROMPT: Final[str] = 'Please enter a valid response (y/n).'

# Prompt for the user to enter the words per minute.
ENTER_WPM_PROMPT: str = 'How many words per minute?'

# Inputs for exiting the program.
EXIT_INPUTS: Final[set[str]] = {'quit', 'q', 'exit', 'e'}

# Message for when the user exits the program.
EXIT_MESSAGE: Final[str] = 'Exiting the program...'

# Help description for command-line arguments.
HELP_DESCRIPTION: Final[str] = (
    'Specify which text warping function to apply to the clipboard.'
)

# Message for when the program copies modified text to the clipboard.
MODIFIED_TEXT_COPIED: Final[str] = 'Modified text copied to clipboard.'

# Inputs for indicating a negative response.
NO_INPUTS: Final[set[str]] = {'no', 'n'}

# Opening quote characters.
OPEN_QUOTES: Final[set[str]] = {'"', '“', "'", '‘'}

# Part-of-speech tags for past participles.
PAST_PARTICIPLE_TAGS: Final[set[str]] = {'VBN', 'VBD'}

# Tuple of tuples for parts of speech tags and their names.
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

# Tuple of strings for POS tags representing words.
POS_WORD_TAGS: Final[tuple[str, ...]] = tuple(
    item[0] for item in POS_TAGS if item[0] != 'X'
)

# Named entities that are typically proper nouns.
PROPER_NOUN_ENTITIES: Final[set[str]] = {
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

# Message for when a replacement is not found in the text.
REPLACEMENT_NOT_FOUND_MESSAGE: Final[str] = 'Replacement not found.'

# Part-of-speech tag exceptions for title case capitalization.
TITLE_CASE_TAG_EXCEPTIONS: Final[set[str]] = {
    'CC',   # Coordinating conjunction (e.g., 'and', 'but')
    'DT',   # Determiner (e.g., 'a', 'an', 'the')
    'IN',   # Preposition or subordinating conjunction
            # (e.g., 'in', 'of', 'on')
    'RP',   # Particle (e.g., 'in' in 'give in')
    'TO',   # to (infinitive marker)
    'WDT',  # Wh-determiner (e.g., 'what')
}

# Inputs for indicating an affirmative response.
YES_INPUTS: Final[set[str]] = {'yes', 'y'}
