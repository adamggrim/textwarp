from dataclasses import (
    dataclass,
    field
)
from typing import final

from ._constants import POS_TAGS


@final
@dataclass
class POSCounts:
    """
    A class representing the counts and percentages for each part of
    speech.
    """
    word_count: int = 0,
    adj_count: int = 0,
    adp_count: int = 0,
    adv_count: int = 0,
    conj_count: int = 0,
    det_count: int = 0,
    noun_count: int = 0,
    num_count: int = 0,
    part_count: int =0,
    pron_count: int = 0,
    verb_count: int = 0,
    x_count: int = 0

    def _calculate_percentage(self, count: int) -> float:
        """
        Calculate the percentage of a given part of
        speech in the total word count.

        Args:
            count (int): The specific POS count.

        Returns:
            float: The calculated percentage, or 0.0 if self.word_count
                is zero.
        """
        return (count / self.word_count * 100) if self.word_count else 0.0

    @property
    def adj_percentage(self) -> float:
        """
        Calculate the percentage of adjectives in the total word count.

        Returns:
            float: The percentage of adjectives in the total word count.
        """
        return self._calculate_percentage(self.adj_count)

    @property
    def adp_percentage(self) -> float:
        """
        Calculate the percentage of adpositions in the total word count.

        Returns:
            float: The percentage of adpositions in the total word
                count.
        """
        return self._calculate_percentage(self.adp_count)

    @property
    def adv_percentage(self) -> float:
        """
        Calculate the percentage of adverbs in the total word count.

        Returns:
            float: The percentage of adverbs in the total word count.
        """
        return self._calculate_percentage(self.adv_count)

    @property
    def conj_percentage(self) -> float:
        """
        Calculate the percentage of conjunctions in the total word
        count.

        Returns:
            float: The percentage of conjunctions in the total word
                count.
        """
        return self._calculate_percentage(self.conj_count)

    @property
    def det_percentage(self) -> float:
        """
        Calculate the percentage of determiners in the total word count.

        Returns:
            float: The percentage of determiners in the total word
                count.
        """
        return self._calculate_percentage(self.det_count)

    @property
    def noun_percentage(self) -> float:
        """
        Calculate the percentage of nouns in the total word count.

        Returns:
            float: The percentage of nouns in the total word count.
        """
        return self._calculate_percentage(self.noun_count)

    @property
    def num_percentage(self) -> float:
        """
        Calculate the percentage of numbers in the total word count.

        Returns:
            float: The percentage of numbers in the total word count.
        """
        return self._calculate_percentage(self.num_count)

    @property
    def part_percentage(self) -> float:
        """
        Calculate the percentage of particles in the total word count.

        Returns:
            float: The percentage of particles in the total word count.
        """
        return self._calculate_percentage(self.part_count)

    @property
    def pron_percentage(self) -> float:
        """
        Calculate the percentage of pronouns in the total word count.

        Returns:
            float: The percentage of pronouns in the total word count.
        """
        return self._calculate_percentage(self.pron_count)

    @property
    def verb_percentage(self) -> float:
        """
        Calculate the percentage of verbs in the total word count.

        Returns:
            float: The percentage of verbs in the total word count.
        """
        return self._calculate_percentage(self.verb_count)

    @property
    def x_percentage(self) -> float:
        """
        Calculate the percentage of other parts of speech tags in the
        total word count.

        Returns:
            float: The percentage of other parts of speech tags in the
                total word count.
        """
        return self._calculate_percentage(self.x_count)


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
