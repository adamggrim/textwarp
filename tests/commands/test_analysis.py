"""Tests for analysis commands."""

from textwarp._commands import analysis
from textwarp._cli.constants.messages import ENTER_VALID_NUMBER_PROMPT


def test_char_count():
    result = analysis.char_count('Call me Ishmael.')
    assert 'Character count: 16' in result


def test_entity_counts(simulate_input, capsys):
    simulate_input(['invalid', '3'])

    result = analysis.entity_counts(
        'How a Ship having passed the Line was driven by storms to the cold '
        'Country towards the South Pole; and how from thence she made her '
        'course to the tropical Latitude of the Great Pacific Ocean; and of '
        'the strange things that befell; and in what manner the Ancyent '
        'Marinere came back to his own Country.'
    )
    captured = capsys.readouterr()

    assert ENTER_VALID_NUMBER_PROMPT in captured.out

    assert "'the South Pole'" in result
    assert '1' in result
    assert "'Latitude of the Great Pacific Ocean'" in result


def test_line_count():
    result = analysis.line_count(
        'so much depends\n'
        'upon\n'
        'a red wheel\n'
        'barrow'
    )

    assert 'Line count: 4' in result


def test_mfws(simulate_input, capsys):
    simulate_input(['invalid', '2'])

    result = analysis.mfws('Rose is a rose is a rose is a rose.')
    captured = capsys.readouterr()

    assert ENTER_VALID_NUMBER_PROMPT in captured.out

    assert 'rose' in result
    assert 'is' in result
    assert 'daffodil' not in result


def test_pos_counts():
    result = analysis.pos_counts('Colorless green ideas sleep furiously.')

    assert 'Nouns' in result
    assert 'Verbs' in result
    assert 'Adjectives' in result
    assert '%' in result


def test_sentence_count():
    result = analysis.sentence_count(
        'The best lack all conviction, while the worst\n'
        'Are full of passionate intensity.\n'
        'Surely some revelation is at hand;\n'
        'Surely the Second Coming is at hand.'
    )

    assert 'Sentence count: 2' in result


def test_time_to_read(simulate_input, capsys):
    simulate_input(['wrong', '250'])
    dummy_text = 'A Brief History of Time ' * 237

    result = analysis.time_to_read(dummy_text)
    captured = capsys.readouterr()

    assert ENTER_VALID_NUMBER_PROMPT in captured.out

    assert '5 minutes to read' in result


def test_ttr():
    result = analysis.ttr(
        'Bent double, like old beggars under sacks,\n'
        'Knock-kneed, coughing like hags, we cursed through sludge,\n'
        'Till on the haunting flares we turned our backs\n'
        'And towards our distant rest began to trudge.'
    )

    assert 'Type-token ratio:' in result
    assert '0.91' in result


def test_word_count():
    result = analysis.word_count('Words, words, words.')

    assert 'Word count: 3' in result
