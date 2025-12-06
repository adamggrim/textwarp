from spacy.tokens import Doc

from .._nlp import nlp


def process_as_doc(content: str | Doc) -> Doc:
    """
    Process the input as a spaCy ``Doc``.

    Args:
        content: The string or ``Doc`` to process.

    Returns:
        Doc: The processed spaCy ``Doc``.
    """
    if isinstance(content, Doc):
        return content
    return nlp(content)
