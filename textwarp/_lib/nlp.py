"""Functions for lazy spaCy loading and text processing."""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import spacy.language
    from spacy.tokens import Doc

from textwarp._cli.ui import print_wrapped
from textwarp._core.constants.nlp import POS_WORD_TAGS

ModelPriority = Literal['accuracy', 'speed']
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


def process_as_doc(content: str | Doc, model_priority: str = 'speed') -> Doc:
    """
    Process the input as a spaCy ``Doc``.

    Args:
        content: The string or ``Doc`` to process.
        model_priority: The size of the spaCy model to use.

    Returns:
        Doc: The processed spaCy ``Doc``.
    """
    if not isinstance(content, str):
        return content
    nlp = get_nlp(model_priority)
    return nlp(content)


def get_nlp(model_priority: ModelPriority = 'speed') -> spacy.language.Language:
    """
    Returns the best available spaCy model instance based on speed or
    accuracy.

    Args:
        model_priority: The spaCy model priority. Can be either "speed" or
            "accuracy". Defaults to "speed".

    Returns:
        spacy.language.Language: The loaded spaCy model instance.
    """
    import spacy
    import sys

    # Priority is "speed".
    model_priorities = [
        'en_core_web_sm',
        'en_core_web_md',
        'en_core_web_lg',
        'en_core_web_trf'
    ]

    if model_priority == 'accuracy':
        model_priorities = model_priorities[::-1]

    for model_name in model_priorities:
        if spacy.util.is_package(model_name):
            if model_name not in _nlp_instances:
                try:
                    _nlp_instances[model_name] = spacy.load(model_name)
                except ImportError:
                    # Occurs when ``en_core_web_trf`` is installed but
                    # ``spacy-transformers`` is missing.
                    continue
            return _nlp_instances[model_name]

    # Search for any other installed English model.
    installed_models = spacy.util.get_installed_models()
    for model_name in installed_models:
        if model_name.startswith('en_'):
            if model_name not in _nlp_instances:
                _nlp_instances[model_name] = spacy.load(model_name)
            return _nlp_instances[model_name]

    priority_model_name = model_priorities[0]
    print_wrapped('Error: No English spaCy models found.', file=sys.stderr)
    print_wrapped(
        f'Run: python -m spacy download {priority_model_name}', file=sys.stderr
    )
    sys.exit(1)
