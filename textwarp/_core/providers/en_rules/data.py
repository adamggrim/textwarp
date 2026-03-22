"""English-specific data loading and caching."""

import importlib.resources
import json
from functools import lru_cache
from pathlib import Path
from types import MappingProxyType
from typing import Final, Mapping, cast

from textwarp._core.types import EntityCasingContext, JSONType

__all__ = [
    'EnContractionExpansion',
    'EnEntityCasing',
    'EnPunctuation',
    'EnStringCasing',
    'EnTokenCasing'
]


def _load_en_data(relative_path: str | Path) -> JSONType:
    """Load JSON content from the English (en) data directory.

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


class EnContractionExpansion:
    """Data loader for English contraction expansion rules."""

    DIR: Final = Path('contraction_expansion')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_ambiguous_map() -> tuple[str, ...]:
        """Get a cached tuple of ambiguous contractions."""
        return tuple(
            cast(
                list[str],
                _load_en_data(
                    EnContractionExpansion.DIR / 'ambiguous_contractions.json'
                )
            )
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_common_stateless_participles() -> tuple[str, ...]:
        """Get a cached tuple of common stateless participles."""
        return tuple(
            cast(
                list[str],
                _load_en_data(
                    EnContractionExpansion.DIR
                    / 'common_stateless_participles.json'
                )
            )
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_idiomatic_map() -> Mapping[str, str]:
        """Get a cached mapping of idiomatic phrases."""
        return MappingProxyType(
            cast(
                dict[str, str],
                _load_en_data(
                    EnContractionExpansion.DIR / 'idiomatic_phrases.json'
                )
            )
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_unambiguous_map() -> Mapping[str, str]:
        """Get a cached mapping of unambiguous contractions."""
        return MappingProxyType(
            cast(
                dict[str, str],
                _load_en_data(
                    EnContractionExpansion.DIR
                    / 'unambiguous_contractions_map.json'
                )
            )
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_whatcha_are_words() -> tuple[str, ...]:
        """
        Get a cached tuple of "whatcha" "are" replacement words.
        """
        return tuple(
            cast(
                list[str],
                _load_en_data(
                    EnContractionExpansion.DIR / 'whatcha_are_words.json'
                )
            )
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_whatcha_have_words() -> tuple[str, ...]:
        """
        Get a cached tuple of "whatcha" "have" replacement words.
        """
        return tuple(
            cast(
                list[str],
                _load_en_data(
                    EnContractionExpansion.DIR / 'whatcha_have_words.json'
                )
            )
        )


class EnEntityCasing:
    """Data loader for English entity casing rules."""

    DIR: Final = Path('entity_casing')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_absolute_map() -> Mapping[str, str]:
        """Get a cached mapping for absolute entity casing."""
        return MappingProxyType(
            cast(
                dict[str, str],
                _load_en_data(
                    EnEntityCasing.DIR / 'absolute_casings_map.json'
                )
            )
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_contextual_map() -> Mapping[str, tuple[EntityCasingContext, ...]]:
        """Get a cached mapping for contextual entity casing."""
        raw_map = cast(
            dict[str, list[EntityCasingContext]],
            _load_en_data(EnEntityCasing.DIR / 'contextual_casings_map.json')
        )
        return MappingProxyType(
            {key: tuple(contexts) for key, contexts in raw_map.items()}
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_contraction_suffixes() -> frozenset[str]:
        """Get a cached frozenset of allowed contraction suffixes."""
        return frozenset(
            cast(
                list[str],
                _load_en_data(EnEntityCasing.DIR / 'contraction_suffixes.json')
            )
        )


class EnPunctuation:
    """Data loader for English punctuation rules."""

    @staticmethod
    @lru_cache(maxsize=1)
    def get_elision_words() -> frozenset[str]:
        """Get a cached `frozenset` of elision words."""
        return frozenset(
            cast(list[str], _load_en_data('elision_words.json')))


class EnStringCasing:
    """Data loader for English string casing exceptions and prefixes."""

    DIR: Final = Path('string_casing')

    @staticmethod
    @lru_cache(maxsize=1)
    def get_lookup_map() -> Mapping[str, str]:
        """Get a combined cached mapping for string casings."""
        absolute_map = cast(
            dict[str, str],
            _load_en_data(EnStringCasing.DIR / 'absolute_casings_map.json')
        )
        prefixed_surnames_map = cast(
            dict[str, str],
            _load_en_data(EnStringCasing.DIR / 'prefixed_surnames_map.json')
        )
        return MappingProxyType(
            {**prefixed_surnames_map, **absolute_map}
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_lowercase_abbreviations() -> frozenset[str]:
        """
        Get a cached `frozenset` of lowercase abbreviations.
        """
        return frozenset(
            cast(
                list[str],
                _load_en_data(
                    EnStringCasing.DIR / 'lowercase_abbreviations.json'
                )
            )
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_map_suffix_exceptions() -> tuple[str, ...]:
        """Get a cached tuple of map suffix exceptions."""
        return tuple(
            cast(
                list[str],
                _load_en_data(
                    EnStringCasing.DIR / 'map_suffix_exceptions.json'
                )
            )
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_surname_prefix_exceptions() -> tuple[str, ...]:
        """Get a cached tuple of surname prefix exceptions."""
        return tuple(
            cast(
                list[str],
                _load_en_data(
                    EnStringCasing.DIR / 'surname_prefix_exceptions.json'
                )
            )
        )

    @staticmethod
    @lru_cache(maxsize=1)
    def get_surname_prefixes() -> tuple[str, ...]:
        """Get a cached tuple of standard surname prefixes."""
        return tuple(
            cast(
                list[str],
                _load_en_data(EnStringCasing.DIR / 'surname_prefixes.json')
            )
        )


class EnTokenCasing:
    """Data loader for English token casing specific rules."""

    @staticmethod
    @lru_cache(maxsize=1)
    def get_lowercase_particles() -> frozenset[str]:
        """Get a cached `frozenset` of lowercase particles."""
        return frozenset(
            cast(
                list[str],
                _load_en_data(
                    Path('entity_casing') / 'lowercase_particles.json'
                )
            )
        )
