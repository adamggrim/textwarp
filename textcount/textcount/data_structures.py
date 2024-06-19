class POSCounts:
    """
    A class representing the counts for each part of speech in a given text.
    """
    def __init__(self, word_count=0, adj_count=0, adp_count=0, adv_count=0, 
                 conj_count=0, det_count=0, noun_count=0, prt_count=0, 
                 pron_count=0, verb_count=0, other_count=0):
        self.word_count = word_count
        self.adj_count = adj_count
        self.adp_count = adp_count
        self.adv_count = adv_count
        self.conj_count = conj_count
        self.det_count = det_count
        self.noun_count = noun_count
        self.prt_count = prt_count
        self.pron_count = pron_count
        self.verb_count = verb_count
        self.other_count = other_count

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

    @property
    def other_ratio(self) -> float:
        """
        Calculates the ratio of other parts of speech tags to total 
            word count.

        Returns:
            float: The ratio of other parts of speech tags to total 
                word count.
        """
        return (self.other_count / self.word_count * 100 if self.word_count 
                else 0)