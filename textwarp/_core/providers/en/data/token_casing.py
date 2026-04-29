"""Functions for loading English token casing rules."""

from functools import cache
from pathlib import Path

from textwarp._core.utils import load_json_data

__all__ = ['get_lowercase_particles']


@cache
def get_lowercase_particles() -> frozenset[str]:
    """Get a cached `frozenset` of lowercase particles."""
    return frozenset(
        cast(
            list[str],
            load_json_data(
                Path('token_casing') / 'lowercase_particles.json', locale='en'
            )
        )
    )
