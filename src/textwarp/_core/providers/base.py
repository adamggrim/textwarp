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
        Regular expression for matching either apostrophes within words
        or elisions.
        """
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
    def open_quotes(self) -> frozenset[str]:
        """Opening quote characters for the locale."""
        pass

    @property
    @abstractmethod
    def proper_noun_entities(self) -> frozenset[str]:
        """
        Named entities that are typically proper nouns for the locale's
        model.
        """
        pass

    @property
    @abstractmethod
    def punct_inside_pattern(self) -> re.Pattern[str]:
        """
        Regular expression for matching punctuation inside quotation
        marks.
        """
        pass

    @property
    @abstractmethod
    def punct_outside_pattern(self) -> re.Pattern[str]:
        """
        Regular expression for matching punctuation outside quotation
        marks.
        """
        pass

    @property
    @abstractmethod
    def spacy_models(self) -> tuple[str, ...]:
        """Ranking of spaCy models by speed."""
        pass

    @property
    @abstractmethod
    def title_case_tag_exceptions(self) -> frozenset[str]:
        """
        Part-of-speech tag exceptions for title case capitalization.
        """
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

    def curly_to_straight(self, text: str) -> str:
        """
        Convert curly quotes in a given string to straight quotes.
        """
        return text

    @abstractmethod
    def expand_contractions(self, doc: 'Doc') -> str:
        """Expand all contractions in a given spaCy `Doc`."""
        pass

    @abstractmethod
    def ordinal_to_cardinal(self, text: str) -> str:
        """
        Convert ordinal numbers in a given string to cardinal numbers.
        """
        pass

    def remove_apostrophes(self, text: str) -> str:
        """
        Remove apostrophes from a string without removing single quotes.
        """
        return text

    @abstractmethod
    def should_always_lowercase(self, text: str) -> bool:
        """
        Determine if a specific token string should always remain
        lowercase.
        """
        pass

    def straight_to_curly(self, text: str) -> str:
        """
        Convert straight quotes in a given string to curly quotes.
        """
        return text
