"""Functions for lazy spaCy loading and text processing."""

from __future__ import annotations

import gettext
from functools import lru_cache
from types import ModuleType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import spacy.language
    from spacy.tokens import Doc

from textwarp._core.constants.nlp import POS_WORD_TAGS
from textwarp._core.context import ctx
from textwarp._core.enums import ModelPriority

_ = gettext.gettext

__all__ = ['extract_words_from_doc', 'process_as_doc']


@lru_cache(maxsize=1)
def _load_spacy() -> ModuleType:
    """
    Lazily load and cache the spaCy module.

    Returns:
        ModuleType: The loaded spaCy module.
    """
    import spacy
    return spacy


@lru_cache(maxsize=None)
def _load_spacy_model(model_name: str) -> spacy.language.Language:
    """
    Load a spaCy model by name.

    Args:
        model_name: The name of the spaCy model to load.

    Returns:
        spacy.language.Language: The loaded spaCy model.
    """
    spacy = _load_spacy()
    return spacy.load(model_name)


def _get_nlp(
    model_priority: ModelPriority = ModelPriority.SPEED
) -> spacy.language.Language:
    """
    Returns the best available spaCy model instance based on speed or
    accuracy for the active language locale.

    Args:
        model_priority: The spaCy model to prioritize. Can be either
            `SPEED` or `ACCURACY`. Defaults to `SPEED`.

    Returns:
        spacy.language.Language: The loaded spaCy model instance.
    """
    spacy = _load_spacy()

    locale_models = ctx.provider.spacy_models

    if model_priority == ModelPriority.ACCURACY:
        model_ranking = locale_models[::-1]
    else:
        model_ranking = locale_models

    for model_name in model_ranking:
        if spacy.util.is_package(model_name):
            try:
                return _load_spacy_model(model_name)
            except ImportError:
                # Occurs when a transformer model is installed but
                # `spacy-transformers` is missing.
                continue

    installed_models = spacy.util.get_installed_models()
    locale_prefix = f'{ctx.locale}_'
    for model_name in installed_models:
        if model_name.startswith(locale_prefix):
            return _load_spacy_model(model_name)

    priority_model_name = model_ranking[0]
    message = _(
        'Error: No {locale} spaCy models found. Run: python -m spacy download '
        '{model}'
    ).format(
        locale=ctx.locale.upper(),
        model=priority_model_name
    )
    raise RuntimeError(message)


def extract_words_from_doc(doc: Doc) -> list[str]:
    """
    Extract a list of word strings from a spaCy `Doc`.

    Args:
        doc: The spaCy `Doc` to analyze.

    Returns:
        list[str]: The list of word strings from the `Doc`.
    """
    return [
        token.lower_
        for token in doc
        if token.pos_ in POS_WORD_TAGS
    ]


def process_as_doc(
    content: str | Doc,
    model_priority: ModelPriority = ModelPriority.SPEED,
    disable: list[str] | None = None
) -> Doc:
    """
    Process the input as a spaCy `Doc`.

    Args:
        content: The string or `Doc` to process.
        model_priority: The spaCy model to prioritize. Can be either
            `SPEED` or `ACCURACY`. Defaults to `SPEED`.
        disable: A list of pipeline components to disable during
            processing. Defaults to `None`.

    Returns:
        Doc: The processed spaCy `Doc`.
    """
    if not isinstance(content, str):
        return content

    nlp = _get_nlp(model_priority)
    if disable:
        with nlp.select_pipes(disable=disable):
            return nlp(content)

    return nlp(content)
