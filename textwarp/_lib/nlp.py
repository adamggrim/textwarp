"""Functions for lazy spaCy loading and text processing."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import spacy.language
    from spacy.tokens import Doc

from .._core.constants import POS_WORD_TAGS

ModelSize = Literal['small', 'large']
# Use string forward reference to support lazy spaCy loading.
_nlp_instances: dict[str, 'spacy.language.Language'] = {}


def extract_words_from_doc(doc: Doc) -> list[str]:
    """
    Extract a list of word strings from a spaCy ``Doc``.

    Args:
        doc: The spaCy ``Doc`` to analyze.

    Returns:
        list[str]: The list of word strings from the ``Doc``.
    """
    return [
        token.text.lower()
        for token in doc
        if token.pos_ in POS_WORD_TAGS
    ]


def process_as_doc(content: str | Doc, model_size: str = 'small') -> Doc:
    """
    Process the input as a spaCy ``Doc``.

    Args:
        content: The string or ``Doc`` to process.
        model_size: The size of the spaCy model to use.

    Returns:
        Doc: The processed spaCy ``Doc``.
    """
    if not isinstance(content, str):
        return content
    nlp = get_nlp(model_size)
    return nlp(content)


def get_nlp(size: ModelSize = 'small') -> spacy.language.Language:
    """
    Returns the loaded spaCy model instance, downloading it if not
    found.

    Args:
        size: The size of the spaCy model to load. Can be either
            "small" (for speed) or "large" (for accuracy).

    Returns:
        spacy.language.Language: The loaded spaCy model instance.
    """
    import spacy

    model_map = {
        'small': 'en_core_web_sm',
        'large': 'en_core_web_trf'
    }

    target_model = model_map.get(size, 'en_core_web_sm')

    if target_model not in _nlp_instances:
        try:
            _nlp_instances[target_model] = spacy.load(target_model)
        except OSError:
            # Deferred import to avoid circular dependency.
            from .._cli.ui import print_wrapped

            print_wrapped(f"Downloading spaCy model '{target_model}'...")
            spacy.cli.download(target_model)
            _nlp_instances[target_model] = spacy.load(target_model)

    return _nlp_instances[target_model]
