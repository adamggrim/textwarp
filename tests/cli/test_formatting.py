"""Tests for CLI output formatting."""

from textwarp._cli.formatting import (
    _format_table,
    format_count,
    format_mfws,
    format_pos_count,
    format_time_to_read
)
from textwarp._core.models import POSCounts, WordCount


def test_format_table():
    """
    Test that the internal table formatter aligns columns correctly.
    """
    data = [
        ('Penelope', '1', '(25.0%)'),
        ('Circe', '1', '(25.0%)'),
        ('Lestrygonians', '2', '(50.0%)')
    ]
    result = _format_table(data, padding=2)
    lines = result.split('\n')

    assert len(lines) == 3
    # Check alignment and padding length
    assert lines[0] == 'Penelope       1  (25.0%)'
    assert lines[1] == 'Circe          1  (25.0%)'
    assert lines[2] == 'Lestrygonians  2  (50.0%)'

    assert _format_table([]) == ''


def test_format_count():
    """Test standard count formatting."""
    assert format_count('Word', 451) == 'Word count: 451'
    assert format_count('Character', 1984) == 'Character count: 1984'


def test_format_mfws():
    """Test formatting of most frequent words data."""
    mock_mfws = [
        WordCount(word='the', count=10, percentage=50.0),
        WordCount(word='a', count=5, percentage=25.0)
    ]
    result = format_mfws(mock_mfws)

    assert 'the' in result
    assert '10' in result
    assert '(50.00%)' in result
    assert 'a' in result
    assert '5' in result
    assert '(25.00%)' in result


def test_format_pos_count():
    """Test formatting of parts-of-speech counts."""
    mock_pos_counts = POSCounts(
        word_count=20,
        tag_counts={'NOUN': 10, 'VERB': 5}
    )
    result = format_pos_count(mock_pos_counts)

    # Nouns should represent 50% (10/20)
    assert 'Nouns' in result
    assert '10' in result
    assert '(50.00%)' in result

    # Verbs should represent 25% (5/20)
    assert 'Verbs' in result
    assert '5' in result
    assert '(25.00%)' in result


def test_format_time_to_read():
    """Test time-to-read formatting for various minute values."""
    assert format_time_to_read(0) == 'Less than 1 minute'
    assert format_time_to_read(1) == '1 minute'
    assert format_time_to_read(45) == '45 minutes'
    assert format_time_to_read(60) == '1 hour'
    assert format_time_to_read(61) == '1 hour, 1 minute'
    assert format_time_to_read(125) == '2 hours, 5 minutes'
