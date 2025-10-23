class POSCounts:
    """A class representing the counts for each part of speech in a
    given text."""

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
            prt_count: int =0,
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
        self.prt_count: int = prt_count
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
    def adj_ratio(self) -> float:
        """
        Calculate the ratio of adjectives to the total word count.

        Returns:
            float: The ratio of adjectives to the total word count.
        """
        return self._calculate_percentage(self.adj_count)

    @property
    def adp_ratio(self) -> float:
        """
        Calculate the ratio of adpositions to the total word count.

        Returns:
            float: The ratio of adpositions to the total word count.
        """
        return self._calculate_percentage(self.adp_count)

    @property
    def adv_ratio(self) -> float:
        """
        Calculate the ratio of adverbs to the total word count.

        Returns:
            float: The ratio of adverbs to the total word count.
        """
        return self._calculate_percentage(self.adv_count)

    @property
    def conj_ratio(self) -> float:
        """
        Calculate the ratio of conjunctions to the total word count.

        Returns:
            float: The ratio of conjunctions to the total word count.
        """
        return self._calculate_percentage(self.conj_count)

    @property
    def det_ratio(self) -> float:
        """
        Calculate the ratio of determiners to the total word count.

        Returns:
            float: The ratio of determiners to the total word count.
        """
        return self._calculate_percentage(self.det_count)

    @property
    def noun_ratio(self) -> float:
        """
        Calculate the ratio of nouns to the total word count.

        Returns:
            float: The ratio of nouns to the total word count.
        """
        return self._calculate_percentage(self.noun_count)

    @property
    def num_ratio(self) -> float:
        """
        Calculate the ratio of numbers to the total word count.

        Returns:
            float: The ratio of numbers to the total word count.
        """
        return self._calculate_percentage(self.num_count)

    @property
    def prt_ratio(self) -> float:
        """
        Calculate the ratio of particles to the total word count.

        Returns:
            float: The ratio of particles to the total word count.
        """
        return self._calculate_percentage(self.prt_count)

    @property
    def pron_ratio(self) -> float:
        """
        Calculate the ratio of pronouns to the total word count.

        Returns:
            float: The ratio of pronouns to the total word count.
        """
        return self._calculate_percentage(self.pron_count)

    @property
    def verb_ratio(self) -> float:
        """
        Calculate the ratio of verbs to the total word count.

        Returns:
            float: The ratio of verbs to the total word count.
        """
        return self._calculate_percentage(self.verb_count)

    @property
    def x_ratio(self) -> float:
        """
        Calculate the ratio of other parts of speech tags to the total
        word count.

        Returns:
            float: The ratio of other parts of speech tags to the total
                word count.
        """
        return self._calculate_percentage(self.x_count)
