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

    num_cols = len(data_rows[0])

    col_widths = [0] * num_cols
    for row in data_rows:
        for i, item in enumerate(row):
            col_widths[i] = max(col_widths[i], len(item))

    results = []
    for row in data_rows:
        formatted_cols = []
        for i, item in enumerate(row):
            align = '<' if i != num_cols - 1 else '>'
            width = col_widths[i]

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


def format_mfws(mfws: list[tuple]) -> str:
    """
    Return a string indicating the most frequent words in a given
    string.

    Args:
        mfws: A list of tuples with each tuple containing a word and its
            count.

    Returns:
        str: A formatted string indicating most frequent words.
    """
    formatted_word_counts: list[str] = [f'{word}: {count}' for word, count in mfws]
    return '\n'.join(formatted_word_counts)


def format_pos_count(pos_counts: POSCounts) -> str:
    """
    Return a dynamically formatted string indicating parts of speech
    counts for a given POSCounts object.

    Args:
        pos_counts: The parts of speech counts.

    Returns:
        str: A formatted string indicating parts of speech counts.
    """
    pos_tuples: list[tuple[str, int, float]] = []
    for tag_pair in POS_TAGS:
        pos: str = tag_pair[1]
        count: int = getattr(pos_counts, f'{tag_pair[0].lower()}_count')
        ratio: float = getattr(pos_counts, f'{tag_pair[0].lower()}_ratio')
        pos_tuples.append((pos, count, ratio))
    max_count_length: int = max(len(f'{count}') for _, count, _ in pos_tuples)
    max_ratio_length: int = max(len(f'({ratio:.2f}%)') for _, _, ratio in
                           pos_tuples)
    padding: int = 2
    results: list[str] = []
    for pos, count, ratio in pos_tuples:
        formatted_ratio: str = f'({ratio:.2f}%)'
        # Dynamic spacing based on POS, count and ratio length
        results.append(f'{pos:{MAX_POS_LENGTH + padding}}'
                       f'{count:<{max_count_length + padding}}'
                       f'{formatted_ratio:>{max_ratio_length}}')
    return '\n'.join(results)


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
        formatted_hours = f'{hours} hours' if hours != 1 else '1 hour'
        if minutes == 0:
            return formatted_hours
        formatted_minutes = f'{minutes} minutes' if minutes != 1 else '1 minute'
        return f'{formatted_hours}, {formatted_minutes}'
    elif minutes >= 1:
        return f'{minutes} minutes' if minutes != 1 else '1 minute'
    else:
        return 'Less than 1 minute'
