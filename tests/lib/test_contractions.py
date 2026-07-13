"""Tests for the main contraction expansion engine."""

from textwarp._lib.contractions import (
    apply_expansion_casing,
    expand_contractions
)
from textwarp._lib.nlp import process_as_doc


def test_apply_expansion_casing_lower():
    assert apply_expansion_casing('can’t', 'can not') == 'can not'


def test_apply_expansion_casing_upper():
    assert apply_expansion_casing('CAN’T', 'can not') == 'CAN NOT'


def test_apply_expansion_casing_sentence():
    assert apply_expansion_casing('Won’t', 'will not') == 'Will not'
    assert apply_expansion_casing(
        'Couldn’t’ve', 'could not have'
    ) == 'Could not have'


def test_apply_expansion_casing_title():
    assert apply_expansion_casing('Don’t Don’t', 'do not do not') == 'Do Not Do Not'


def test_expand_contractions_no_contractions():
    text = ('How does it feel?')
    doc = process_as_doc(text)
    assert expand_contractions(doc) == text


def test_expand_contractions_ambiguous():
    doc = process_as_doc(
        'There’s a starman waitin’ in the sky\n'
        'He’d like to come and meet us\n'
        'But he thinks he’d blow our minds\n'
        'There’s a starman waitin’ in the sky\n'
        'He’s told us not to blow it\n'
        "'Cause he knows it's all worthwhile\n"
    )
    result = expand_contractions(doc)
    assert result == (
        "There is a starman waitin’ in the sky\n"
        'He would like to come and meet us\n'
        'But he thinks he would blow our minds\n'
        "There is a starman waitin’ in the sky\n"
        'He has told us not to blow it\n'
        'Because he knows it is all worthwhile\n'
    )


def test_expand_contractions_unambiguous():
    doc = process_as_doc('They won’t go when I go.')
    result = expand_contractions(doc)
    assert result == 'They will not go when I go.'


def test_expand_contractions_inverted_and_multiple():
    doc = process_as_doc(
        'Ain’t it just like the night to play\n'
        'Tricks when you’re trying to be so quiet?'
    )
    result = expand_contractions(doc)
    assert result == (
        'Is it not just like the night to play\n'
        'Tricks when you are trying to be so quiet?'
    )


def test_expand_contractions_chained():
    doc = process_as_doc(
        'I shouldn’t’ve said that. I should not have said that.'
    )
    result = expand_contractions(doc)
    assert result == 'I should not have said that. I should not have said that.'
