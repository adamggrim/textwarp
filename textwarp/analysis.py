from collections import Counter
from math import ceil

from spacy.tokens import Doc

from ._constants import POS_TAGS, POS_WORD_TAGS
from ._model import nlp
from ._pos_counts import POSCounts


def calculate_time_to_read(text: str, wpm: int) -> int:
    """
    Calculate the minutes to read a given string.

    Args:
        text: The string to analyze.
        wpm: The number of words per minute to return.

    Returns:
        int: The minutes to read the given string. Rounded up if
            between zero and one minute, otherwise rounded to the
            nearest integer.
    """
    word_count: int = count_words(text)
    minutes_to_read: float = word_count / wpm
    rounded_minutes: int = int(minutes_to_read + 0.5)
    return ceil(minutes_to_read) if minutes_to_read < 1 else rounded_minutes


def count_chars(text: str) -> int:
    """
    Count the number of characters in a given string.

    Args:
        text: The string to analyze.

    Returns:
        int: The total number of characters in the string.
    """
    return len(text)


def count_lines(text: str) -> int:
    """
    Count the number of non-whitespace lines in a given string.

    Args:
        text: The string to analyze.

    Returns:
        int: The number of non-whitespace lines in the string.
    """
    lines: list[str] = text.splitlines()
    text_lines: list[str] = [line for line in lines if line.strip()]
    return len(text_lines)


def count_mfws(text: str, number_of_mfws: int) -> list[tuple]:
    """
    Count the most frequent words in a given string.

    Args:
        text: The string to analyze.
        number_of_mfws: The number of most frequent words to return.

    Returns:
        list[tuple]: A list of tuples with each tuple containing a word
            and its count.
    """
    doc: Doc = nlp(text)
    words: list[str] = [token.text.lower() for token in doc if token.is_alpha]
    counts: Counter[str] = Counter(words)
    return counts.most_common(number_of_mfws)


def count_pos(text: str) -> POSCounts:
    """
    Count the parts of speech in a given string.

    Args:
        text: The string to analyze.

    Returns:
        POSCounts: The parts of speech counts for the string.
    """
    doc: Doc = nlp(text)
    tags: list[str] = [
        token.pos_ for token in doc if not token.is_space
    ]
    counts: Counter[str] = Counter(tags)

    tag_counts: dict[str, int] = {
        tag_pair[0]: counts.get(tag_pair[0], 0) for tag_pair in POS_TAGS
    }
    total_word_count: int = sum(
        counts.get(tag, 0) for tag in POS_WORD_TAGS
    )

    pos_kwargs = {
        f'{tag.lower()}_count': count for tag, count in tag_counts.items()
    }
    return POSCounts(
        word_count=total_word_count,
        **pos_kwargs
    )


def count_sents(text: str) -> int:
    """
    Count the number of sentences in a given string.

    Args:
        text: The string to analyze.

    Returns:
        int: The number of sentences in the string.
    """
    doc: Doc = nlp(text)
    return len(list(doc.sents))


def count_words(text: str) -> int:
    """
    Count the number of words in a given string.

    Args:
        text: The string to analyze.

    Returns:
        word_count: The number of words in the string.
    """
    count_pos(text).word_count
