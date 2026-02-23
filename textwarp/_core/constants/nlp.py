"""Objects used across the package for spaCy processing."""

from typing import Final

__all__ = [
    'HAVE_AUXILIARIES',
    'MODEL_RANKING_BY_SPEED',
    'NOUN_PHRASE_TAGS',
    'NOUN_TAGS',
    'PARTICIPLE_TAGS',
    'POS_TAGS',
    'POS_WORD_TAGS',
    'PREFERENCE_VERBS',
    'PROPER_NOUN_ENTITIES',
    'SUBJECT_POS_TAGS',
    'THIRD_PERSON_SINGULAR_PRONOUNS',
    'TITLE_CASE_TAG_EXCEPTIONS',
    'WH_WORDS'
]

# Auxiliary verbs forms of "have".
HAVE_AUXILIARIES: Final[set[str]] = {'have', 'has', 'had', "'ve", "'d"}

# Ranking of spaCy models by speed.
MODEL_RANKING_BY_SPEED: Final[list[str]] = [
    'en_core_web_sm',
    'en_core_web_md',
    'en_core_web_lg',
    'en_core_web_trf'
]

# Fine-grained part-of-speech tags for the first word of a noun phrase.
NOUN_PHRASE_TAGS: Final[set[str]] = {
    'JJ', 'JJR', 'JJS',      # Adjectives
    'DT', 'PDT', 'WDT',      # Determiners
    'PRP', 'PRP$', 'WP',     # Pronouns
    'NN', 'NNS',             # Common nouns
    'NNP', 'NNPS'            # Proper nouns
}

# Coarse-grained part-of-speech tags for singular and proper nouns.
NOUN_TAGS: Final[set[str]] = {'NOUN', 'PROPN'}

# Fine-grained part-of-speech tags for past tense and past participle 
# verb forms. (Fine-grained tags used to distinguish verb tense.)
PARTICIPLE_TAGS: Final[set[str]] = {'VBN', 'VBD'}

# Tuple of tuples for all part-of-speech tags and their names.
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

# Tuple of strings for all coarse-grained part-of-speech tags
# representing words.
POS_WORD_TAGS: Final[tuple[str, ...]] = tuple(
    item[0] for item in POS_TAGS if item[0] != 'X'
)

# Strings for verbs that expand to "would".
PREFERENCE_VERBS: Final[set[str]] = {'care', 'mind', 'prefer'}

# Named entities that are typically proper nouns.
PROPER_NOUN_ENTITIES: Final = {
    'EVENT',
    'FAC',
    'GPE',
    'LANGUAGE',
    'LAW',
    'LOC',
    'NORP',
    'ORG',
    'PERSON',
    'PRODUCT',
    'WORK_OF_ART'
}

# Fine-grained part-of-speech tags for singular nouns and proper nouns.
SINGULAR_NOUN_TAGS: Final[set[str]] = {'NN', 'NNP'}

# Coarse-grained part-of-speech tags for pronouns, proper nouns, and
# nouns.
SUBJECT_POS_TAGS: Final[set[str]] = {'PRON', 'PROPN', 'NOUN'}

# Third-person singular pronouns for subject-verb agreement checks.
THIRD_PERSON_SINGULAR_PRONOUNS: Final[set[str]] = {'he', 'she', 'it'}

# Fine-grained part-of-speech tag exceptions for title case
# capitalization. (Fine-grained tags used to distinguish articles
# from possessives.)
TITLE_CASE_TAG_EXCEPTIONS: Final = {
    'CC',   # Coordinating conjunction (e.g., 'and', 'but')
    'DT',   # Determiner (e.g., 'a', 'an', 'the')
    'IN',   # Preposition or subordinating conjunction
            # (e.g., 'in', 'of', 'on')
    'RP',   # Particle (e.g., 'in' in 'give in')
    'TO',   # to (infinitive marker)
    'WDT',  # Wh-determiner (e.g., 'what')
}

# Wh-words that start questions.
WH_WORDS: Final[set[str]] = {'how', 'what', 'when', 'where', 'who', 'why'}
