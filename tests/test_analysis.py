"""Tests for analysis functions."""

from textwarp.analysis import (
    calculate_time_to_read,
    count_chars,
    count_lines,
    count_mfws,
    count_pos,
    count_sents,
    count_words
)
from textwarp._core.models import POSCounts

TIME_TO_READ_TEXT = (
    'riverrun, past Eve and Adam’s, from swerve of shore to bend of bay, '
    'brings us by a commodius vicus of recirculation back to Howth Castle and '
    'Environs.\n'
    'Sir Tristram, violer d’amores, fr’over the short sea, had passencore '
    'rearrived from North Armorica on this side the scraggy isthmus of Europe '
    'Minor to wielderfight his penisolate war: nor had topsawyer’s rocks by '
    'the stream Oconee exaggerated themselse to Laurens County’s gorgios '
    'while they went doublin their mumper all the time: nor avoice from afire '
    'bellowsed mishe mishe to tauftauf thuartpeatrick not yet, though '
    'venissoon after, had a kidscad buttended a bland old isaac: not yet, '
    'though all’s fair in vanessy, were sosie sesthers wroth with twone '
    'nathandjoe.\n'
    'Rot a peck of pa’s malt had Jhem or Shen brewed by arclight and rory end '
    'to the regginbrow was to be seen ringsome on the aquaface.')

COUNT_CHARS_TEXT = 'Even the sun-clouds this morning cannot manage such skirts.'

COUNT_LINES_TEXT = (
    'Does it dry up\n'
    'like a raisin in the sun?'
)

COUNT_MFWS_TEXT = (
    '‘You gave me hyacinths first a year ago;\n'
    '‘They called me the hyacinth girl.’\n'
    '—Yet when we came back, late, from the Hyacinth garden,\n'
    'Your arms full, and your hair wet, I could not\n'
    'Speak, and my eyes failed, I was neither\n'
    'Living nor dead, and I knew nothing,\n'
    'Looking into the heart of light, the silence.'
)

COUNT_POS_TEXT = (
    'The apparition of these faces in the crowd:\n'
    'Petals on a wet, black bough.'
)

COUNT_SENTS_TEXT = (
    'Gatsby believed in the green light, the orgiastic future that year by '
    'year recedes before us. It eluded us then, but that’s no matter—tomorrow '
    'we will run faster, stretch out our arms further… And one fine morning—\n'
    'So we beat on, boats against the current, borne back ceaselessly into '
    'the past.'
)

COUNT_WORDS_TEXT = (
    'Awaking with a start,\n'
    'The waters heave around me; and on high\n'
    'The winds lift up their voices: I depart,\n'
    'Whither I know not; but the hour’s gone by,\n'
    'When Albion’s lessening shores could grieve or glad mine eye.'
)


def test_calculate_time_to_read():
    """Test reading time calculation."""
    assert calculate_time_to_read(TIME_TO_READ_TEXT, wpm=200) == 1

    minutes = calculate_time_to_read(TIME_TO_READ_TEXT, wpm=10)
    assert 14 <= minutes <= 16


def test_count_chars():
    """Test character counting."""
    assert count_chars(COUNT_CHARS_TEXT) == 59


def test_count_lines():
    """Test line counting."""
    assert count_lines(COUNT_LINES_TEXT) == 2


def test_count_mfws():
    """Test most frequent word counting."""
    mfws = count_mfws(COUNT_MFWS_TEXT, num_mfws=5)

    assert len(mfws) == 5

    assert mfws[0].word == 'the'
    assert mfws[0].count == 4

    i_entry = next((w for w in mfws if w.word == 'i'), None)
    assert i_entry is not None
    assert i_entry.count == 3

    hyacinth_entry = next((w for w in mfws if w.word == 'hyacinth'), None)
    assert hyacinth_entry is not None
    assert hyacinth_entry.count == 2


def test_count_pos():
    """Test parts-of-speech counting."""
    pos_counts = count_pos(COUNT_POS_TEXT)

    assert isinstance(pos_counts, POSCounts)

    assert pos_counts.get_pos_count('NOUN') == 5
    assert pos_counts.get_pos_count('ADJ') == 2

    assert pos_counts.get_percentage('NOUN') > 0


def test_count_sents():
    """Test sentence counting."""
    count = count_sents(COUNT_SENTS_TEXT)
    # Depending on the specific spaCy version, "And one fine morning—"
    # would count as three or four sentences.
    assert count in (3, 4)


def test_count_words():
    """
    Test word counting.
    """
    count = count_words(COUNT_WORDS_TEXT)
    assert count == 41
