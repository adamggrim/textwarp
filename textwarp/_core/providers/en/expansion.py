"""English-specific logic for expanding contractions."""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re

if TYPE_CHECKING:
    from spacy.tokens import Doc, Span

from textwarp._core.providers import en
from textwarp._lib.contractions import apply_expansion_casing
from textwarp._lib.punctuation import curly_to_straight

__all__ = ['expand_contractions']


def _expand_ambiguous_contraction(
    contraction: str,
    span: Span
) -> tuple[str, int]:
    """
    Replace an ambiguous contraction with its expanded version.

    Args:
        contraction: The contraction to expand.
        span: The spaCy `Span` containing the contraction.

    Returns:
        tuple[str, int]: A tuple containing:
            1. The expanded version of the matched contraction.
            2. The end index of the expanded contraction.
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
        phrase: The input text to expand.

    Returns:
        str: The text with expanded idiomatic phrases.
    """
    idiom_map = en.data.contraction_expansion.get_idiomatic_map()

    def _replace_idiom(match: re.Match[str]) -> str:
        """Replace a matched idiomatic phrase with its expansion."""
        original_phrase = match.group(0)
        straight_match = curly_to_straight(original_phrase).lower()
        expanded_text = idiom_map.get(straight_match, original_phrase)

        apostrophe_match = en.patterns.get_any_apostrophe().search(
            original_phrase
        )
        if apostrophe_match:
            expanded_text = en.patterns.get_any_apostrophe().sub(
                apostrophe_match.group(0), expanded_text
            )

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
        contractions_map: A mapping of each unambiguous contraction to
            its expansion.

    Returns:
        str: The expanded contraction.
    """
    straight_contraction: str = curly_to_straight(contraction).lower()
    expanded_contraction: str = contractions_map.get(
        straight_contraction, contraction
    )
    return apply_expansion_casing(contraction, expanded_contraction)


def expand_contractions(doc: Doc) -> str:
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
