class POSCount:
    word_count: int
    adj_count: int
    adp_count: int
    adv_count: int
    conj_count: int
    det_count: int
    noun_count: int
    prt_count: int
    pron_count: int
    verb_count: int

    @property
    def adj_ratio(self) -> float:
        """
        Calculates the ratio of adjectives to total word count.

        Returns:
            float: The ratio of adjectives to total word count.
        """
        return self.adj_count / self.word_count * 100 if self.word_count else 0

    @property
    def adp_ratio(self) -> float:
        """
        Calculates the ratio of adpositions to total word count.

        Returns:
            float: The ratio of adpositions to total word count.
        """
        return self.adp_count / self.word_count * 100 if self.word_count else 0

    @property
    def adv_ratio(self) -> float:
        """
        Calculates the ratio of adverbs to total word count.

        Returns:
            float: The ratio of adverbs to total word count.
        """
        return self.adv_count / self.word_count * 100 if self.word_count else 0

    @property
    def conj_ratio(self) -> float:
        """
        Calculates the ratio of conjunctions to total word count.
        
        Returns:
            float: The ratio of conjunctions to total word count.
        """
        return (self.conj_count / self.word_count * 100 if self.word_count 
                else 0)

    @property
    def det_ratio(self) -> float:
        """
        Calculates the ratio of determiners to total word count.
        
        Returns:
            float: The ratio of determiners to total word count.
        """
        return self.det_count / self.word_count * 100 if self.word_count else 0

    @property
    def noun_ratio(self) -> float:
        """
        Calculates the ratio of nouns to total word count.

        Returns:
            float: The ratio of nouns to total word count.
        """
        return (self.noun_count / self.word_count * 100 if self.word_count 
                else 0)

    @property
    def prt_ratio(self) -> float:
        """
        Calculates the ratio of particles to total word count.

        Returns:
            float: The ratio of particles to total word count.
        """
        return self.prt_count / self.word_count * 100 if self.word_count else 0

    @property
    def pron_ratio(self) -> float:
        """
        Calculates the ratio of pronouns to total word count.

        Returns:
            float: The ratio of pronouns to total word count.
        """
        return (self.pron_count / self.word_count * 100 if self.word_count 
                else 0)

    @property
    def verb_ratio(self) -> float:
        """
        Calculates the ratio of verbs to total word count.

        Returns:
            float: The ratio of verbs to total word count.
        """
        return self.verb_count / self.word_count * 100 if self.word_count else 0