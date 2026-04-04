"""English-specific NLP constants."""

from typing import Final, cast
from textwarp._core.providers.en.data import load_data

__all__ = [
    'BASE_VERB_TAGS',
    'HAVE_AUXILIARIES',
    'LEFT_SEARCH_STOP_TAGS',
    'NOUN_PHRASE_TAGS',
    'OPEN_QUOTES',
    'PARTICIPLE_TAGS',
    'PROPER_NOUN_ENTITIES',
    'RIGHT_SEARCH_STOP_TAGS',
    'SINGULAR_NOUN_TAGS',
    'SUBJECT_POS_TAGS',
    'THIRD_PERSON_SINGULAR_PRONOUNS',
    'TITLE_CASE_TAG_EXCEPTIONS',
    'WH_WORDS'
]

# Fine-grained parts-of-speech tags for base verb forms.
BASE_VERB_TAGS: Final[frozenset[str]] = frozenset(
    cast(list[str], load_data('nlp_constants/base_verb_tags.json'))
)

# Auxiliary verbs forms of "have".
HAVE_AUXILIARIES: Final[frozenset[str]] = frozenset(
    cast(list[str], load_data('nlp_constants/have_auxiliaries.json'))
)

# Coarse-grained parts-of-speech tags for stopping a subject search when
# looking left.
LEFT_SEARCH_STOP_TAGS: Final[frozenset[str]] = frozenset(
    cast(list[str], load_data('nlp_constants/left_search_stop_tags.json'))
)

# Fine-grained parts-of-speech tags for the first word of a noun phrase.
NOUN_PHRASE_TAGS: Final[frozenset[str]] = frozenset(
    cast(list[str], load_data('nlp_constants/noun_phrase_tags.json'))
)

# Opening quote characters.
OPEN_QUOTES: Final[frozenset[str]] = frozenset(
    cast(list[str], load_data('nlp_constants/open_quotes.json'))
)

# Fine-grained parts-of-speech tags for past tense and past participle
# verb forms. (Fine-grained tags used to distinguish verb tense.)
PARTICIPLE_TAGS: Final[frozenset[str]] = frozenset(
    cast(list[str], load_data('nlp_constants/participle_tags.json'))
)

# Named entities that are typically proper nouns.
PROPER_NOUN_ENTITIES: Final[frozenset[str]] = frozenset(
    cast(list[str], load_data('nlp_constants/proper_noun_entities.json'))
)

# Coarse-grained parts-of-speech tags for stopping a subject search when
# looking right.
RIGHT_SEARCH_STOP_TAGS: Final[frozenset[str]] = frozenset(
    cast(list[str], load_data('nlp_constants/right_search_stop_tags.json'))
)

# Fine-grained parts-of-speech tags for singular nouns and proper nouns.
SINGULAR_NOUN_TAGS: Final[frozenset[str]] = frozenset(
    cast(list[str], load_data('nlp_constants/singular_noun_tags.json'))
)

# Coarse-grained parts-of-speech tags for pronouns, proper nouns, and
# nouns.
SUBJECT_POS_TAGS: Final[frozenset[str]] = frozenset(
    cast(list[str], load_data('nlp_constants/subject_pos_tags.json'))
)

# Third-person singular pronouns for subject-verb agreement checks.
THIRD_PERSON_SINGULAR_PRONOUNS: Final[frozenset[str]] = frozenset(
    cast(list[str], load_data('nlp_constants/third_person_singular_pronouns.json'))
)

# Fine-grained parts-of-speech tag exceptions for title case
# capitalization. (Fine-grained tags used to distinguish articles from
# possessives.)
TITLE_CASE_TAG_EXCEPTIONS: Final[frozenset[str]] = frozenset(
    cast(list[str], load_data('nlp_constants/title_case_tag_exceptions.json'))
)

# Wh-words that start questions.
WH_WORDS: Final[frozenset[str]] = frozenset(
    cast(list[str], load_data('nlp_constants/wh_words.json'))
)
