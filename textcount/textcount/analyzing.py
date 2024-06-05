from collections import Counter
from math import ceil

from nltk import pos_tag, word_tokenize

from textcount.constants import POS_KNOWN_TAGS, POS_TAGS
from textcount.data_structures import POSCounts


def get_char_count(string) -> str:
    """
    Returns a string indicating the number of characters in a given 
        string.

    Args:
        string (str): The string to analyze.
    """
    char_count = len(string)
    return char_count


def get_pos_count(string) -> POSCounts:
    """
    Returns a POSCount object containing the parts of speech counts 
        for a given string.

    Args:
        string (str): The string to analyze.

    Returns:
        POSCount: The parts of speech counts for the string.
    """
    words = word_tokenize(string)
    word_tags = pos_tag(words, tagset='universal')
    counts = Counter(tag for _, tag in word_tags)
    pos_counts = {
        'word_count': sum(counts.get(tag, 0) for tag in POS_TAGS),
    }
    for tag in POS_KNOWN_TAGS:
        pos_counts[f'{tag.lower()}_count'] = counts.get(tag, 0)
    return pos_counts


def get_time_to_read(string, wpm) -> str:
    """
    Returns a string representing the minutes to read a given string.

    Args:
        string (str): The string to analyze.
        wpm (int): The number of words per minute.

    Returns:
        str: The minutes to read the given string, rounded up if greater than 
            one.
    """
    word_count = get_word_count(string)
    minutes_to_read = word_count / wpm
    return ceil(minutes_to_read) if minutes_to_read > 1 else minutes_to_read


def get_word_count(string) -> str:
    """
    Returns the number of words in a given string.

    Args:
        string (str): The string to analyze.
    """
    words = word_tokenize(string)
    word_tags = pos_tag(words, tagset='universal')
    counts = Counter(tag for _, tag in word_tags)
    for tag in POS_TAGS:
        word_count += counts[tag] 
    return word_count