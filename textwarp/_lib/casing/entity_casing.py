"""Functions for spaCy-based entity capitalization."""

from __future__ import annotations

from typing import TYPE_CHECKING

import regex as re
if TYPE_CHECKING:
    from spacy.tokens import Doc, Span

from textwarp._core.config import EntityCasing
from textwarp._core.constants.nlp import PROPER_NOUN_ENTITIES
from textwarp._core.types import EntityCasingContext

__all__ = [
    'map_all_entities'
]


def _case_contextual_entity(
    span: Span,
    key: str
) -> str | None:
    """
    Determine the casing for a contextual entity based on parts-of-
    speech sequences and ngrams.

    Args:
        span: The spaCy ``Span`` to case.
        key: The key to look up in the context map.

    Returns:
        str | None: The contextual casing; otherwise ``None``.
    """
    contextual_entities_map = EntityCasing.get_contextual_map()
    contexts: list[EntityCasingContext] = contextual_entities_map.get(
        key, []
    )

    current_pos_seq = [token.pos_ for token in span]

    for context in contexts:
        context_pos_seqs = context.get('pos_sequences', [])
        for context_pos_seq in context_pos_seqs:
            if current_pos_seq == context_pos_seq:
                return context['casing']

        context_ngrams = context.get('ngrams', [])
        if context_ngrams:
            context_window = context.get('context_window', 4)
            if _check_for_ngrams(span, context_ngrams, context_window):
                return context['casing']

        if not context_pos_seqs and not context_ngrams:
            return context['casing']

    return None


def _check_for_ngrams(
    span: Span,
    ngrams: list[str],
    context_window: int
) -> bool:
    """
    Check if any of a given list of ngrams are present around a
    specific index in the Doc.

    Args:
        span: The spaCy ``Span`` to check.
        ngrams: A list of ngrams to check for.
        context_window: The number of tokens around the ``Span`` to
            check.

    Returns:
        bool: ``True`` if any ngram is found, otherwise ``False``.
    """
    doc = span.doc

    start_idx = max(0, span.start - context_window)
    end_idx = min(len(doc), span.end + context_window)

    # The text of the window around the entity.
    left_context = doc[start_idx : span.start].text.lower()
    right_context = doc[span.end : end_idx].text.lower()

    for ngram in ngrams:
        pattern = r'(?<!\w)' + re.escape(ngram.lower()) + r'(?!\w)'
        if (re.search(pattern, left_context) or
            re.search(pattern, right_context)):
            return True

    return False


def _map_custom_entities(doc: Doc) -> dict[int, tuple[Span, int, str]]:
    """
    Map entities in a spaCy ``Doc`` to their correct contextual casing.

    Args:
        doc: The spaCy ``Doc`` to convert.

    Returns:
        dict[int, tuple[Span, int, str]]: A dictionary where each key is
            an entity's start token index and each value is a tuple
            containing:
                1. The entity's spaCy ``Span`` object.
                2. The entity's end token index.
                3. The cased entity.
    """
    custom_entities_map: dict[int, tuple[Span, int, str]] = {}

    absolute_entities_map = EntityCasing.get_absolute_map()
    contextual_entities_map = EntityCasing.get_contextual_map()

    all_keys: set[str] = (
        absolute_entities_map.keys()
        | contextual_entities_map.keys()
    )

    # Sort words by length in descending order to prioritize longer
    # matches.
    sorted_keys = sorted(all_keys, key=len, reverse=True)
    keys_pattern = re.compile(
        rf'(?<!\w)(?:{"|".join(re.escape(key) for key in sorted_keys)})(?!\w)',
        re.IGNORECASE
    )

    for match in keys_pattern.finditer(doc.text):
        start_char, end_char = match.span()
        span = doc.char_span(start_char, end_char)

        # Skip the match if the ``Span`` does not align with a token.
        if span is None:
            continue

        key = match.group(0).lower()
        cased_text: str | None = None

        if key in absolute_entities_map:
            cased_text = absolute_entities_map[key]
        elif key in contextual_entities_map:
            cased_text = _case_contextual_entity(span, key)

        if cased_text:
            custom_entities_map[span.start] = (span, span.end, cased_text)

    return custom_entities_map


def _map_model_entities(doc: Doc) -> dict[int, tuple[Span, int, None]]:
    """
    Map model entities in a spaCy ``Doc``. These entities are detected
    by the underlying spaCy NLP model.

    Args:
        doc: The spaCy ``Doc`` to convert.

    Returns:
        dict[int, tuple[Span, int, None]]: A dictionary where each key
            is an entity's start token index and each value is a tuple
            containing:
                1. The entity's spaCy ``Span`` object.
                2. The entity's end token index.
                3. ``None`` (no forced casing).
    """
    return {
        ent.start: (ent, ent.end, None) for ent in doc.ents
        if ent.label_ in PROPER_NOUN_ENTITIES
    }


def map_all_entities(doc: Doc) -> dict[int, tuple[Span, int, str | None]]:
    """
    Create a prioritized map of all entities (absolute > contextual > model).

    Args:
        doc: The spaCy ``Doc`` to convert.

    Returns:
        dict[int, tuple[str | Span, int, None]]: A dictionary where each
            key is an entity's start token index and each value is a
            tuple containing:
                1. The entity's spaCy ``Span`` object.
                2. The entity's end token index.
                3. The cased entity; otherwise ``None``.
    """
    custom_map = _map_custom_entities(doc)

    consumed_idxs = set()
    for span, _, _ in custom_map.values():
        consumed_idxs.update(range(span.start, span.end))

    standard_map = _map_model_entities(doc)

    combined_map: dict[int, tuple[Span, int, str| None]] = dict(custom_map)

    for start_idx, (span, end_idx, text) in standard_map.items():
        span_idxs = set(range(span.start, span.end))
        # Only add standard indices if they don't overlap with custom
        # indices.
        if span_idxs.isdisjoint(consumed_idxs):
            combined_map[start_idx] = (span, end_idx, text)

    return combined_map
