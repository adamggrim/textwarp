"""Functions for cleaning and sanitizing text."""

from html.parser import HTMLParser

from textwarp._core.constants import patterns

__all__ = [
    'strip_html',
    'to_single_spaces'
]


class _HTMLStripper(HTMLParser):
    """
    A subclass of HTMLParser used to strip HTML tags.
    """

    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.strict=False
        self.convert_charrefs=True
        self.text_parts: list[str] = []

    def handle_data(self, d: str) -> None:
        self.text_parts.append(d)

    def get_data(self) -> str:
        return ''.join(self.text_parts)


def strip_html(text: str) -> str:
    """Strip HTML tags from a string."""
    stripper = _HTMLStripper()
    stripper.feed(text)
    return stripper.get_data()


def to_single_spaces(text: str) -> str:
    """
    Convert consecutive spaces to a single space.

    This function preserves leading spaces and tabs.
    """
    return patterns.warping.get_multiple_spaces().sub(' ', text)
