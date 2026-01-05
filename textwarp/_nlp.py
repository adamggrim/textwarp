"""Function for lazy loading of the spaCy model."""

from typing import Optional

import spacy

from ._ui import print_wrapped

_nlp_instance: Optional[spacy.language.Language] = None

def get_nlp():
    """
    Returns the loaded spaCy model instance, downloading it if not
    found.

    Returns:
        spacy.language.Language: The loaded spaCy model instance.
    """
    global _nlp_instance
    if _nlp_instance is None:
        model_name = 'en_core_web_trf'
        try:
            _nlp_instance = spacy.load(model_name)
        except OSError:
            print_wrapped(f"Downloading spaCy model '{model_name}'...")
            spacy.cli.download(model_name)
            _nlp_instance = spacy.load(model_name)

    return _nlp_instance
