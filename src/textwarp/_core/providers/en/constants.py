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

BASE_VERB_TAGS: frozenset[str]

CURLY_TO_STRAIGHT_TABLE: Final[dict[int, str]] = str.maketrans({
    '‘': "'",
    '’': "'",
    '“': '"',
    '”': '"'
})

HAVE_AUXILIARIES: frozenset[str]
LEFT_SEARCH_STOP_TAGS: frozenset[str]
NOUN_PHRASE_TAGS: frozenset[str]
OPEN_QUOTES: frozenset[str]

ORDINAL_SUFFIX_MAP: Final[dict[int, str]] = {
    1: 'st',
    2: 'nd',
    3: 'rd'
}

ORDINAL_SUFFIXES: Final[tuple[str, ...]] = (
    'nd', 'nds',
    'rd', 'rds',
    'st', 'sts',
    'th', 'ths',
)

PARTICIPLE_TAGS: frozenset[str]

PREFERENCE_VERBS: Final[frozenset[str]] = frozenset(
    {'care', 'mind', 'prefer'}
)

PARTICIPLE_SUFFIXES: tuple = ("in'", 'in’')
PROPER_NOUN_ENTITIES: frozenset[str]
QUOTATION_MARKS: frozenset[str] = frozenset({'"', "'"})
RIGHT_SEARCH_STOP_TAGS: frozenset[str]
SINGULAR_NOUN_TAGS: frozenset[str]
SUBJECT_POS_TAGS: frozenset[str]
THIRD_PERSON_SINGULAR_PRONOUNS: frozenset[str]
TITLE_CASE_TAG_EXCEPTIONS: frozenset[str]
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
