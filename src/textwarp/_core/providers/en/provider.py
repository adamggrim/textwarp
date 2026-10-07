"""English-specific `LanguageProvider` implementation."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

import regex as re

if TYPE_CHECKING:
    from spacy.tokens import Doc, Span, Token

    from textwarp._core.types import EntityCasingContext

from textwarp._core.enums import MainPOSTag, UniversalPOSTag
from textwarp._core.providers import en
from textwarp._core.providers.base import LanguageProvider

__all__ = ['EnglishProvider']


class EnglishProvider(LanguageProvider):
    """English language rules for text warping."""

    @property
    def absolute_casings_map(self) -> Mapping[str, str]:
        """Mapping for absolute entity casing."""
        return en.data.entity_casing.get_absolute_map()

    @property
    def contextual_casings_map(self) -> Mapping[
        str, tuple['EntityCasingContext', ...]
    ]:
        """Mapping for contextual entity casing."""
        return en.data.entity_casing.get_contextual_map()

    @property
    def open_quotes(self) -> frozenset[str]:
        """Opening quote characters for the locale."""
        return en.constants.OPEN_QUOTES

    @property
    def pos_tags(self) -> tuple[tuple[MainPOSTag, str], ...]:
        """Part-of-speech tags and their localized labels."""
        return en.constants.POS_TAGS

    @property
    def pos_mapping(self) -> Mapping[UniversalPOSTag, MainPOSTag]:
        """Mapping of Universal POS tags to Main POS tags."""
        return {
            UniversalPOSTag.ADJ: MainPOSTag.ADJ,
            UniversalPOSTag.ADP: MainPOSTag.ADP,
            UniversalPOSTag.ADV: MainPOSTag.ADV,
            UniversalPOSTag.AUX: MainPOSTag.VERB,
            UniversalPOSTag.CCONJ: MainPOSTag.CONJ,
            UniversalPOSTag.DET: MainPOSTag.ADJ,
            UniversalPOSTag.INTJ: MainPOSTag.INTJ,
            UniversalPOSTag.NOUN: MainPOSTag.NOUN,
            UniversalPOSTag.PART: MainPOSTag.ADV,
            UniversalPOSTag.PRON: MainPOSTag.PRON,
            UniversalPOSTag.PROPN: MainPOSTag.NOUN,
            UniversalPOSTag.SCONJ: MainPOSTag.CONJ,
            UniversalPOSTag.VERB: MainPOSTag.VERB
        }

    @property
    def pos_word_tags(self) -> frozenset[UniversalPOSTag]:
        """Part-of-speech tags that count as distinct words."""
        return en.constants.POS_WORD_TAGS

    @property
    def proper_noun_entities(self) -> frozenset[str]:
        """Named entities that are typically proper nouns."""
        return en.constants.PROPER_NOUN_ENTITIES

    @property
    def spacy_models(self) -> tuple[str, ...]:
        """Ranking of spaCy models by speed."""
        return (
            'en_core_web_sm',
            'en_core_web_md',
            'en_core_web_lg',
            'en_core_web_trf'
        )

    def cardinal_to_ordinal(self, text: str) -> str:
        """
        Convert cardinal numbers in a string to ordinal numbers.

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
        Convert curly quotes in a string to straight quotes.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return en.punctuation.curly_to_straight(text)

    def extract_words(self, text: str) -> list[str]:
        """
        Extract words using Unicode Standard Annex (UAX) #29 text 
        segmentation.
        """
        pattern = re.compile(r'\b', flags=re.V1 | re.WORD)
        segments = pattern.split(text)
        return [seg for seg in segments if any(c.isalnum() for c in seg)]

    def get_title_case_idxs(self, text_container: Doc | Span) -> set[int]:
        """Get the indices of tokens to capitalize for title case."""
        def _find_first_word(start_idx: int) -> int | None:
            for i in range(start_idx, len(text_container)):
                token = text_container[i]
                if not token.is_space and not token.is_punct:
                    return token.i
            return None

        position_idxs: set[int] = set()

        for i, token in enumerate(text_container):
            is_valid_punctuation_boundary = (
                (token.text == ':' or token.text in self.open_quotes)
                and token.i + 1 < len(text_container)
            )

            if i == 0 or token.is_sent_start:
                first_word_idx = _find_first_word(i)
                if first_word_idx is not None:
                    position_idxs.add(first_word_idx)
            elif is_valid_punctuation_boundary:
                first_word_idx = _find_first_word(i + 1)
                if first_word_idx is not None:
                    position_idxs.add(first_word_idx)
            elif self.should_capitalize_in_title(token):
                position_idxs.add(token.i)

        for token in reversed(text_container):
            if not token.is_space and not token.is_punct:
                position_idxs.add(token.i)
                break

        return position_idxs

    def expand_contractions(self, content: str | Doc) -> str:
        """
        Expand all contractions in a string or spaCy `Doc`.

        Args:
            content: A string or spaCy `Doc`.

        Returns:
            str: The converted text.
        """
        return en.expansion.core.expand_contractions(content)

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

    def is_lowercase_particle_or_affix(self, text: str) -> bool:
        """
        Determine if a token string is a particle or contraction suffix
        that should remain lowercase.

        Args:
            text: The string to check.

        Returns:
            bool: `True` if the string should remain lowercase,
                otherwise `False`.
        """
        return en.casing.is_lowercase_particle_or_affix(text)

    def ordinal_to_cardinal(self, text: str) -> str:
        """
        Convert ordinal numbers in a string to cardinal numbers.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return en.numbers.ordinal_to_cardinal(text)

    def punct_to_inside(self, text: str) -> str:
        """
        Move periods and commas at the end of quotes inside quotation
        marks.
        """
        return en.punctuation.punct_to_inside(text)

    def punct_to_outside(self, text: str) -> str:
        """
        Move periods and commas at the end of quotes outside quotation
        marks.
        """
        return en.punctuation.punct_to_outside(text)

    def remove_apostrophes(self, text: str) -> str:
        """
        Remove apostrophes from a string without removing single quotes.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return en.punctuation.remove_apostrophes(text)

    def should_capitalize_in_title(self, token: Token) -> bool:
        """
        Determine whether to capitalize a spaCy `Token` for title case
        based on its part of speech or length.
        """
        return en.casing.should_capitalize_in_title(token)

    def straight_to_curly(self, text: str) -> str:
        """
        Convert straight quotes in a string to curly quotes.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return en.punctuation.straight_to_curly(text)
