from collections import Counter
from math import ceil

from nltk import pos_tag, word_tokenize

from textcount.constants import POS_TAGS, POS_WORD_TAGS
from textcount.data_structures import POSCounts


def count_chars(text: str) -> int:
    """
    Returns an integer representing the number of characters in a given
        string.

    Args:
        text: The string to analyze.

    Returns:
        int: A formatted string indicating character count.
    """
    return len(text)


def count_lines(text: str) -> int:
    """
    Returns an integer representing the number of non-whitespace lines
        in a given string.

    Args:
        text: The string to analyze.

    Returns:
        int: The number of non-whitespace lines in the string.
    """
    lines: list[str] = text.splitlines()
    text_lines: list[str] = [line for line in lines if line.strip()]
    return len(text_lines)


def count_mfws(text: str, mfw_count: int) -> list[tuple]:
    """
    Returns a list of tuples indicating the most frequent words in a
        given string.

    Args:
        text: The string to analyze.
        mfw_count: The number of most frequent words to return.

    Returns:
        list[tuple]: A list of tuples with each tuple containing a word
            and its count.
    """
    words: list[str] = word_tokenize(text)
    counts: Counter[str] = Counter(words)
    return counts.most_common(mfw_count)


def count_pos(text: str) -> POSCounts:
    """
    Returns a POSCounts object containing the parts of speech counts
        for a given string.

    Args:
        text: The string to analyze.

    Returns:
        POSCounts: The parts of speech counts for the string.
    """
    words: list[str] = word_tokenize(text)
    word_tags: list[tuple[str, str]] = pos_tag(words, tagset='universal')
    counts: Counter[str] = Counter(tag for _, tag in word_tags)
    pos_counts: POSCounts = POSCounts()
    # Set total word count for POSCounts object
    setattr(pos_counts, 'word_count', sum(counts.get(tag, 0) for tag in
                                          POS_WORD_TAGS))
    # Set parts of speech counts for POSCounts object
    for tag_pair in POS_TAGS:
        count: int = counts.get(tag_pair[0], 0)
        setattr(pos_counts, f'{tag_pair[0].lower()}_count', count)
    return pos_counts


def count_time_to_read(text: str, wpm: int) -> int:
    """
    Returns an integer representing the minutes to read a given string.

    Args:
        text: The string to analyze.
        wpm: The number of words per minute to return.

    Returns:
        int: The minutes to read the given string. Rounded up if more
            than one minute, zero if less than one minute.
    """
    word_count: int = count_words(text)
    minutes_to_read: float = word_count / wpm
    return ceil(minutes_to_read) if minutes_to_read > 1 else 0


def count_words(text: str) -> int:
    """
    Returns an integer representing the number of words in a given
        string.

    Args:
        text: The string to analyze.

    Returns:
        word_count: The number of words in the string.
    """
    words: list[str] = word_tokenize(text)
    word_tags: list[tuple[str, str]] = pos_tag(words, tagset='universal')
    counts: Counter[str] = Counter(tag for _, tag in word_tags)
    word_count: int = 0
    for tag in POS_WORD_TAGS:
        word_count += counts[tag]
    return word_count
