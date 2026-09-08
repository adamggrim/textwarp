"""Generic type definitions used across the package."""

from typing import (
    TYPE_CHECKING,
    Any,
    TypeAlias,
    TypedDict
)

if TYPE_CHECKING:
    from textwarp._cli.args import CLICommand

__all__ = ['EntityCasingContext', 'JSONType', 'Pipeline', 'PipelineItem']


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

PipelineItem: TypeAlias = 'CLICommand'

Pipeline: TypeAlias = list[PipelineItem]
