"""Tests for NLP tag collections and constants."""

from textwarp._core.constants.nlp import (
    NOUN_TAGS,
    POS_TAGS,
    POS_WORD_TAGS
)


def test_nlp_tag_sets_are_frozensets():
    """
    Verify that the tag collections are immutable `frozenset` objects.
    """
    assert isinstance(NOUN_TAGS, frozenset)


def test_noun_tags():
    """`Verify the `NOUN_TAGS` set."""
    assert 'NOUN' in NOUN_TAGS
    assert 'PROPN' in NOUN_TAGS
    assert 'VERB' not in NOUN_TAGS


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
    """
    Verify that the `POS_WORD_TAGS` `frozenset` strips out the 'X'
    (Other) tag.
    """
    assert isinstance(POS_WORD_TAGS, frozenset)
    assert 'NOUN' in POS_WORD_TAGS
    assert 'VERB' in POS_WORD_TAGS
    assert 'X' not in POS_WORD_TAGS
