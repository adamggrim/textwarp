"""Functions for loading universal encoding data."""

import importlib.resources
import json
from functools import lru_cache
from types import MappingProxyType
from typing import Mapping, cast
from pathlib import Path

from textwarp._core.types import JSONType

__all__ = ['get_morse_map', 'get_morse_reversed_map']


def _load_universal(relative_path: str | Path) -> JSONType:
    pkg_files = importlib.resources.files(__package__)
    resource = pkg_files.joinpath('data', *Path(relative_path).parts)
    return cast(JSONType, json.loads(resource.read_text(encoding='utf-8')))


@lru_cache(maxsize=1)
def get_morse_map() -> Mapping[str, str]:
    """Get a cached mapping of characters to Morse code."""
    return MappingProxyType(cast(dict[str, str], _load_universal(
        'morse_map.json'
    )))


@lru_cache(maxsize=1)
def get_morse_reversed_map() -> Mapping[str, str]:
    """Get a cached mapping of Morse code to characters."""
    return MappingProxyType({
        value: key for key, value in get_morse_map().items()
    })
