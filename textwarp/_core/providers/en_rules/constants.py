"""English-specific NLP constants."""

from typing import Final

__all__ = [
    'BASE_VERB_TAGS',
    'HAVE_AUXILIARIES',
    'NOUN_PHRASE_TAGS',
    'PARTICIPLE_TAGS',
    'SINGULAR_NOUN_TAGS',
    'THIRD_PERSON_SINGULAR_PRONOUNS',
    'TITLE_CASE_TAG_EXCEPTIONS',
    'WH_WORDS'
]

# Fine-grained parts-of-speech tags for base verb forms.
BASE_VERB_TAGS: Final[frozenset[str]] = frozenset({'VB', 'VBP'})

# Auxiliary verbs forms of "have".
HAVE_AUXILIARIES: Final[frozenset[str]] = frozenset({
    'have', 'has', 'had', "'ve", "'d"
})

# Fine-grained parts-of-speech tags for the first word of a noun phrase.
NOUN_PHRASE_TAGS: Final[frozenset[str]] = frozenset({
    'JJ', 'JJR', 'JJS',      # Adjectives
    'DT', 'PDT', 'WDT',      # Determiners
    'PRP', 'PRP$', 'WP',     # Pronouns
    'NN', 'NNS',             # Common nouns
    'NNP', 'NNPS'            # Proper nouns
})

# Fine-grained parts-of-speech tags for past tense and past participle
# verb forms. (Fine-grained tags used to distinguish verb tense.)
PARTICIPLE_TAGS: Final[frozenset[str]] = frozenset({'VBN', 'VBD'})

# Fine-grained parts-of-speech tags for singular nouns and proper nouns.
SINGULAR_NOUN_TAGS: Final[frozenset[str]] = frozenset({'NN', 'NNP'})

# Third-person singular pronouns for subject-verb agreement checks.
THIRD_PERSON_SINGULAR_PRONOUNS: Final[frozenset[str]] = frozenset({
    'he', 'she', 'it', 'nobody', 'everyone', 'someone', 'anyone', 'no one',
    'everybody', 'somebody', 'anybody'
})

# Fine-grained parts-of-speech tag exceptions for title case
# capitalization. (Fine-grained tags used to distinguish articles from
# possessives.)
TITLE_CASE_TAG_EXCEPTIONS: Final[frozenset[str]] = frozenset({
    'CC',   # Coordinating conjunction (e.g., 'and', 'but')
    'DT',   # Determiner (e.g., 'a', 'an', 'the')
    'IN',   # Preposition or subordinating conjunction
            # (e.g., 'in', 'of', 'on')
    'RP',   # Particle (e.g., 'in' in 'give in')
    'TO',   # to (infinitive marker)
    'WDT',  # Wh-determiner (e.g., 'what')
})

# Wh-words that start questions.
WH_WORDS: Final[frozenset[str]] = frozenset({
    'how', 'what', 'when', 'where', 'which', 'who', 'why'
})
