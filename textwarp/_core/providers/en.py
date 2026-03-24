"""English-specific LanguageProvider implementation."""

from __future__ import annotations

from typing import Mapping, TYPE_CHECKING

import regex as re

if TYPE_CHECKING:
    from spacy.tokens import Doc, Span
    from textwarp._core.types import EntityCasingContext

from textwarp._core.providers.base import LanguageProvider
from textwarp._core.providers.en_rules.data import (
    EnContractionExpansion,
    EnEntityCasing,
    EnTokenCasing
)
from textwarp._core.providers.en_rules.constants import (
    BASE_VERB_TAGS,
    HAVE_AUXILIARIES,
    NOUN_PHRASE_TAGS,
    PARTICIPLE_TAGS,
    SINGULAR_NOUN_TAGS,
    THIRD_PERSON_SINGULAR_PRONOUNS,
    TITLE_CASE_TAG_EXCEPTIONS,
    WH_WORDS
)
from textwarp._core.providers.en_rules.casing import en_case_from_string
from textwarp._core.providers.en_rules.regexes import EnWarpingPatterns
from textwarp._core.providers.en_rules.handlers import (
    handle_d,
    handle_gotta,
    handle_negation,
    handle_s,
    handle_wanna,
    handle_whatcha
)
from textwarp._core.providers.en_rules.utils import apply_expansion_casing
from textwarp._lib.punctuation import curly_to_straight

__all__ = ['EnglishProvider']


def _replace_cardinal(match: re.Match[str]) -> str:
    """
    Helper function to replace a matched cardinal number with an
    ordinal.

    Args:
        match: A match object representing a cardinal number found in
            the string.

    Returns:
        str: The ordinal version of the matched cardinal.
    """
    number_str = match.group(0)
    number = int(number_str.replace(',', ''))

    suffix: str
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')

    preceding_text = match.string[:match.start()]
    fraction_match = re.search(r'(\d+)/$', preceding_text)

    if fraction_match:
        numerator = int(fraction_match.group(1))
        if numerator > 1:
            suffix += 's'

    return number_str + suffix


def _replace_ordinal(match: re.Match[str]) -> str:
    """
    Helper function to replace a matched ordinal number with its
    cardinal equivalent.

    Args:
        match: A match object representing an ordinal number found in
            the string.

    Returns:
        str: The cardinal version of the matched ordinal.
    """
    return match.group(1)


def _expand_ambiguous_contraction(
    contraction: str,
    span: Span
) -> tuple[str, int]:
    """
    Helper function to replace a matched ambiguous contraction with its
    expanded version.

    This function uses spaCy to disambiguate contractions based on
    context.

    Args:
        contraction: The contraction to expand.
        suffix_token: The token containing the contraction suffix
            (e.g., "'s", "n't").
        doc: The spaCy `Doc` containing the contraction.

    Returns:
        tuple[str, int]: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The index where the next search should begin.
    """
    original_end_char_idx = span.end_char

    expansion_strategies = [
        handle_d,
        handle_gotta,
        handle_negation,
        handle_s,
        handle_wanna,
        handle_whatcha,
    ]

    for strategy in expansion_strategies:
        result = strategy(span)
        if result is not None:
            expansion, end_idx = result
            return expansion, end_idx

    return contraction, original_end_char_idx


def _expand_idiomatic_phrases(phrase: str) -> str:
    """
    Expand multi-word idiomatic phrases before expanding standard
    contractions.

    Args:
        phrase: The idiomatic phrase to expand.

    Returns:
        str: The expanded phrase.
    """
    idiom_map = EnContractionExpansion.get_idiomatic_map()

    def _replace_idiom(match: re.Match[str]) -> str:
        original_phrase = match.group(0)
        straight_match = curly_to_straight(original_phrase).lower()
        expanded_text = idiom_map.get(straight_match, original_phrase)
        return apply_expansion_casing(original_phrase, expanded_text)

    return EnWarpingPatterns.get_idiomatic_phrases().sub(
        _replace_idiom, phrase
    )


def _expand_unambiguous_contraction(
    contraction: str,
    contractions_map: dict[str, str]
) -> str:
    """
    Replace an unambiguous contraction with its expanded version using
    the contractions map.

    Args:
        contraction: The contraction to expand.

    Returns:
        str: The expanded contraction.
    """
    straight_contraction: str = curly_to_straight(contraction).lower()
    expanded_contraction: str = contractions_map.get(
        straight_contraction, contraction
    )
    return apply_expansion_casing(contraction, expanded_contraction)


class EnglishProvider(LanguageProvider):
    """English language rules for text warping."""

    @property
    def absolute_casings_map(self) -> Mapping[str, str]:
        """Mapping for absolute entity casing."""
        return EnEntityCasing.get_absolute_map()

    @property
    def apostrophe_in_word_pattern(self) -> re.Pattern[str]:
        """
        Regular expression for matching apostrophes within words or
        elisions.
        """
        return EnWarpingPatterns.get_apostrophe_in_word()

    @property
    def base_verb_tags(self) -> frozenset[str]:
        """Fine-grained parts-of-speech tags for base verb forms."""
        return BASE_VERB_TAGS

    @property
    def contextual_casings_map(self) -> Mapping[
        str, tuple['EntityCasingContext', ...]
    ]:
        """Mapping for contextual entity casing."""
        return EnEntityCasing.get_contextual_map()

    @property
    def have_auxiliaries(self) -> frozenset[str]:
        """Auxiliary verbs forms of "have"."""
        return HAVE_AUXILIARIES

    @property
    def noun_phrase_tags(self) -> frozenset[str]:
        """
        Fine-grained parts-of-speech tags for the first word of a noun
        phrase.
        """
        return NOUN_PHRASE_TAGS

    @property
    def participle_tags(self) -> frozenset[str]:
        """
        Fine-grained parts-of-speech tags for past tense and past
        participle verb forms. (Fine-grained tags used to distinguish
        verb tense.)
        """
        return PARTICIPLE_TAGS

    @property
    def singular_noun_tags(self) -> frozenset[str]:
        """
        Fine-grained parts-of-speech tags for singular nouns and proper
        nouns.
        """
        return SINGULAR_NOUN_TAGS

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
        return THIRD_PERSON_SINGULAR_PRONOUNS

    @property
    def title_case_tag_exceptions(self) -> frozenset[str]:
        """
        Fine-grained parts-of-speech tag exceptions for title case
        capitalization. (Fine-grained tags used to distinguish articles
        from possessives.)
        """
        return TITLE_CASE_TAG_EXCEPTIONS

    @property
    def wh_words(self) -> frozenset[str]:
        """Wh-words that start questions."""
        return WH_WORDS

    def cardinal_to_ordinal(self, text: str) -> str:
        """
        Convert cardinal numbers in a given string to ordinal numbers.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return EnWarpingPatterns.get_cardinal().sub(_replace_cardinal, text)

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
        return en_case_from_string(
            word, lowercase_by_default, preserve_mixed_case
        )

    def expand_contractions(self, doc: Doc) -> str:
        """
        Expand all contractions in a given spaCy `Doc`.

        Args:
            doc: A spaCy `Doc`.

        Returns:
            str: The converted `Doc` text.
        """
        text_with_idioms_expanded = _expand_idiomatic_phrases(doc.text)

        if text_with_idioms_expanded != doc.text:
            from textwarp._lib.nlp import process_as_doc
            doc = process_as_doc(text_with_idioms_expanded)

        matches = list(EnWarpingPatterns.get_contraction().finditer(doc.text))
        if not matches:
            return doc.text

        expanded_parts: list[str] = []
        last_idx = 0
        skip_until_idx = -1

        for match in matches:
            start_idx, end_idx = match.span()

            if start_idx < skip_until_idx:
                continue

            expanded_parts.append(doc.text[last_idx:start_idx])
            contraction: str = match.group(0)

            is_negation: bool = bool(
                EnWarpingPatterns.get_n_t_suffix().search(contraction)
            )
            is_ambiguous: bool = bool(
                EnWarpingPatterns.get_ambiguous_contraction().fullmatch(
                    contraction
                )
            )

            if is_negation or is_ambiguous:
                span: Span | None = doc.char_span(start_idx, end_idx)
                if span:
                    expanded_text: str
                    new_end_idx: int

                    expanded_text, new_end_idx = _expand_ambiguous_contraction(
                        contraction, span
                    )
                    expanded_parts.append(expanded_text)
                    last_idx = new_end_idx
                    skip_until_idx = new_end_idx
                    continue

            cased_expansion: str = _expand_unambiguous_contraction(
                contraction,
                EnContractionExpansion.get_unambiguous_map()
            )

            expanded_parts.append(cased_expansion)
            last_idx = end_idx

        expanded_parts.append(doc.text[last_idx:])
        return ''.join(expanded_parts)

    def ordinal_to_cardinal(self, text: str) -> str:
        """
        Convert ordinal numbers in a given string to cardinal numbers.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return EnWarpingPatterns.get_ordinal().sub(_replace_ordinal, text)

    @property
    def punct_inside_pattern(self) -> re.Pattern[str]:
        """
        Regular expression for matching punctuation inside quotation
        marks.
        """
        return EnWarpingPatterns.get_punct_inside()

    @property
    def punct_outside_pattern(self) -> re.Pattern[str]:
        """
        Regular expression for matching punctuation outside quotation
        marks.
        """
        return EnWarpingPatterns.get_punct_outside()

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
        return (
            text.lower() in EnTokenCasing.get_lowercase_particles()
            or bool(
                EnWarpingPatterns.get_contraction_suffixes_pattern()
                .fullmatch(text)
            )
        )
