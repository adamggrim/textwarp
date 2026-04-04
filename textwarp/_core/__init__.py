"""Exposes core configuration, constants, and models."""

from textwarp._core.encoding import get_morse_map, get_morse_reversed_map
from textwarp._core.constants import maps, nlp, patterns
from textwarp._core.enums import (
    CaseSeparator,
    Casing,
    CountLabels,
    PresenceCheckType,
    RegexBoundary
)
from textwarp._core.exceptions import (
    CaseNotFoundError,
    EmptyClipboardError,
    InvalidCaseNameError,
    NoCaseNameError,
    NoRegexError,
    NoTextError,
    RegexNotFoundError,
    TextNotFoundError,
    WhitespaceCaseNameError,
    WhitespaceClipboardError
)
from textwarp._core.models import POSCounts, WordCount
from textwarp._core.types import EntityCasingContext, JSONType
from textwarp._core.utils import find_first_alphabetical_idx

__all__ = [
    'get_morse_map',
    'get_morse_reversed_map',
    'maps',
    'nlp',
    'patterns',
    'CaseSeparator',
    'Casing',
    'CountLabels',
    'PresenceCheckType',
    'RegexBoundary',
    'CaseNotFoundError',
    'EmptyClipboardError',
    'InvalidCaseNameError',
    'NoCaseNameError',
    'NoRegexError',
    'NoTextError',
    'RegexNotFoundError',
    'TextNotFoundError',
    'WhitespaceCaseNameError',
    'WhitespaceClipboardError',
    'POSCounts',
    'WordCount',
    'EntityCasingContext',
    'JSONType',
    'find_first_alphabetical_idx'
]
