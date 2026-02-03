"""Public functions for analyzing text."""

from __future__ import annotations

from collections import Counter
from math import ceil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.tokens import Doc

from ._core.constants.nlp import POS_TAGS
from ._core.models import (
    POSCounts,
    WordCount
)
from ._lib.nlp import (
    extract_words_from_doc,
    process_as_doc
)


def calculate_time_to_read(text: str, wpm: int) -> int:
    """
    Calculate the minutes to read a given string.

    Args:
        text: The string to analyze.
        wpm: The number of words per minute to return.

    Returns:
        int: The minutes to read the given string. Rounded up if
            between zero and one minute, otherwise rounded to the
            nearest integer.
    """
    word_count = count_words(text)
    minutes_to_read = word_count / wpm
    rounded_minutes = int(minutes_to_read + 0.5)
    return ceil(minutes_to_read) if minutes_to_read < 1 else rounded_minutes


def count_chars(text: str) -> int:
    """
    Count the number of characters in a given string.

    Args:
        text: The string to analyze.

    Returns:
        int: The total number of characters in the string.
    """
    return len(text)


def count_lines(text: str) -> int:
    """
    Count the number of non-whitespace lines in a given string.

    Args:
        text: The string to analyze.

    Returns:
        int: The number of non-whitespace lines in the string.
    """
    lines = text.splitlines()
    text_lines = [line for line in lines if line.strip()]
    return len(text_lines)


def count_mfws(content: str | Doc, num_mfws: int) -> list[WordCount]:
    """
    Count the most frequent words in a given string.

    Args:
        content: The string or spaCy ``Doc`` to analyze.
        num_mfws: The number of most frequent words to return.

    Returns:
        list[WordCount]: A list of WordCount objects containing a word
            and its count.
    """
    doc = process_as_doc(content)
    words = extract_words_from_doc(doc)
    total_word_count = len(words)

    if total_word_count == 0:
        return []

    counts = Counter(words)
    count_tuples: list[tuple[str, int]] = counts.most_common(num_mfws)

    return [
        WordCount(
            word=word,
            count=count,
            percentage=(count / total_word_count * 100)
        )
        for word, count in count_tuples
    ]


def count_pos(content: str | Doc) -> POSCounts:
    """
    Count the parts of speech in a given string.

    Args:
        content: The string or spaCy ``Doc`` to analyze.

    Returns:
        POSCounts: The parts of speech counts for the string.
    """
    doc = process_as_doc(content)
    tags = [token.pos_ for token in doc if not token.is_space]
    counts = Counter(tags)

    tag_counts: dict[str, int] = {
        tag_pair[0]: counts.get(tag_pair[0], 0) for tag_pair in POS_TAGS
    }
    total_word_count = len(extract_words_from_doc(doc))

    return POSCounts(
        word_count=total_word_count,
        tag_counts=tag_counts
    )


def count_sents(content: str | Doc) -> int:
    """
    Count the number of sentences in a given string.

    Args:
        content: The string or spaCy ``Doc`` to analyze.

    Returns:
        int: The number of sentences in the string.
    """
    doc = process_as_doc(content)
    return len(list(doc.sents))


def count_words(content: str | Doc) -> int:
    """
    Count the number of words in a given string.

    Args:
        text: The string to analyze.

    Returns:
        word_count: The number of words in the string.
    """
    doc = process_as_doc(content)
    return len(extract_words_from_doc(doc))
