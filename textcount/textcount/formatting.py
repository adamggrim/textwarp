from textcount.data_structures import POSCounts


def format_char_count(char_count: int) -> str:
    """
    Returns a string indicating the number of characters in a given 
        string.

    Args:
        char_count (int): The string to analyze.

    Returns:
        str: A formatted string indicating character count.
    """
    return f'Character count: {char_count}'


def format_mfws(mfws: list[tuple]) -> str:
    """
    Returns a string indicating the most frequent words in a given 
        string.

    Args:
        mfws (list[tuple]): A list of tuples with each tuple containing 
            a word (str) and its count (int)

    Returns:
        str: A formatted string indicating most frequent words.
    """
    word_count_strs = [f'{word}: {count}' for word, count in mfws]
    return '\n'.join(word_count_strs)


def format_pos_count(pos_counts: POSCounts) -> str:
    """
    Returns a string indicating the parts of speech counts for a given 
        string.

    Args:
        pos_counts (POSCounts): The parts of speech counts for the 
            string.

    Returns:
        str: A formatted string indicating parts of speech counts.
    """
    pos_str_counts = (
        ('Adjectives', pos_counts.adj_count, pos_counts.adj_ratio),
        ('Adpositions', pos_counts.adp_count, pos_counts.adp_ratio),
        ('Adverbs', pos_counts.adv_count, pos_counts.adv_ratio),
        ('Conjunctions', pos_counts.conj_count, pos_counts.conj_ratio),
        ('Determiners', pos_counts.det_count, pos_counts.det_ratio),
        ('Nouns', pos_counts.noun_count, pos_counts.noun_ratio),
        ('Particles', pos_counts.prt_count, pos_counts.prt_ratio),
        ('Pronouns', pos_counts.pron_count, pos_counts.pron_ratio),
        ('Verbs', pos_counts.verb_count, pos_counts.verb_ratio),
        ('Other', pos_counts.other_count, pos_counts.other_ratio)
    )
    results = [
        f'{pos:12}: {count:4} ({ratio:6.2f}%)'
        for pos, count, ratio in pos_str_counts
    ]
    return '\n'.join(results)


def format_time_to_read(minutes_to_read: int) -> str:
    """
    Returns a string indicating the time to read a given string.

    Args:
        string (str): The string to analyze.
        wpm (int): The number of words per minute.

    Returns:
        str: The formatted string indicating time to read.
    """
    hours, minutes = divmod(minutes_to_read, 60)
    if hours >= 1:
        hours_str = f'{hours} hours' if hours != 1 else '1 hour'
        if minutes == 0:
            return hours_str
        minutes_str = f'{minutes} minutes' if minutes != 1 else '1 minute'
        return f'{hours_str}, {minutes_str}'
    elif minutes >= 1:
        return f'{minutes} minutes' if minutes != 1 else '1 minute'
    else:
        return 'Less than 1 minute'


def format_word_count(word_count: int) -> str:
    """
    Returns a string indicating the number of words in a given string.

    Args:
        string (str): The string to analyze.

    Returns:
        str: The formatted string indicating word count.
    """
    return f'Word count: {word_count}'