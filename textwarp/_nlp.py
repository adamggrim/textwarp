import spacy
from spacy.cli import download
from spacy.language import Language

from ._ui import print_wrapped


def _load_spacy_model(model_name: str):
    """
    Loads a spaCy model, downloading it if not found.

    Args:
        model_name (str): The name of the spaCy model to load.
    """
    try:
        nlp: Language = spacy.load(model_name)
    except OSError:
        print_wrapped(f"Downloading spaCy model '{model_name}'...")
        download(model_name)
        nlp = spacy.load(model_name)
    return nlp


nlp: Language = _load_spacy_model('en_core_web_trf')
