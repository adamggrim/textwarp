"""
Functions for extracting words and processing text as a spaCy ``Doc``.
"""

from spacy.tokens import Doc

from .._constants import POS_WORD_TAGS
from .._nlp import get_nlp

__all__ = [
    'extract_words_from_doc',
    'process_as_doc'
]


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
    if isinstance(content, Doc):
        return content
    nlp = get_nlp(model_size)
    return nlp(content)
