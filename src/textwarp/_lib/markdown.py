"""
Functions for parsing Markdown and transforming Markdown Abstract Syntax
Trees (ASTs).
"""

import contextvars
from collections.abc import Callable
from typing import Any

import marko
from marko.md_renderer import MarkdownRenderer

__all__ = ['process_markdown', 'strip_markdown']

# Thread-safe context variable for the active transformation function.
_active_transform: contextvars.ContextVar[Callable[[str], str] | None] = (
    contextvars.ContextVar('active_transform', default=None)
)


class _TextwarpRenderer(MarkdownRenderer):
    """A custom renderer that intercepts raw text nodes."""

    def render_raw_text(self, element: Any) -> str:
        """Apply the transformation function to raw text nodes."""
        handler_func = _active_transform.get()
        if handler_func is not None:
            return handler_func(element.children)
        return element.children


_markdown_parser = marko.Markdown(renderer=_TextwarpRenderer)


def process_markdown(text: str, transform_func: Callable[[str], str]) -> str:
    """
    Parse a Markdown string into an Abstract Syntax Tree (AST), apply a
    transformation function and translate the string back into Markdown.
    """
    token = _active_transform.set(transform_func)
    try:
        return _markdown_parser.convert(text)
    finally:
        _active_transform.reset(token)


def strip_markdown(text: str) -> str:
    """Parse a Markdown string and extract only the plain text."""
    extracted_text: list[str] = []

    def intercept_text(chunk: str) -> str:
        extracted_text.append(chunk)
        # Return `chunk` to prevent renderer crashes for empty strings.
        return chunk

    process_markdown(text, intercept_text)
    return ''.join(extracted_text)
