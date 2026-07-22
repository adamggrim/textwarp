"""
Functions for parsing Markdown and transforming Markdown Abstract Syntax
Trees (ASTs).
"""

from typing import Any, Callable

import marko
from marko.md_renderer import MarkdownRenderer

__all__ = ['process_markdown', 'strip_markdown']


class _TextwarpRenderer(MarkdownRenderer):
    """A custom renderer that intercepts raw text nodes."""

    handler_func: Callable[[str], str] | None = None

    def render_raw_text(self, element: Any) -> str:
        """Apply the transformation function to raw text nodes."""
        if _TextwarpRenderer.handler_func is not None:
            return _TextwarpRenderer.handler_func(element.children)
        return element.children


# Initialize the parser once globally for improved performance.
_markdown_parser = marko.Markdown(renderer=_TextwarpRenderer)


def process_markdown(text: str, transform_func: Callable[[str], str]) -> str:
    """
    Parse a Markdown string into an Abstract Syntax Tree (AST), apply a
    transformation function and translate the string back into Markdown.
    """
    _TextwarpRenderer.handler_func = transform_func
    try:
        return _markdown_parser.convert(text)
    finally:
        _TextwarpRenderer.handler_func = None


def strip_markdown(text: str) -> str:
    """Parse a Markdown string and extract only the plain text."""
    extracted_text: list[str] = []

    def intercept_text(chunk: str) -> str:
        extracted_text.append(chunk)
        return ''

    process_markdown(text, intercept_text)
    return ''.join(extracted_text)
