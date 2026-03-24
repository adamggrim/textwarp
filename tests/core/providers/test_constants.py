"""Tests for English-specific NLP constants."""

from textwarp._core.providers.en_rules.constants import (
    BASE_VERB_TAGS,
    HAVE_AUXILIARIES,
    NOUN_PHRASE_TAGS,
    PARTICIPLE_TAGS,
    SINGULAR_NOUN_TAGS,
    THIRD_PERSON_SINGULAR_PRONOUNS,
    TITLE_CASE_TAG_EXCEPTIONS,
    WH_WORDS
)


def test_en_constants_are_frozensets():
    """Verify that all English constant collections are immutable."""
    assert isinstance(BASE_VERB_TAGS, frozenset)
    assert isinstance(HAVE_AUXILIARIES, frozenset)
    assert isinstance(NOUN_PHRASE_TAGS, frozenset)
    assert isinstance(PARTICIPLE_TAGS, frozenset)
    assert isinstance(SINGULAR_NOUN_TAGS, frozenset)
    assert isinstance(THIRD_PERSON_SINGULAR_PRONOUNS, frozenset)
    assert isinstance(TITLE_CASE_TAG_EXCEPTIONS, frozenset)
    assert isinstance(WH_WORDS, frozenset)


def test_have_auxiliaries():
    """Verify auxiliary verb forms of 'have'."""
    assert 'have' in HAVE_AUXILIARIES
    assert 'has' in HAVE_AUXILIARIES
    assert "'ve" in HAVE_AUXILIARIES


def test_third_person_singular_pronouns():
    """Verify pronouns used for subject-verb agreement."""
    assert 'he' in THIRD_PERSON_SINGULAR_PRONOUNS
    assert 'she' in THIRD_PERSON_SINGULAR_PRONOUNS
    assert 'nobody' in THIRD_PERSON_SINGULAR_PRONOUNS
    assert 'we' not in THIRD_PERSON_SINGULAR_PRONOUNS


def test_wh_words():
    """Verify interrogative wh-words."""
    assert 'how' in WH_WORDS
    assert 'what' in WH_WORDS
    assert 'when' in WH_WORDS
    assert 'where' in WH_WORDS
    assert 'which' in WH_WORDS
    assert 'who' in WH_WORDS
    assert 'why' in WH_WORDS
