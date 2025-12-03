"""Functions for formatting text analysis into human-readable output."""

from ._models import (
    POSCounts,
    WordCount
)


def _format_table(
    data_rows: list[tuple[str, ...]],
    padding: int = 2
) -> str:
    """
    Create a neatly aligned, multi-line table from tuples of strings.

    Args:
        data_rows: A list of rows, where each row is a tuple of strings.
        padding: The space to add between columns.

    Returns:
        str: A formatted, multi-line string table.
    """
    if not data_rows:
        return ''

    num_cols: int = len(data_rows[0])

    col_widths: list[int] = [0] * num_cols
    for row in data_rows:
        for i, item in enumerate(row):
            col_widths[i] = max(col_widths[i], len(item))

    results: list[str] = []
    for row in data_rows:
        formatted_cols: list[str] = []
        for i, item in enumerate(row):
            align: str = '<' if i != num_cols - 1 else '>'
            width: int = col_widths[i]

            if i < num_cols - 1:
                width += padding

            formatted_cols.append(f'{item:{align}{width}}')

        results.append(''.join(formatted_cols))

    return '\n'.join(results)


def format_count(name: str, count: int) -> str:
    """
    Return a string indicating the count of a specific analysis.

    Args:
        name: The name of the count.
        count: The count to display.

    Returns:
        str: A formatted string indicating the name and count.
    """
    return f'{name} count: {count}'


def format_mfws(mfws: list[WordCount]) -> str:
    """
    Return a string indicating the most frequent words in a given
    string.

    Args:
        mfws: A list of WordCount objects containing a word and its
            count.

    Returns:
        str: A formatted string indicating most frequent words.
    """
    mfw_data: list[tuple[str, str, str]] = [
        (
            word_count.word,
            str(word_count.count),
            f'({word_count.percentage:.2f}%)'
        )
        for word_count in mfws
    ]

    return _format_table(mfw_data)


def format_pos_count(pos_counts: POSCounts) -> str:
    """
    Return a dynamically formatted string indicating parts of speech
    counts for a given POSCounts object.

    Args:
        pos_counts: The parts of speech counts.

    Returns:
        str: A formatted string indicating parts of speech counts.
    """
    pos_data: list[tuple[str, int, float]] = pos_counts.get_pos_data()

    formatted_pos_data: list[tuple[str, str, str]] = [
        (
            name,
            str(count),
            f'({percentage:.2f}%)'
        )
        for name, count, percentage in pos_data
    ]

    return _format_table(formatted_pos_data)


def format_time_to_read(minutes_to_read: int) -> str:
    """
    Return a string indicating the time to read a given string.

    Args:
        minutes_to_read (int): The number of minutes.

    Returns:
        str: The formatted string indicating time to read.
    """
    hours: int
    minutes: int
    hours, minutes = divmod(minutes_to_read, 60)
    if hours >= 1:
        formatted_hours: str = f'{hours} hours' if hours != 1 else '1 hour'
        if minutes == 0:
            return formatted_hours
        formatted_minutes: str = (
            f'{minutes} minutes' if minutes != 1 else '1 minute'
        )
        return f'{formatted_hours}, {formatted_minutes}'
    elif minutes >= 1:
        return f'{minutes} minutes' if minutes != 1 else '1 minute'
    else:
        return 'Less than 1 minute'
