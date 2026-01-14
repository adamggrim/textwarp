"""Generic type definitions used across the package."""

from dataclasses import dataclass
from typing import (
    Any,
    TypeAlias,
    TypedDict,
    final
)

@final
@dataclass
class EntityCasingContext(TypedDict):
    """
    The casing context for a custom entity.

    Attributes:
        casing: The casing to apply.
        pos_sequences: A list of parts-of-speech sequences for the
            entity.
        ngrams: A list of ngrams to check for.

    """
    casing: str
    pos_sequences: list[list[str]]
    ngrams: list[str]


# A type for JSON data.
JSONType: TypeAlias = (
    dict[str, Any] | list[Any] | str | int | float | bool | None
)
