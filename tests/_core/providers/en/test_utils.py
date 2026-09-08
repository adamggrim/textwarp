"""Tests for contraction utility functions."""

from textwarp._core.enums import POSTag
from textwarp._core.providers.en.utils import (
    find_subject_token,
    get_negative_contraction_base_verb,
    get_next_lexical_token,
    get_prev_lexical_token
)
from textwarp._lib.nlp import process_as_doc


def test_get_negative_contraction_base_verb():
    assert get_negative_contraction_base_verb('won’t') == 'will'
    assert get_negative_contraction_base_verb('shan’t') == 'shall'
    assert get_negative_contraction_base_verb('cannot') == 'can'
    assert get_negative_contraction_base_verb('can’t') == 'can'
    assert get_negative_contraction_base_verb('didn’t') == 'did'
    assert get_negative_contraction_base_verb('hasn’t') == 'has'
    assert get_negative_contraction_base_verb('doesn’t') == 'does'


def test_find_subject_token_standard_order():
    doc = process_as_doc('We don’t need no education.')
    verb_token = doc[1]
    subject = find_subject_token(verb_token)

    assert subject is not None
    assert subject.text == 'We'


def test_find_subject_token_inverted_order():
    doc = process_as_doc('Isn’t she lovely?')
    verb_token = doc[0]
    subject = find_subject_token(verb_token)

    assert subject is not None
    assert subject.text.lower() == 'she'


def test_get_next_lexical_token():
    doc = process_as_doc('I’d only ever kissed before.')
    token = get_next_lexical_token(
        doc, 2,
        skip_pos={POSTag.SPACE, POSTag.PUNCT, POSTag.ADV}
    )

    assert token is not None
    assert token.text == 'kissed'


def test_get_prev_lexical_token():
    doc = process_as_doc(
        'Just gotta get out, just gotta get right outta here.'
    )
    start_idx = next(t.i for t in doc if t.text == 'right')
    token = get_prev_lexical_token(
        doc,
        start_idx,
        skip_pos={POSTag.SPACE, POSTag.PUNCT, POSTag.ADV}
    )

    assert token is not None
    assert token.text == 'get'


def test_lexical_token_bounds():
    doc = process_as_doc('Here, there and everywhere')
    skip_tags = {POSTag.SPACE, POSTag.PUNCT, POSTag.ADV, POSTag.CCONJ}
    next_token = get_next_lexical_token(
        doc,
        0,
        skip_pos=skip_tags
    )
    assert next_token is None

    prev_token = get_prev_lexical_token(
        doc,
        len(doc) - 1,
        skip_pos=skip_tags
    )
    assert prev_token is None
