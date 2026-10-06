"""Helper functions for the test suite."""

from typing import Any

from textwarp._cli.args import ARGS_MAP
from textwarp._cli.parsing import DEFAULT_MAX_FILE_MB, ParsedArgs


def make_parsed_args(**overrides: Any) -> ParsedArgs:
    """
    Create a `ParsedArgs` instance with sensible defaults for testing.
    """
    defaults: dict[str, Any] = {
        'pipeline': [ARGS_MAP['uppercase']],
        'lang': 'en',
        'input_files': [],
        'output_file': None,
        'markdown': False,
        'find': None,
        'replace': None,
        'copy_to_clipboard': False,
        'debug': False,
        'max_file_mb': DEFAULT_MAX_FILE_MB,
    }
    defaults.update(overrides)
    return ParsedArgs(**defaults)


def normalize_output(text: str) -> str:
    """Normalize whitespace for wrapped terminal output."""
    return ' '.join(text.split())
