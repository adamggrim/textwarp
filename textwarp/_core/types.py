"""Generic type definitions used across the package."""

from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    TypeAlias,
    TypedDict,
    final
)

__all__ = ['EntityCasingContext', 'JSONType']


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

# A type for a pipeline item, a tuple of a command string and a callable
# function.
PipelineItem: TypeAlias = tuple[str, Callable[[str], str]]

# A type for a pipeline, a list of pipeline items.
Pipeline: TypeAlias = list[PipelineItem]
