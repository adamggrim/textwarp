"""Functions for loading English entity casing rules."""

from functools import lru_cache
from pathlib import Path
from types import MappingProxyType
from typing import Final, Mapping, cast

from textwarp._core.utils import load_json_data
from textwarp._core.types import EntityCasingContext

DIR: Final = Path('entity_casing')


@lru_cache(maxsize=1)
def get_absolute_map() -> Mapping[str, str]:
    """Get a cached map for absolute entity casing."""
    return MappingProxyType(
        cast(
            dict[str, str],
            load_json_data(DIR / 'absolute_casings_map.json', locale='en')
        )
    )


@lru_cache(maxsize=1)
def get_contextual_map() -> Mapping[str, tuple[EntityCasingContext, ...]]:
    """Get a cached map for contextual entity casing."""
    raw_map = cast(
        dict[str, list[EntityCasingContext]],
        load_json_data(DIR / 'contextual_casings_map.json', locale='en')
    )
    return MappingProxyType(
        {key: tuple(contexts) for key, contexts in raw_map.items()}
    )


@lru_cache(maxsize=1)
def get_contraction_suffixes() -> frozenset[str]:
    """Get a cached frozenset of allowed contraction suffixes."""
    return frozenset(
        cast(
            list[str],
            load_json_data(DIR / 'contraction_suffixes.json', locale='en')
        )
    )
