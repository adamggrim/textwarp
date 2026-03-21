"""Tests for NLP tag collections and constants."""

from textwarp._core.constants.nlp import (
    LEFT_SEARCH_STOP_TAGS,
    NOUN_TAGS,
    POS_TAGS,
    POS_WORD_TAGS,
    PROPER_NOUN_ENTITIES,
    RIGHT_SEARCH_STOP_TAGS,
    SUBJECT_POS_TAGS
)


def test_nlp_tag_sets_are_frozensets():
    """
    Verify that the tag collections are immutable `frozenset` objects.
    """
    assert isinstance(LEFT_SEARCH_STOP_TAGS, frozenset)
    assert isinstance(NOUN_TAGS, frozenset)
    assert isinstance(PROPER_NOUN_ENTITIES, frozenset)
    assert isinstance(RIGHT_SEARCH_STOP_TAGS, frozenset)
    assert isinstance(SUBJECT_POS_TAGS, frozenset)


def test_noun_tags():
    """`Verify the `NOUN_TAGS` set."""
    assert 'NOUN' in NOUN_TAGS
    assert 'PROPN' in NOUN_TAGS
    assert 'VERB' not in NOUN_TAGS


def test_proper_noun_entities():
    """Verify the `PROPER_NOUN_ENTITIES` set."""
    assert 'PERSON' in PROPER_NOUN_ENTITIES
    assert 'ORG' in PROPER_NOUN_ENTITIES
    assert 'WORK_OF_ART' in PROPER_NOUN_ENTITIES


def test_pos_tags_structure():
    """Verify the structure of the `POS_TAGS` tuple."""
    assert isinstance(POS_TAGS, tuple)
    assert len(POS_TAGS) > 0

    for tag_pair in POS_TAGS:
        assert isinstance(tag_pair, tuple)
        assert len(tag_pair) == 2
        assert isinstance(tag_pair[0], str)
        assert isinstance(tag_pair[1], str)


def test_pos_word_tags():
    """Verify that `POS_WORD_TAGS` strips out the 'X' (Other) tag."""
    assert isinstance(POS_WORD_TAGS, tuple)
    assert 'NOUN' in POS_WORD_TAGS
    assert 'VERB' in POS_WORD_TAGS
    assert 'X' not in POS_WORD_TAGS


def test_subject_pos_tags():
    """Verify tags that represent subjects in dependency parsing."""
    assert 'PRON' in SUBJECT_POS_TAGS
    assert 'PROPN' in SUBJECT_POS_TAGS
    assert 'NOUN' in SUBJECT_POS_TAGS
