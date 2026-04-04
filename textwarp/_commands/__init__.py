"""
Exposes analysis and replacement commands for use across the package.
"""

from textwarp._commands.analysis import (
    char_count,
    line_count,
    mfws,
    pos_count,
    sentence_count,
    time_to_read,
    word_count
)
from textwarp._commands.replacement import replace, replace_case, replace_regex

__all__ = [
    'char_count',
    'line_count',
    'mfws',
    'pos_count',
    'sentence_count',
    'time_to_read',
    'word_count',
    'replace',
    'replace_case',
    'replace_regex'
]
