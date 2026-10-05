"""
Functions for parsing Markdown and transforming Abstract Syntax Trees
(ASTs).
"""

import contextvars
import threading
from collections.abc import Callable, Generator
from contextlib import contextmanager
from typing import Any

import marko
from marko.md_renderer import MarkdownRenderer

__all__ = ['process_markdown', 'strip_markdown']

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


class _ThreadLocalMarkdownPool(threading.local):
    """Thread-local storage for a reusable Markdown parser instance."""

    def __init__(self) -> None:
        self.parser: marko.Markdown | None = None
        self.in_use: bool = False


_pool = _ThreadLocalMarkdownPool()


@contextmanager
def _checkout_parser(
    transform_func: Callable[[str], str]
) -> Generator[marko.Markdown, None, None]:
    """
    Provide a thread-local `marko.Markdown` instance, or a temporary
    instance if the thread's parser is already active in a nested call.
    """
    token = _active_transform.set(transform_func)
    if _pool.in_use:
        try:
            yield marko.Markdown(renderer=_TextwarpRenderer)
        finally:
            _active_transform.reset(token)
        return

    if _pool.parser is None:
        _pool.parser = marko.Markdown(renderer=_TextwarpRenderer)

    _pool.in_use = True
    try:
        yield _pool.parser
    finally:
        _pool.in_use = False
        _active_transform.reset(token)


def process_markdown(text: str, transform_func: Callable[[str], str]) -> str:
    """
    Parse a Markdown string into an Abstract Syntax Tree (AST), apply a
    transformation function and translate the string back into Markdown.
    """
    with _checkout_parser(transform_func) as parser:
        return parser.convert(text)


def strip_markdown(text: str) -> str:
    """Parse a Markdown string and extract only the plain text."""
    extracted_text: list[str] = []

    def intercept_text(chunk: str) -> str:
        extracted_text.append(chunk)
        # Return `chunk` to prevent renderer crashes for empty strings.
        return chunk

    process_markdown(text, intercept_text)
    return ''.join(extracted_text)
