import importlib.resources
import json

import pytest

from textwarp._core.providers.en.data.entity_casing import get_absolute_map
from textwarp._core.providers.en.data.contraction_expansion import (
    get_ambiguous_map,
    get_unambiguous_map
)

def get_json_files():
    """Helper function to find all JSON files in the data directory."""
    data_dir = importlib.resources.files('textwarp').joinpath('_core', 'data')

    def _find_json(directory):
        for item in directory.iterdir():
            if item.is_dir():
                yield from _find_json(item)
            elif item.name.endswith('.json'):
                yield item

    return list(_find_json(data_dir))


def test_absolute_casings_keys_are_lowercase():
    """Verify that keys in casing maps are lowercase for lookups."""
    casing_map = get_absolute_map()

    for key in casing_map.keys():
        assert key == key.lower(), (
            f"Key '{key}' in `absolute_casings_map` must be lowercase."
        )


@pytest.mark.parametrize('json_file', get_json_files())
def test_json_files_are_valid_and_not_empty(json_file):
    """Verify that every JSON file is valid syntax and has content."""
    data = json.loads(json_file.read_text(encoding='utf-8'))
    assert data is not None
    assert len(data) > 0


def test_no_duplicate_contractions():
    """Ensure expansion maps do not have overlapping keys."""
    unambig = set(get_unambiguous_map().keys())
    ambig = set(get_ambiguous_map())

    overlap = unambig.intersection(ambig)
    assert not overlap, f'Contractions found in both maps: {overlap}'
