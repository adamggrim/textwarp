"""English-specific NLP constants."""

from typing import Final
from textwarp._core.utils import load_json_data

__all__ = [
    'BASE_VERB_TAGS',
    'HAVE_AUXILIARIES',
    'LEFT_SEARCH_STOP_TAGS',
    'NOUN_PHRASE_TAGS',
    'OPEN_QUOTES',
    'ORDINAL_SUFFIX_MAP',
    'ORDINAL_SUFFIXES',
    'PARTICIPLE_TAGS',
    'PREFERENCE_VERBS',
    'PROPER_NOUN_ENTITIES',
    'RIGHT_SEARCH_STOP_TAGS',
    'SINGULAR_NOUN_TAGS',
    'SUBJECT_POS_TAGS',
    'THIRD_PERSON_SINGULAR_PRONOUNS',
    'TITLE_CASE_TAG_EXCEPTIONS',
    'WH_WORDS'
]

# Fine-grained parts-of-speech tags for base verb forms.
BASE_VERB_TAGS: frozenset[str]

# Auxiliary verbs forms of "have".
HAVE_AUXILIARIES: frozenset[str]

# Coarse-grained parts-of-speech tags for stopping a subject search when
# looking left.
LEFT_SEARCH_STOP_TAGS: frozenset[str]

# Fine-grained parts-of-speech tags for the first word of a noun phrase.
NOUN_PHRASE_TAGS: frozenset[str]

# Opening quote characters.
OPEN_QUOTES: frozenset[str]

# A mapping of integers to their corresponding ordinal suffix.
ORDINAL_SUFFIX_MAP: Final[dict[int, str]] = {
    1: 'st',
    2: 'nd',
    3: 'rd'
}

# Strings for ordinal suffixes.
ORDINAL_SUFFIXES: Final[tuple[str, ...]] = (
    'nd', 'nds',
    'rd', 'rds',
    'st', 'sts',
    'th', 'ths',
)

# Fine-grained parts-of-speech tags for past tense and past participle
# verb forms. (Fine-grained tags used to distinguish verb tense.)
PARTICIPLE_TAGS: frozenset[str]

# Strings for verbs that expand to "would".
PREFERENCE_VERBS: Final[frozenset[str]] = frozenset(
    {'care', 'mind', 'prefer'}
)

# Named entities that are typically proper nouns.
PROPER_NOUN_ENTITIES: frozenset[str]

# Coarse-grained parts-of-speech tags for stopping a subject search when
# looking right.
RIGHT_SEARCH_STOP_TAGS: frozenset[str]

# Fine-grained parts-of-speech tags for singular nouns and proper nouns.
SINGULAR_NOUN_TAGS: frozenset[str]

# Coarse-grained parts-of-speech tags for pronouns, proper nouns and
# nouns.
SUBJECT_POS_TAGS: frozenset[str]

# Third-person singular pronouns for subject-verb agreement checks.
THIRD_PERSON_SINGULAR_PRONOUNS: frozenset[str]

# Fine-grained parts-of-speech tag exceptions for title case
# capitalization. (Fine-grained tags used to distinguish articles from
# possessives.)
TITLE_CASE_TAG_EXCEPTIONS: frozenset[str]

# Wh-words that start questions.
WH_WORDS: frozenset[str]


def __getattr__(name: str) -> frozenset[str]:
    """Lazily load JSON data for constants when accessed."""

    _file_map = {
        'BASE_VERB_TAGS': 'nlp_constants/base_verb_tags.json',
        'HAVE_AUXILIARIES': 'nlp_constants/have_auxiliaries.json',
        'LEFT_SEARCH_STOP_TAGS': 'nlp_constants/left_search_stop_tags.json',
        'NOUN_PHRASE_TAGS': 'nlp_constants/noun_phrase_tags.json',
        'OPEN_QUOTES': 'nlp_constants/open_quotes.json',
        'PARTICIPLE_TAGS': 'nlp_constants/participle_tags.json',
        'PROPER_NOUN_ENTITIES': 'nlp_constants/proper_noun_entities.json',
        'RIGHT_SEARCH_STOP_TAGS': 'nlp_constants/right_search_stop_tags.json',
        'SINGULAR_NOUN_TAGS': 'nlp_constants/singular_noun_tags.json',
        'SUBJECT_POS_TAGS': 'nlp_constants/subject_pos_tags.json',
        'THIRD_PERSON_SINGULAR_PRONOUNS': (
            'nlp_constants/third_person_singular_pronouns.json'
        ),
        'TITLE_CASE_TAG_EXCEPTIONS': (
            'nlp_constants/title_case_tag_exceptions.json'
        ),
        'WH_WORDS': 'nlp_constants/wh_words.json'
    }

    if name in _file_map:
        return frozenset(load_json_data(_file_map[name], locale='en'))

    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
