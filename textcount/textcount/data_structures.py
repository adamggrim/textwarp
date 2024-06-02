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
        Calculate the percentage of adjectives relative to the 
        total word count."""
        return self.adj_count / self.word_count * 100 if self.word_count else 0

    @property
    def adp_ratio(self) -> float:
        return self.adp_count / self.word_count * 100 if self.word_count else 0

    @property
    def adv_ratio(self) -> float:
        return self.adv_count / self.word_count * 100 if self.word_count else 0

    @property
    def conj_ratio(self) -> float:
        return self.conj_count / self.word_count * 100 if self.word_count else 0

    @property
    def det_ratio(self) -> float:
        return self.det_count / self.word_count * 100 if self.word_count else 0

    @property
    def noun_ratio(self) -> float:
        return self.noun_count / self.word_count * 100 if self.word_count else 0

    @property
    def prt_ratio(self) -> float:
        return self.prt_count / self.word_count * 100 if self.word_count else 0

    @property
    def pron_ratio(self) -> float:
        return self.pron_count / self.word_count * 100 if self.word_count else 0

    @property
    def verb_ratio(self) -> float:
        return self.verb_count / self.word_count * 100 if self.word_count else 0