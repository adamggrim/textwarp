"""Tests for analysis commands."""

from textwarp._commands import analysis


def test_char_count():
    result = analysis.char_count('Call me Ishmael.')
    assert 'Character count: 16' in result


def test_entity_counts():
    result = analysis.entity_counts(
        'How a Ship having passed the Line was driven by storms to the cold '
        'Country towards the South Pole; and how from thence she made her '
        'course to the tropical Latitude of the Great Pacific Ocean; and of '
        'the strange things that befell; and in what manner the Ancyent '
        'Marinere came back to his own Country.',
        limit=3
    )

    lines = [line for line in result.split('\n') if line.strip()]
    assert len(lines) <= 3
    if lines:
        assert all('%' in line for line in lines)


def test_line_count():
    result = analysis.line_count(
        'so much depends\n'
        'upon\n'
        'a red wheel\n'
        'barrow'
    )

    assert 'Line count: 4' in result


def test_mfws():
    result = analysis.mfws(
        'Rose is a rose is a rose is a rose.',
        limit=2
    )

    assert 'rose' in result
    assert 'is' in result


def test_pos_counts():
    result = analysis.pos_counts('The present King of France is bald.')

    lines = [line for line in result.split('\n') if line.strip()]
    assert len(lines) > 0
    for line in lines:
        assert '%' in line
        assert any(char.isdigit() for char in line)


def test_sentence_count():
    result = analysis.sentence_count(
        'The best lack all conviction, while the worst\n'
        'Are full of passionate intensity.\n'
        'Surely some revelation is at hand;\n'
        'Surely the Second Coming is at hand.'
    )

    assert 'Sentence count: 2' in result


def test_time_to_read():
    text = 'A Brief History of Time ' * 300

    result = analysis.time_to_read(text, wpm=250)

    assert '6 minutes to read' in result


def test_ttr():
    result = analysis.ttr(
        'Tyger Tyger, burning bright,\n'
        'In the forests of the night;\n'
        'What immortal hand or eye,\n'
        'Could frame thy fearful symmetry?'
    )

    assert 'Type-token ratio:' in result
    assert '0.90' in result


def test_word_count():
    result = analysis.word_count('Words, words, words.')

    assert 'Word count: 3' in result
