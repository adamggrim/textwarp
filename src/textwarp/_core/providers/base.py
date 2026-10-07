"""Abstract base class for language providers."""

import unicodedata
from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import TYPE_CHECKING

from textwarp._core.enums import MainPOSTag, UniversalPOSTag

if TYPE_CHECKING:
    from spacy.tokens import Doc, Span, Token

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
    def pos_tags(self) -> tuple[tuple[MainPOSTag, str], ...]:
        """
        Language-specific part-of-speech tags and their localized
        labels.
        """
        pass

    @property
    @abstractmethod
    def pos_word_tags(self) -> frozenset[UniversalPOSTag]:
        """Part-of-speech tags that count as distinct words."""
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
    def spacy_models(self) -> tuple[str, ...]:
        """Ranking of spaCy models by speed."""
        pass

    @property
    @abstractmethod
    def pos_mapping(self) -> Mapping[UniversalPOSTag, MainPOSTag]:
        """
        Mapping from `UniversalPOSTag` to the simplified `MainPOSTag`.
        """
        pass

    @abstractmethod
    def cardinal_to_ordinal(self, text: str) -> str:
        """
        Convert cardinal numbers in a string to ordinal numbers.
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
    def extract_words(self, text: str) -> list[str]:
        """Extract lexical words from a raw string."""
        pass

    @abstractmethod
    def get_title_case_idxs(self, text_container: 'Doc | Span') -> set[int]:
        """Get the indices of tokens to capitalize for title case."""
        pass

    def curly_to_straight(self, text: str) -> str:
        """
        Convert curly quotes in a string to straight quotes.
        """
        return text

    def expand_contractions(self, content: 'str | Doc') -> str:
        """Expand all contractions in a string or spaCy `Doc`."""
        return content if isinstance(content, str) else content.text

    def normalize_for_morse(self, text: str) -> str:
        """
        Normalize a string for Morse code.
        """
        uppercase_text = text.upper()

        normalized = ''.join(
            char for char in unicodedata.normalize('NFD', uppercase_text)
            if unicodedata.category(char) != 'Mn'
        )

        return normalized

    @abstractmethod
    def is_lowercase_particle_or_affix(self, text: str) -> bool:
        """
        Determine if a token string is a particle or affix that should
        remain lowercase.
        """
        pass

    @abstractmethod
    def ordinal_to_cardinal(self, text: str) -> str:
        """
        Convert ordinal numbers in a string to cardinal numbers.
        """
        pass

    def punct_to_inside(self, text: str) -> str:
        """
        Move punctuation at the end of quotes inside quotation marks.
        """
        return text

    def punct_to_outside(self, text: str) -> str:
        """
        Move punctuation at the end of quotes outside quotation marks.
        """
        return text

    def remove_apostrophes(self, text: str) -> str:
        """
        Remove apostrophes from a string without removing single quotes.
        """
        return text

    @abstractmethod
    def should_capitalize_in_title(self, token: 'Token') -> bool:
        """
        Determine whether to capitalize a spaCy `Token` based on
        language-specific rules.
        """
        pass

    def straight_to_curly(self, text: str) -> str:
        """
        Convert straight quotes in a string to curly quotes.
        """
        return text
