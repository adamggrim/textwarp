from collections import Counter
from math import ceil

from nltk import pos_tag, word_tokenize

from textcount.constants import POS_TAGS, POS_WORD_TAGS
from textcount.data_structures import POSCounts


def get_char_count(string: str) -> int:
    """
    Gets an int indicating the number of characters in a given string.

    Args:
        string (str): The string to analyze.

    Returns:
        int: A formatted string indicating character count.
    """
    return len(string)


def get_mfws(string: str, mfw_count: int) -> list[tuple]:
    """
    Gets a list of tuples indicating the most frequent words in a given 
        string.

    Args:
        string (str): The string to analyze.
        mfw_count (int): The number of most frequent words to return.

    Returns:
        list[tuple]: A list of tuples with each tuple containing a word 
            (str) and its count (int).
    """
    words = word_tokenize(string)
    counts = Counter(words)
    return counts.most_common(mfw_count)


def get_pos_count(string: str) -> POSCounts:
    """
    Gets a POSCounts object containing the parts of speech counts for a 
        given string.

    Args:
        string (str): The string to analyze.

    Returns:
        POSCounts: The parts of speech counts for the string.
    """
    words = word_tokenize(string)
    word_tags = pos_tag(words, tagset='universal')
    counts = Counter(tag for _, tag in word_tags)
    pos_counts = POSCounts()
    # Set total word count for POSCounts object
    setattr(pos_counts, 'word_count', sum(counts.get(tag, 0) for tag in 
                                          POS_WORD_TAGS))
    # Set parts of speech counts for POSCounts object
    for tag_pair in POS_TAGS:
        count = counts.get(tag_pair[0], 0)
        setattr(pos_counts, f'{tag_pair[0].lower()}_count', count)
    return pos_counts


def get_time_to_read(string: str, wpm: int) -> int:
    """
    Gets an integer representing the minutes to read a given string.

    Args:
        string (str): The string to analyze.
        wpm (int): The number of words per minute to return.

    Returns:
        int: The minutes to read the given string. Rounded up if more 
            than one minute, zero if less than one minute.
    """
    word_count = get_word_count(string)
    minutes_to_read = word_count / wpm
    return ceil(minutes_to_read) if minutes_to_read > 1 else 0


def get_word_count(string: str) -> int:
    """
    Gets an integer representing the number of words in a given string.

    Args:
        string (str): The string to analyze.

    Returns:
        word_count (int): The number of words in the string.
    """
    words = word_tokenize(string)
    word_tags = pos_tag(words, tagset='universal')
    counts = Counter(tag for _, tag in word_tags)
    word_count = 0
    for tag in POS_WORD_TAGS:
        word_count += counts[tag] 
    return word_count