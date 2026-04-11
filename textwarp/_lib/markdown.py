"""
Functions for parsing Markdown and transforming Markdown Abstract Syntax
Trees (ASTs).
"""

from typing import Callable
import marko
from marko.md_renderer import MarkdownRenderer

__all__ = ['process_markdown']


def process_markdown(text: str, transform_func: Callable[[str], str]) -> str:
    """
    Parse a Markdown string into an Abstract Syntax Tree (AST), apply a
    transformation function to the raw text nodes and translate it back
    into Markdown.a

    Args:
        text: The Markdown string to process.
        transform_func: The function to apply to the text nodes.

    Returns:
        str: The transformed Markdown string.
    """

    class TextwarpRenderer(MarkdownRenderer):
        """A custom renderer that intercepts raw text nodes."""
        def render_raw_text(self, element) -> str:
            """Apply the transformation function to raw text nodes."""
            return transform_func(element.children)

    markdown = marko.Markdown(renderer=TextwarpRenderer)
    return markdown.convert(text)
