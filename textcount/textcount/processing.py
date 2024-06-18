from textcount.analyzing import (get_char_count, get_mfws, get_pos_count, 
                                 get_time_to_read, get_word_count)
from textcount.data_structures import POSCounts
from textcount.formatting import (format_char_count, format_mfws, 
                                  format_pos_count, format_time_to_read, 
                                  format_word_count)
from textcount.input_output import ParameterInput


def process_char_count(string) -> None:
    """
    Deploys functions to analyze, format and print character count 
        output.

    Args:
        string (str): The string to analyze.

    """
    char_count = get_char_count(string)
    char_count_str = format_char_count(char_count)
    print(char_count_str)


def process_mfws(string, mfw_count) -> list[tuple]:
    """
    Deploys functions to analyze and format most frequent words output.

    Args:
        string (str): The string to analyze.
        mfw_count (int): The number of most frequent words to return.

    Returns:
        list[tuple]: A list of tuples with each tuple containing a word 
            (str) and its count (int).
    """
    mfw_count = int(mfw_count)
    mfws = get_mfws(string, mfw_count)
    words = word_tokenize(string)
    counts = Counter(words)
    return counts.most_common(mfw_count)


def process_pos_count(string) -> POSCounts:
    """
    Returns a POSCounts object containing the parts of speech counts 
        for a given string.

    Args:
        string (str): The string to analyze.

    Returns:
        POSCounts: The parts of speech counts for the string.
    """
    words = word_tokenize(string)
    word_tags = pos_tag(words, tagset='universal')
    counts = Counter(tag for _, tag in word_tags)
    pos_counts = POSCounts()
    setattr(pos_counts, 'word_count', sum(counts.get(tag, 0) for tag in 
                                          POS_TAGS))
    for tag in POS_KNOWN_TAGS:
        count = counts.get(tag, 0)
        setattr(pos_counts, f'{tag.lower()}_count', count)
    return pos_counts


def process_time_to_read(string, wpm) -> int:
    """
    Returns an integer representing the minutes to read a given string.

    Args:
        string (str): The string to analyze.
        wpm (int): The number of words per minute.

    Returns:
        int: The minutes to read the given string. Rounded up if more 
            than one minute, zero if less than one minute.
    """
    word_count = get_word_count(string)
    minutes_to_read = word_count / wpm
    return ceil(minutes_to_read) if minutes_to_read > 1 else 0


def process_word_count(string) -> int:
    """
    Returns an integer representing the number of words in a given 
        string.

    Args:
        string (str): The string to analyze.

    Returns:
        word_count (int): The number of words in the string.
    """
    words = word_tokenize(string)
    word_tags = pos_tag(words, tagset='universal')
    counts = Counter(tag for _, tag in word_tags)
    word_count = 0
    for tag in POS_TAGS:
        word_count += counts[tag] 
    return word_count