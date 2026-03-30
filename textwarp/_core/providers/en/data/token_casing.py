"""Functions for loading English token casing rules."""

from functools import lru_cache
from pathlib import Path
from typing import cast

from textwarp._core.providers.en.data.loader import load_data

__all__ = ['get_lowercase_particles']


@lru_cache(maxsize=1)
def get_lowercase_particles() -> frozenset[str]:
    """Get a cached `frozenset` of lowercase particles."""
    return frozenset(
        cast(
            list[str],
            load_data(
                Path('entity_casing') / 'lowercase_particles.json'
            )
        )
    )
