class POSCounts:
    """
    A class representing the counts and percentages for each part of
    speech.
    """

    def __init__(
            self,
            word_count: int = 0,
            adj_count: int = 0,
            adp_count: int = 0,
            adv_count: int = 0,
            conj_count: int = 0,
            det_count: int =0,
            noun_count: int = 0,
            num_count: int = 0,
            part_count: int =0,
            pron_count: int = 0,
            verb_count: int = 0,
            x_count: int = 0
    ):
        self.word_count: int = word_count
        self.adj_count: int = adj_count
        self.adp_count: int = adp_count
        self.adv_count: int = adv_count
        self.conj_count: int = conj_count
        self.det_count: int = det_count
        self.noun_count: int = noun_count
        self.num_count: int = num_count
        self.part_count: int = part_count
        self.pron_count: int = pron_count
        self.verb_count: int = verb_count
        self.x_count: int = x_count


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
