"""Tests for core analytical models."""

from textwarp._core.models import POSCounts, WordCount
from textwarp._core.constants.nlp import POS_TAGS


def test_word_count_initialization():
    """Test that WordCount initializes and stores its attributes."""
    word_count = WordCount(word='alone', count=6, percentage=0.15)

    assert word_count.word == 'alone'
    assert word_count.count == 6
    assert word_count.percentage == 0.15


def test_pos_counts_initialization():
    """Test POSCounts initialization."""
    pos_counts = POSCounts()

    assert pos_counts.word_count == 0
    assert pos_counts.tag_counts == {}


def test_pos_counts_get_pos_counts():
    """Test retrieving counts for part-of-spech tags."""
    pos_counts = POSCounts(word_count=4, tag_counts={'NOUN': 1, 'VERB': 1})

    assert pos_counts.get_pos_counts('ADJ') == 0
    assert pos_counts.get_pos_counts('NOUN') == 1
    assert pos_counts.get_pos_counts('VERB') == 1


def test_pos_counts_get_percentage():
    """Test percentage calculation for part-of-speech tags."""
    pos_counts = POSCounts(word_count=10, tag_counts={'NOUN': 4})

    assert pos_counts.get_percentage('NOUN') == 40.0
    assert pos_counts.get_percentage('VERB') == 0.0


def test_pos_counts_get_percentage_zero_word_count():
    """Test that get_percentage safely handles a word count of 0."""
    pos_counts = POSCounts(word_count=0, tag_counts={'NOUN': 4})

    assert pos_counts.get_percentage('NOUN') == 0.0


def test_pos_counts_get_pos_data():
    """Test that get_pos_data maps internal tags to display names."""
    pos_counts = POSCounts(word_count=20, tag_counts={'NOUN': 10, 'VERB': 5})
    pos_data = pos_counts.get_pos_data()

    assert len(pos_data) == len(POS_TAGS)

    pos_dict = {
        name: (count, percentage) for name, count, percentage in pos_data
    }

    assert pos_dict['Nouns'] == (10, 50.0)
    assert pos_dict['Verbs'] == (5, 25.0)
    assert pos_dict['Adjectives'] == (0, 0.0)
