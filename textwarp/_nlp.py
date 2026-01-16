"""Function for lazy loading of the spaCy model."""

from typing import (
    Literal,
    Optional
)

import spacy

from ._ui import print_wrapped

ModelSize = Literal['small', 'large']
_nlp_instances: dict[str, spacy.language.Language] = {}


def get_nlp(size: ModelSize = 'small'):
    """
    Returns the loaded spaCy model instance, downloading it if not
    found.

    Args:
        size: The size of the spaCy model to load. Can be either
            "small" (speed) or "large" (accuracy).

    Returns:
        spacy.language.Language: The loaded spaCy model instance.
    """
    model_map = {
        'small': 'en_core_web_sm',
        'large': 'en_core_web_trf'
    }

    target_model = model_map.get(size, 'en_core_web_sm')

    if target_model not in _nlp_instances:
        try:
            _nlp_instances[target_model] = spacy.load(target_model)
        except OSError:
            print_wrapped(f"Downloading spaCy model '{target_model}'...")
            spacy.cli.download(target_model)
            _nlp_instances[target_model] = spacy.load(target_model)

    return _nlp_instances[target_model]
