"""Namespaces for loading English-specific data."""

import importlib.resources
import json
from pathlib import Path
from typing import cast

from textwarp._core.types import JSONType

__all__ = [
    'contraction_expansion',
    'entity_casing',
    'load_data',
    'punctuation',
    'string_casing',
    'token_casing'
]


def load_data(relative_path: str | Path) -> JSONType:
    """Load JSON content from the English data directory.

    Args:
        relative_path: The file path relative to the data directory.

    Returns:
        The parsed JSON content.
    """
    pkg_files = importlib.resources.files(__package__.split('.')[0])
    parts = ('en',) + Path(relative_path).parts
    resource = pkg_files.joinpath('_core', 'data', *parts)
    return cast(
        JSONType,
        json.loads(resource.read_text(encoding='utf-8'))
    )


from textwarp._core.providers.en.data import (
    contraction_expansion,
    entity_casing,
    punctuation,
    string_casing,
    token_casing
)
