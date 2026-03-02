"""Tests for analysis commands."""

from textwarp._commands import analysis
from textwarp._cli.constants.messages import ENTER_VALID_NUMBER_PROMPT


def test_char_count(capsys):
    """Test that char_count prints the formatted character count."""
    analysis.char_count('Call me Ishmael.')
    captured = capsys.readouterr()

    assert 'Character count: 16' in captured.out


def test_line_count(capsys):
    """Test that line_count prints the formatted line count."""
    analysis.line_count('so much depends\nupon\na red wheel\nbarrow')
    captured = capsys.readouterr()

    assert 'Line count: 4' in captured.out


def test_mfws(simulate_input, capsys):
    """Test the most frequent words command and its input loop."""
    simulate_input(['invalid', '2'])

    analysis.mfws('Rose is a rose is a rose is a rose.')
    captured = capsys.readouterr()

    assert ENTER_VALID_NUMBER_PROMPT in captured.out

    assert 'rose' in captured.out
    assert 'is' in captured.out
    assert 'daffodil' not in captured.out


def test_pos_count(capsys):
    """
    Test that pos_count prints a formatted table of parts-of-speech
    counts.
    """
    analysis.pos_count('I celebrate myself, and sing myself.')
    captured = capsys.readouterr()

    assert 'Nouns' in captured.out
    assert 'Verbs' in captured.out
    assert 'Adjectives' in captured.out
    assert '%' in captured.out


def test_sentence_count(capsys):
    """Test that sentence_count prints the formatted sentence count."""
    analysis.sentence_count(
        'The best lack all conviction, while the worst'
        'Are full of passionate intensity.'
        'Surely some revelation is at hand;'
        'Surely the Second Coming is at hand.'
    )
    captured = capsys.readouterr()

    assert 'Sentence count: 2' in captured.out


def test_time_to_read(simulate_input, capsys):
    """Test the time to read command and its input loop."""
    simulate_input(['wrong', '250'])
    dummy_text = 'chrysanthemum ' * 500

    analysis.time_to_read(dummy_text)
    captured = capsys.readouterr()

    assert ENTER_VALID_NUMBER_PROMPT in captured.out

    assert '2 minutes' in captured.out


def test_word_count(capsys):
    """Test that word_count prints the formatted word count."""
    analysis.word_count('Cogito, ergo sum.')
    captured = capsys.readouterr()

    assert 'Word count: 3' in captured.out
