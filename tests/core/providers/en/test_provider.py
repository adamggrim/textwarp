"""Tests for the EnglishProvider implementation."""

from textwarp._core.providers.en.provider import EnglishProvider
from textwarp._lib.nlp import process_as_doc


def test_english_provider_properties():
    """
    Verify that `EnglishProvider` returns the correct types for its
    properties.
    """
    provider = EnglishProvider()
    assert isinstance(provider.spacy_models, tuple)
    assert isinstance(provider.base_verb_tags, frozenset)
    assert isinstance(provider.have_auxiliaries, frozenset)
    assert isinstance(provider.third_person_singular_pronouns, frozenset)
    assert isinstance(provider.title_case_tag_exceptions, frozenset)
    assert isinstance(provider.wh_words, frozenset)
    assert 'who' in provider.wh_words
    assert 'why' in provider.wh_words


def test_cardinal_to_ordinal():
    """Test cardinal-to-ordinal conversion through the provider."""
    provider = EnglishProvider()
    result = provider.cardinal_to_ordinal('Platform 9 3/4')
    assert result == 'Platform 9 3/4ths'


def test_ordinal_to_cardinal():
    """Test ordinal-to-cardinal conversion through the provider."""
    provider = EnglishProvider()
    result = provider.ordinal_to_cardinal('742nd Evergreen Terrace')
    assert result == '742 Evergreen Terrace'


def test_case_from_string():
    """Test word capitalization rules through the provider."""
    provider = EnglishProvider()
    assert provider.case_from_string('lennon') == 'Lennon'
    assert provider.case_from_string('mccartney') == 'McCartney'
    assert provider.case_from_string('qWeRTy') == 'qWeRTy'


def test_expand_contractions():
    """Test contraction expansion using the provider."""
    provider = EnglishProvider()

    text = "Help me, Obi-Wan Kenobi. You're my only hope."
    doc = process_as_doc(text)

    result = provider.expand_contractions(doc)
    assert result == "Help me, Obi-Wan Kenobi. You are my only hope."


def test_should_always_lowercase():
    """
    Test the identification of particles and suffixes that should
    always be lowercase.
    """
    provider = EnglishProvider()

    assert provider.should_always_lowercase('von') is True
    assert provider.should_always_lowercase("n't") is True
    assert provider.should_always_lowercase('The') is False
