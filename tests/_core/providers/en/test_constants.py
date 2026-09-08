"""Tests for English-specific NLP constants."""

from textwarp._core.enums import POSTag
from textwarp._core.providers.en.constants import (
    BASE_VERB_TAGS,
    HAVE_AUXILIARIES,
    NOUN_PHRASE_TAGS,
    NOUN_TAGS,
    PARTICIPLE_TAGS,
    POS_TAGS,
    POS_WORD_TAGS,
    SINGULAR_NOUN_TAGS,
    THIRD_PERSON_SINGULAR_PRONOUNS,
    TITLE_CASE_TAG_EXCEPTIONS,
    WH_WORDS
)


def test_en_constants_are_frozensets():
    assert isinstance(BASE_VERB_TAGS, frozenset)
    assert isinstance(HAVE_AUXILIARIES, frozenset)
    assert isinstance(NOUN_PHRASE_TAGS, frozenset)
    assert isinstance(PARTICIPLE_TAGS, frozenset)
    assert isinstance(SINGULAR_NOUN_TAGS, frozenset)
    assert isinstance(THIRD_PERSON_SINGULAR_PRONOUNS, frozenset)
    assert isinstance(TITLE_CASE_TAG_EXCEPTIONS, frozenset)
    assert isinstance(WH_WORDS, frozenset)


def test_have_auxiliaries():
    assert 'have' in HAVE_AUXILIARIES
    assert 'has' in HAVE_AUXILIARIES
    assert "'ve" in HAVE_AUXILIARIES


def test_nlp_tag_sets_are_frozensets():
    assert isinstance(NOUN_TAGS, frozenset)


def test_noun_tags():
    assert POSTag.NOUN in NOUN_TAGS
    assert POSTag.PROPN in NOUN_TAGS
    assert POSTag.VERB not in NOUN_TAGS


def test_pos_tags_structure():
    assert isinstance(POS_TAGS, tuple)
    assert len(POS_TAGS) > 0

    for tag_pair in POS_TAGS:
        assert isinstance(tag_pair, tuple)
        assert len(tag_pair) == 2
        assert isinstance(tag_pair[0], POSTag)
        assert isinstance(tag_pair[1], str)


def test_pos_word_tags():
    """
    Verify that the `POS_WORD_TAGS` `frozenset` strips out the 'X'
    (other) tag.
    """
    assert isinstance(POS_WORD_TAGS, frozenset)
    assert POSTag.NOUN in POS_WORD_TAGS
    assert POSTag.VERB in POS_WORD_TAGS
    assert POSTag.X not in POS_WORD_TAGS


def test_third_person_singular_pronouns():
    assert 'he' in THIRD_PERSON_SINGULAR_PRONOUNS
    assert 'she' in THIRD_PERSON_SINGULAR_PRONOUNS
    assert 'nobody' in THIRD_PERSON_SINGULAR_PRONOUNS
    assert 'we' not in THIRD_PERSON_SINGULAR_PRONOUNS


def test_wh_words():
    assert 'how' in WH_WORDS
    assert 'what' in WH_WORDS
    assert 'when' in WH_WORDS
    assert 'where' in WH_WORDS
    assert 'which' in WH_WORDS
    assert 'who' in WH_WORDS
    assert 'why' in WH_WORDS
