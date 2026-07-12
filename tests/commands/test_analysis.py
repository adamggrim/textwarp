"""Tests for analysis commands."""

from textwarp._commands import analysis
from textwarp._cli.constants.messages import ENTER_VALID_NUMBER_PROMPT


def test_char_count(capsys):
    analysis.char_count('Call me Ishmael.')
    captured = capsys.readouterr()

    assert 'Character count: 16' in captured.out


def test_line_count(capsys):
    analysis.line_count('so much depends\nupon\na red wheel\nbarrow')
    captured = capsys.readouterr()

    assert 'Line count: 4' in captured.out


def test_mfws(simulate_input, capsys):
    simulate_input(['invalid', '2'])

    analysis.mfws('Rose is a rose is a rose is a rose.')
    captured = capsys.readouterr()

    assert ENTER_VALID_NUMBER_PROMPT in captured.out

    assert 'rose' in captured.out
    assert 'is' in captured.out
    assert 'daffodil' not in captured.out


def test_pos_counts(capsys):
    analysis.pos_counts('Colorless green ideas sleep furiously.')
    captured = capsys.readouterr()

    assert 'Nouns' in captured.out
    assert 'Verbs' in captured.out
    assert 'Adjectives' in captured.out
    assert '%' in captured.out


def test_sentence_count(capsys):
    analysis.sentence_count(
        'The best lack all conviction, while the worst\n'
        'Are full of passionate intensity.\n'
        'Surely some revelation is at hand;\n'
        'Surely the Second Coming is at hand.'
    )
    captured = capsys.readouterr()

    assert 'Sentence count: 2' in captured.out


def test_time_to_read(simulate_input, capsys):
    simulate_input(['wrong', '250'])
    dummy_text = 'A Brief History of Time ' * 237

    analysis.time_to_read(dummy_text)
    captured = capsys.readouterr()

    assert ENTER_VALID_NUMBER_PROMPT in captured.out

    assert '5 minutes' in captured.out


def test_word_count(capsys):
    analysis.word_count('Words, words, words.')
    captured = capsys.readouterr()

    assert 'Word count: 3' in captured.out
