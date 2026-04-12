"""
Functions for parsing Markdown and transforming Markdown Abstract Syntax
Trees (ASTs).
"""

from typing import Callable
import marko
from marko.md_renderer import MarkdownRenderer

__all__ = ['_apply_func_to_markdown', 'strip_markdown']


def _apply_func_to_markdown(
    text: str,
    handler_func: Callable[[str], str]
) -> str:
    """
    Parse a Markdown string into an Abstract Syntax Tree (AST), apply a
    handler function and translate the string back into Markdown.

    Args:
        text: The Markdown string to process.
        handler_func: The function to apply to the text nodes.

    Returns:
        str: The transformed Markdown string.
    """

    class TextwarpRenderer(MarkdownRenderer):
        """A custom renderer that intercepts raw text nodes."""
        def render_raw_text(self, element) -> str:
            """Apply the transformation function to raw text nodes."""
            return handler_func(element.children)

    markdown = marko.Markdown(renderer=TextwarpRenderer)
    return markdown.convert(text)


def strip_markdown(text: str) -> str:
    """
    Parse a Markdown string and extract only the plain text.

    Args:
        text: The Markdown string to process.

    Returns:
        str: The extracted plain text.
    """
    extracted_text: list[str] = []

    def intercept_text(chunk: str) -> str:
        extracted_text.append(chunk)
        return ''

    _apply_func_to_markdown(text, intercept_text)
    return ''.join(extracted_text)


def process_markdown(text: str, transform_func: Callable[[str], str]) -> str:
    """
    Parse a Markdown string into an Abstract Syntax Tree (AST), apply a
    transformation function and translate the string back into Markdown.

    Args:
        text: The Markdown string to process.
        transform_func: The function to apply to the text nodes.

    Returns:
        str: The transformed Markdown string.
    """
    return _apply_func_to_markdown(text, transform_func)
