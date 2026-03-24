"""Abstract base class for language providers."""

from abc import ABC, abstractmethod
from typing import Mapping, TYPE_CHECKING
import regex as re

if TYPE_CHECKING:
    from spacy.tokens import Doc
    from textwarp._core.types import EntityCasingContext

__all__ = ['LanguageProvider']


class LanguageProvider(ABC):
    """Interface for language-specific text processing rules."""

    @property
    @abstractmethod
    def absolute_casings_map(self) -> Mapping[str, str]:
        """Mapping for absolute entity casing."""
        pass

    @property
    @abstractmethod
    def apostrophe_in_word_pattern(self) -> re.Pattern[str]:
        """
        Regular expression for matching apostrophes within words or
        elisions.
        """
        pass

    @property
    @abstractmethod
    def base_verb_tags(self) -> frozenset[str]:
        """Fine-grained parts-of-speech tags for base verb forms."""
        pass

    @property
    @abstractmethod
    def contextual_casings_map(self) -> Mapping[
        str, tuple['EntityCasingContext', ...]
    ]:
        """Mapping for contextual entity casing."""
        pass

    @property
    @abstractmethod
    def have_auxiliaries(self) -> frozenset[str]:
        """Auxiliary verbs forms of "have"."""
        pass

    @property
    @abstractmethod
    def noun_phrase_tags(self) -> frozenset[str]:
        """Fine-grained parts-of-speech tags for the first word of a noun phrase."""
        pass

    @property
    @abstractmethod
    def participle_tags(self) -> frozenset[str]:
        """
        Fine-grained parts-of-speech tags for past tense and past participle
        verb forms. (Fine-grained tags used to distinguish verb tense.)
        """
        pass

    @property
    @abstractmethod
    def singular_noun_tags(self) -> frozenset[str]:
        """Fine-grained parts-of-speech tags for singular nouns and proper nouns."""
        pass

    @property
    @abstractmethod
    def spacy_models(self) -> tuple[str, ...]:
        """Ranking of spaCy models by speed."""
        pass

    @property
    @abstractmethod
    def third_person_singular_pronouns(self) -> frozenset[str]:
        """Pronouns for subject-verb agreement checks."""
        pass

    @property
    @abstractmethod
    def title_case_tag_exceptions(self) -> frozenset[str]:
        """
        Part-of-speech tag exceptions for title case capitalization.
        """
        pass

    @property
    @abstractmethod
    def wh_words(self) -> frozenset[str]:
        """Words that start questions."""
        pass

    @abstractmethod
    def cardinal_to_ordinal(self, text: str) -> str:
        """
        Convert cardinal numbers in a given string to ordinal numbers.
        """
        pass

    @abstractmethod
    def case_from_string(
        self,
        word: str,
        lowercase_by_default: bool = False,
        preserve_mixed_case: bool = True
    ) -> str:
        """Capitalize a word according to language-specific rules."""
        pass

    @abstractmethod
    def expand_contractions(self, doc: 'Doc') -> str:
        """
        Expand all contractions in a given spaCy `Doc`.
        """
        pass

    @abstractmethod
    def ordinal_to_cardinal(self, text: str) -> str:
        """
        Convert ordinal numbers in a given string to cardinal numbers.
        """
        pass

    @abstractmethod
    def should_always_lowercase(self, text: str) -> bool:
        """
        Determine if a specific token string should always remain
        lowercase (e.g., particles like "von" or contraction suffixes
        like "n't").
        """
        pass
