"""Objects used across the package for spaCy processing."""

from typing import Final

__all__ = [
    'MODEL_RANKING_BY_SPEED',
    'POS_TAGS',
    'POS_WORD_TAGS',
    'PROPER_NOUN_ENTITIES',
    'TITLE_CASE_TAG_EXCEPTIONS'
]

# Ranking for spaCy models by speed.
MODEL_RANKING_BY_SPEED: Final[list[str]] = [
    'en_core_web_sm',
    'en_core_web_md',
    'en_core_web_lg',
    'en_core_web_trf'
]

# spaCy tags for singular and proper nouns.
NOUN_TAGS: Final[set[str]] = {'NN', 'NNP'}

# spaCy tags for past and past participle verb forms.
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

# Tuple of strings for all part-of-speech tags representing words.
POS_WORD_TAGS: Final[tuple[str, ...]] = tuple(
    item[0] for item in POS_TAGS if item[0] != 'X'
)

# Strings for adverbs modifying verbs that expand to "would".
PREFERENCE_ADVERBS: Final[set[str]] = {'rather', 'sooner'}

# Strings for verbs that expand to "would".
PREFERENCE_VERBS: Final[set[str]] = {'care', 'mind', 'prefer'}

# Named entities that are typically proper nouns.
PROPER_NOUN_ENTITIES: Final = {
    'PERSON',
    'GPE',
    'ORG',
    'NORP',
    'FAC',
    'LOC',
    'PRODUCT',
    'EVENT',
    'WORK_OF_ART',
    'LANGUAGE',
    'LAW'
}

# Singular pronouns for subject-verb agreement checks.
SINGULAR_PRONOUNS: Final[set[str]] = {'he', 'she', 'it'}

# spaCy tags for pronouns, proper nouns, and nouns.
SUBJECT_POS_TAGS: Final[set[str]] = {'PRON', 'PROPN', 'NOUN'}

# Part-of-speech tag exceptions for title case capitalization.
TITLE_CASE_TAG_EXCEPTIONS: Final = {
    'CC',   # Coordinating conjunction (e.g., 'and', 'but')
    'DT',   # Determiner (e.g., 'a', 'an', 'the')
    'IN',   # Preposition or subordinating conjunction
            # (e.g., 'in', 'of', 'on')
    'RP',   # Particle (e.g., 'in' in 'give in')
    'TO',   # to (infinitive marker)
    'WDT',  # Wh-determiner (e.g., 'what')
}
