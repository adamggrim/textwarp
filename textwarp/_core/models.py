"""Classes for parts-of-speech counts and word counts."""

from dataclasses import dataclass, field
from typing import final

from textwarp._core.constants.nlp import POS_TAGS

__all__ = ['POSCounts', 'WordCount']


@final
@dataclass
class POSCounts:
    """
    A class representing the counts and percentages for each part of
    speech.
    """
    word_count: int = 0
    tag_counts: dict[str, int] = field(default_factory=dict)

    def get_pos_counts(self, tag: str) -> int:
        """
        Get the count for a given parts-of-speech tag.

        Args:
            tag: The parts-of-speech tag (e.g., "ADJ", "NOUN").

        Returns:
            int: The count for the given parts-of-speech tag, or 0 if not
                found.
        """
        return self.tag_counts.get(tag, 0)

    def get_percentage(self, tag: str) -> float:
        """
        Get the percentage of a given part of speech in the total word
        count.

        Args:
            tag: The parts-of-speech tag (e.g., "ADJ", "NOUN").

        Returns:
            float: The calculated percentage, or 0.0 if self.word_count
                is zero.
        """
        count = self.get_pos_counts(tag)
        return (count / self.word_count * 100) if self.word_count else 0.0

    def get_pos_data(self) -> list[tuple[str, int, float]]:
        """
        Get all parts-of-speech data (count and percentage) as an
        iterable list of tuples.

        Returns:
            list[tuple[str, int, float]]: A list where each tuple
                contains the parts-of-speech name, count and percentage.
        """
        pos_data: list[tuple[str, int, float]] = []

        for tag, name in POS_TAGS:
            count: int = self.get_pos_counts(tag)
            percentage: float = self.get_percentage(tag)
            pos_data.append((name, count, percentage))

        return pos_data


@final
@dataclass
class WordCount:
    """
    A class representing the count and percentage for a word in a
    string.
    """
    word: str
    count: int
    percentage: float
