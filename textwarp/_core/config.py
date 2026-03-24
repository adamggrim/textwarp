"""A configuration module handling lazy loading of JSON data."""

import importlib.resources
import json
from functools import lru_cache
from types import MappingProxyType
from typing import Mapping, cast
from pathlib import Path

from textwarp._core.types import JSONType

__all__ = ['Encoding']


def _load_universal(relative_path: str | Path) -> JSONType:
    """Load JSON content for universal, non-language-specific data."""
    pkg_files = importlib.resources.files(__package__)
    resource = pkg_files.joinpath('data', *Path(relative_path).parts)
    return cast(JSONType, json.loads(resource.read_text(encoding='utf-8')))


class Encoding:
    """A namespace for encoding and decoding translation data."""

    @staticmethod
    @lru_cache(maxsize=1)
    def get_morse_map() -> Mapping[str, str]:
        return MappingProxyType(cast(dict[str, str], _load_universal(
            'morse_map.json'
        )))

    @staticmethod
    @lru_cache(maxsize=1)
    def get_morse_reversed_map() -> Mapping[str, str]:
        return MappingProxyType({
            value: key for key, value in Encoding.get_morse_map().items()
        })
