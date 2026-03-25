"""Sets used across the package for grouping apostrophe characters."""

from typing import Final

__all__ = ['OPEN_QUOTES']

# Opening quote characters.
OPEN_QUOTES: Final[frozenset[str]] = frozenset({'"', '“', "'", '‘'})
