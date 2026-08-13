"""Tests for core analytical models."""

from textwarp._core.enums import POSTag
from textwarp._core.models import POSCounts, WordCount
from textwarp._core.constants.nlp import POS_TAGS


def test_word_count_initialization():
    word_count = WordCount(word='alone', count=6, percentage=0.15)

    assert word_count.word == 'alone'
    assert word_count.count == 6
    assert word_count.percentage == 0.15


def test_pos_counts_initialization():
    pos_counts = POSCounts()

    assert pos_counts.word_count == 0
    assert pos_counts.tag_counts == {}


def test_pos_counts_get_pos_counts():
    pos_counts = POSCounts(
        word_count=4,
        tag_counts={POSTag.NOUN: 1, POSTag.VERB: 1}
    )

    assert pos_counts.get_pos_counts(POSTag.ADJ) == 0
    assert pos_counts.get_pos_counts(POSTag.NOUN) == 1
    assert pos_counts.get_pos_counts(POSTag.VERB) == 1


def test_pos_counts_get_percentage():
    pos_counts = POSCounts(word_count=10, tag_counts={POSTag.NOUN: 4})

    assert pos_counts.get_percentage(POSTag.NOUN) == 40.0


def test_pos_counts_get_percentage_zero_word_count():
    pos_counts = POSCounts(word_count=0, tag_counts={POSTag.NOUN: 4})

    assert pos_counts.get_percentage(POSTag.NOUN) == 0.0


def test_pos_counts_get_pos_data():
    pos_counts = POSCounts(
        word_count=20,
        tag_counts={POSTag.NOUN: 10, POSTag.VERB: 5}
    )
    pos_data = pos_counts.get_pos_data()

    assert len(pos_data) == len(POS_TAGS)

    pos_dict = {
        name: (count, percentage) for name, count, percentage in pos_data
    }

    assert pos_dict['Nouns'] == (10, 50.0)
    assert pos_dict['Verbs'] == (5, 25.0)
    assert pos_dict['Adjectives'] == (0, 0.0)
