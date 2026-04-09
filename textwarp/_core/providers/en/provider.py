"""English-specific `LanguageProvider` implementation."""

from __future__ import annotations

from typing import Mapping, TYPE_CHECKING

import regex as re

if TYPE_CHECKING:
    from spacy.tokens import Doc, Span
    from textwarp._core.types import EntityCasingContext

from textwarp._core.providers.base import LanguageProvider
from textwarp._core.providers import en
from textwarp._lib.contractions import apply_expansion_casing
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
        span: The spaCy `Span` containing the contraction.

    Returns:
        tuple[str, int]: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The index where the next search should begin.
    """
    original_end_char_idx = span.end_char

    expansion_strategies = [
        en.handlers.handle_d,
        en.handlers.handle_gotta,
        en.handlers.handle_negation,
        en.handlers.handle_s,
        en.handlers.handle_wanna,
        en.handlers.handle_whatcha,
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
    idiom_map = en.data.contraction_expansion.get_idiomatic_map()

    def _replace_idiom(match: re.Match[str]) -> str:
        original_phrase = match.group(0)
        straight_match = curly_to_straight(original_phrase).lower()
        expanded_text = idiom_map.get(straight_match, original_phrase)
        return apply_expansion_casing(original_phrase, expanded_text)

    return en.patterns.get_idiomatic_phrases().sub(
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
        return en.patterns.get_cardinal().sub(_replace_cardinal, text)

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
        text_with_idioms_expanded = _expand_idiomatic_phrases(doc.text)

        if text_with_idioms_expanded != doc.text:
            from textwarp._lib.nlp import process_as_doc
            doc = process_as_doc(text_with_idioms_expanded)

        matches = list(
            en.patterns.get_contraction().finditer(doc.text)
        )
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
                en.patterns.get_n_t_suffix().search(contraction)
            )
            is_ambiguous: bool = bool(
                en.patterns.get_ambiguous_contraction().fullmatch(
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
                en.data.contraction_expansion.get_unambiguous_map()
            )

            expanded_parts.append(cased_expansion)
            last_idx = end_idx

        expanded_parts.append(doc.text[last_idx:])
        return ''.join(expanded_parts)

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
        return en.patterns.get_ordinal().sub(_replace_ordinal, text)

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
        return (
            text.lower() in en.data.token_casing.get_lowercase_particles()
            or bool(
                en.patterns.get_contraction_suffixes_pattern()
                .fullmatch(text)
            )
        )

    def straight_to_curly(self, text: str) -> str:
        """
        Convert straight quotes in a given string to curly quotes.

        Args:
            text: The string to convert.

        Returns:
            str: The converted string.
        """
        return en.punctuation.straight_to_curly(text)
