"""English-specific `LanguageProvider` implementation."""

from __future__ import annotations

from typing import Mapping, TYPE_CHECKING

import regex as re

if TYPE_CHECKING:
    from spacy.tokens import Doc
    from textwarp._core.types import EntityCasingContext

from textwarp._core.providers.base import LanguageProvider
from textwarp._core.providers import en

__all__ = ['EnglishProvider']


class EnglishProvider(LanguageProvider):
    """English language rules for text warping."""

    @property
    def absolute_casings_map(self) -> Mapping[str, str]:
        """Mapping for absolute entity casing."""
        return en.data.entity_casing.get_absolute_map()

    @property
    def apostrophe_in_word_pattern(self) -> re.Pattern[str]:
        """
        Regular expression for matching either apostrophes within words
        or elisions.
        """
        return en.patterns.get_apostrophe_in_word()

    @property
    def base_verb_tags(self) -> frozenset[str]:
        """Fine-grained parts-of-speech tags for base verb forms."""
        return en.constants.BASE_VERB_TAGS

    @property
    def contextual_casings_map(self) -> Mapping[
        str, tuple['EntityCasingContext', ...]
    ]:
        """Mapping for contextual entity casing."""
        return en.data.entity_casing.get_contextual_map()

    @property
    def have_auxiliaries(self) -> frozenset[str]:
        """Auxiliary verbs forms of "have"."""
        return en.constants.HAVE_AUXILIARIES

    @property
    def noun_phrase_tags(self) -> frozenset[str]:
        """
        Fine-grained parts-of-speech tags for the first word of a noun
        phrase.
        """
        return en.constants.NOUN_PHRASE_TAGS

    @property
    def open_quotes(self) -> frozenset[str]:
        """Opening quote characters for the locale."""
        return en.constants.OPEN_QUOTES

    @property
    def participle_tags(self) -> frozenset[str]:
        """
        Fine-grained parts-of-speech tags for past tense and past
        participle verb forms. (Fine-grained tags used to distinguish
        verb tense.)
        """
        return en.constants.PARTICIPLE_TAGS

    @property
    def proper_noun_entities(self) -> frozenset[str]:
        """Named entities that are typically proper nouns."""
        return en.constants.PROPER_NOUN_ENTITIES

    @property
    def punct_inside_pattern(self) -> re.Pattern[str]:
        """
        Regular expression for matching punctuation inside quotation
        marks.
        """
        return en.patterns.get_punct_inside()

    @property
    def punct_outside_pattern(self) -> re.Pattern[str]:
        """
        Regular expression for matching punctuation outside quotation
        marks.
        """
        return en.patterns.get_punct_outside()

    @property
    def singular_noun_tags(self) -> frozenset[str]:
        """
        Fine-grained parts-of-speech tags for singular nouns and proper
        nouns.
        """
        return en.constants.SINGULAR_NOUN_TAGS

    @property
    def spacy_models(self) -> tuple[str, ...]:
        """Ranking of spaCy models by speed."""
        return (
            'en_core_web_sm',
            'en_core_web_md',
            'en_core_web_lg',
            'en_core_web_trf'
        )

    @property
    def third_person_singular_pronouns(self) -> frozenset[str]:
        """
        Third-person singular pronouns for subject-verb agreement
        checks.
        """
        return en.constants.THIRD_PERSON_SINGULAR_PRONOUNS

    @property
    def title_case_tag_exceptions(self) -> frozenset[str]:
        """
        Fine-grained parts-of-speech tag exceptions for title case
        capitalization. (Fine-grained tags used to distinguish articles
        from possessives.)
        """
        return en.constants.TITLE_CASE_TAG_EXCEPTIONS

    @property
    def wh_words(self) -> frozenset[str]:
        """Wh-words that start questions."""
        return en.constants.WH_WORDS

    def cardinal_to_ordinal(self, text: str) -> str:
        """
        Convert cardinal numbers in a given string to ordinal numbers.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return en.numbers.cardinal_to_ordinal(text)

    def case_from_string(
        self,
        word: str,
        lowercase_by_default: bool = False,
        preserve_mixed_case: bool = True
    ) -> str:
        """
        Capitalize a word, handling special name prefixes and preserving
        other mid-word capitalizations.

        Args:
            word: The word to capitalize.
            lowercase_by_default: Whether to lowercase the word if no
                capitalization strategy applies. Defaults to `False`.
            preserve_mixed_case: Whether to preserve mixed-case words.
                Defaults to `True`.

        Returns:
            str: The capitalized word.
        """
        return en.casing.case_from_string(
            word, lowercase_by_default, preserve_mixed_case
        )

    def curly_to_straight(self, text: str) -> str:
        """
        Convert curly quotes in a given string to straight quotes.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return en.punctuation.curly_to_straight(text)

    def expand_contractions(self, doc: Doc) -> str:
        """
        Expand all contractions in a given spaCy `Doc`.

        Args:
            doc: A spaCy `Doc`.

        Returns:
            str: The converted `Doc` text.
        """
        return en.expansion.expand_contractions(doc)

    def normalize_for_morse(self, text: str) -> str:
        """
        Normalize a string for Morse code by converting to all caps and
        replacing non-Morse-compatible characters.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return en.encoding.normalize_for_morse(text)

    def ordinal_to_cardinal(self, text: str) -> str:
        """
        Convert ordinal numbers in a given string to cardinal numbers.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return en.numbers.ordinal_to_cardinal(text)

    def remove_apostrophes(self, text: str) -> str:
        """
        Remove apostrophes from a string without removing single quotes.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return en.punctuation.remove_apostrophes(text)

    def should_always_lowercase(self, text: str) -> bool:
        """
        Determine if a specific token string should always remain
        lowercase (e.g., particles like "von" or contraction suffixes
        like "n't").

        Args:
            text: The string to check.

        Returns:
            bool: `True` if the string should always be lowercase,
                otherwise `False`.
        """
        return en.casing.should_always_lowercase(text)

    def straight_to_curly(self, text: str) -> str:
        """
        Convert straight quotes in a given string to curly quotes.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return en.punctuation.straight_to_curly(text)
