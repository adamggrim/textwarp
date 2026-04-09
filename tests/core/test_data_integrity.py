import json
from pathlib import Path

import pytest

from textwarp._core.providers.en.data.entity_casing import get_absolute_map
from textwarp._core.providers.en.data.contraction_expansion import (
    get_unambiguous_map,
    get_ambiguous_map
)

DATA_DIR = Path(__file__).parents[4] / 'textwarp' / '_core' / 'data'


def get_json_files():
    """Helper function to find all JSON files in the data directory."""
    return list(DATA_DIR.rglob('*.json'))


@pytest.mark.parametrize('json_file', get_json_files())
def test_json_files_are_valid_and_not_empty(json_file):
    """Verify that every JSON file is valid syntax and has content."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        assert data is not None
        assert len(data) > 0


def test_absolute_casings_keys_are_lowercase():
    """Verify that keys in casing maps are lowercase for lookups."""
    casing_map = get_absolute_map()

    for key in casing_map.keys():
        assert key == key.lower(), (
            f"Key '{key}' in `absolute_casings_map` must be lowercase."
        )

def test_no_duplicate_contractions():
    """Ensure expansion maps do not have overlapping keys."""
    unambig = set(get_unambiguous_map().keys())
    ambig = set(get_ambiguous_map())

    overlap = unambig.intersection(ambig)
    assert not overlap, f'Contractions found in both maps: {overlap}'
