"""Tests for spaCy-based entity capitalization mapping."""

from textwarp._lib.casing.entity_casing import map_all_entities
from textwarp._lib.nlp import process_as_doc


def test_map_all_entities_absolute():
    """
    Test absolute entities map casing.
    """
    doc = process_as_doc('They bought a blu-ray player to watch casablanca.')
    entity_map = map_all_entities(doc)

    found_blu_ray = False
    for span, _, cased_text in entity_map.values():
        if span.text.lower() == 'blu-ray':
            assert cased_text == 'Blu-ray'
            found_blu_ray = True

    assert found_blu_ray is True


def test_map_all_entities_contextual():
    """Test contextual entities map casing."""
    doc = process_as_doc('the aids activist wore hearing aids.')
    entity_map = map_all_entities(doc)

    found_uppercase_aids = False
    for span, _, cased_text in entity_map.values():
        if span.start == 1 and span.text.lower() == 'aids':
            assert cased_text == 'AIDS'
            found_uppercase_aids = True

        elif span.start == 5 and span.text.lower() == 'aids':
            assert cased_text == 'Aids'

    assert found_uppercase_aids is True


def test_map_all_entities_model_fallback():
    """
    Test that spaCy model entities are captured without forced casing.
    """
    doc = process_as_doc(
        'Dorothy lived in the midst of the great Kansas prairies.'
    )
    entity_map = map_all_entities(doc)

    found_kansas = False
    for span, _, cased_text in entity_map.values():
        if span.text == 'Kansas':
            assert cased_text is None
            found_kansas = True

    assert found_kansas is True
