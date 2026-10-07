"""Tests for the EnglishProvider implementation."""

from textwarp._core.providers.en.provider import EnglishProvider
from textwarp._lib.nlp import process_as_doc


def test_english_provider_properties():
    provider = EnglishProvider()
    assert isinstance(provider.spacy_models, tuple)
    assert isinstance(provider.open_quotes, frozenset)
    assert isinstance(provider.pos_tags, tuple)
    assert isinstance(provider.pos_word_tags, frozenset)
    assert isinstance(provider.proper_noun_entities, frozenset)


def test_cardinal_to_ordinal():
    provider = EnglishProvider()
    result = provider.cardinal_to_ordinal('Platform 9 3/4')
    assert result == 'Platform 9 3/4ths'


def test_ordinal_to_cardinal():
    provider = EnglishProvider()
    result = provider.ordinal_to_cardinal('742nd Evergreen Terrace')
    assert result == '742 Evergreen Terrace'


def test_case_from_string():
    provider = EnglishProvider()
    assert provider.case_from_string('lennon') == 'Lennon'
    assert provider.case_from_string('mccartney') == 'McCartney'
    assert provider.case_from_string('NeXTSTEP') == 'NeXTSTEP'


def test_expand_contractions():
    provider = EnglishProvider()

    text = ('It’s a truth universally acknowledged, that a word in possession '
            'of an apostrophe, must be in want of expansion.')
    doc = process_as_doc(text)

    result = provider.expand_contractions(doc)
    assert result == (
        'It is a truth universally acknowledged, that a word in possession of '
        'an apostrophe, must be in want of expansion.'
    )


def test_is_lowercase_particle_or_affix():
    provider = EnglishProvider()

    assert provider.is_lowercase_particle_or_affix('von') is True
    assert provider.is_lowercase_particle_or_affix("n't") is True
    assert provider.is_lowercase_particle_or_affix('The') is False
