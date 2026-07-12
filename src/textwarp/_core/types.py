"""Generic type definitions used across the package."""

from typing import (
    Any,
    Callable,
    TypeAlias,
    TypedDict
)

__all__ = ['EntityCasingContext', 'JSONType']


class EntityCasingContext(TypedDict, total=False):
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
    context_window: int


JSONType: TypeAlias = (
    dict[str, Any] | list[Any] | str | int | float | bool | None
)

PipelineItem: TypeAlias = tuple[str, Callable[..., str]]

Pipeline: TypeAlias = list[PipelineItem]
