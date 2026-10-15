from textwarp._lib.casing.token_casing import should_capitalize_pos_or_length
from textwarp._lib.nlp import process_as_doc


def test_should_capitalize_pos_or_length_delegation():
    doc = process_as_doc('Linus van Pelt and the Great Pumpkin')

    assert should_capitalize_pos_or_length(doc[1]) is False
    assert should_capitalize_pos_or_length(doc[3]) is False
    assert should_capitalize_pos_or_length(doc[6]) is True
