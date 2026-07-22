"""Functions for formatting analysis into readable strings."""

from collections.abc import Sequence
import gettext

from textwarp._core.models import POSCounts, WordCount

_ = gettext.gettext
ngettext = gettext.ngettext

__all__ = [
    'format_count',
    'format_entity_counts',
    'format_mfws',
    'format_pos_counts',
    'format_time_to_read',
    'format_ttr'
]


def _format_table(
    data_rows: Sequence[tuple[str, ...]],
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
    translated_name = _(name)

    return _('%(name)s count: %(count)d') % {
        'name': translated_name,
        'count': count
    }


def format_entity_counts(entities: list[WordCount]) -> str:
    """
    Return a string indicating the most frequent entities in a given
    string.

    Args:
        entities: A list of `WordCount` objects, containing an entity
            and its count.

    Returns:
        str: A formatted string indicating most frequent entities.
    """
    entity_data: list[tuple[str, str, str]] = [
        (
            f"'{entity_count.word}'",
            str(entity_count.count),
            f'({entity_count.percentage:.2f}%)'
        )
        for entity_count in entities
    ]

    return _format_table(entity_data)


def format_mfws(mfws: list[WordCount]) -> str:
    """
    Return a string indicating the most frequent words in a given
    string.

    Args:
        mfws: A list of `WordCount` objects, containing a word and its
            count.

    Returns:
        str: A formatted string indicating most frequent words.
    """
    mfw_data: list[tuple[str, str, str]] = [
        (
            f"'{word_count.word}'",
            str(word_count.count),
            f'({word_count.percentage:.2f}%)'
        )
        for word_count in mfws
    ]

    return _format_table(mfw_data)


def format_pos_counts(pos_counts: POSCounts) -> str:
    """
    Return a dynamically formatted string indicating parts of speech
    counts for a given `POSCounts` object.

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
    Return a string indicating the time to read a string.

    Args:
        minutes_to_read (int): The number of minutes.

    Returns:
        str: The formatted string indicating time to read.
    """
    hours, minutes = divmod(minutes_to_read, 60)
    if hours >= 1:
        formatted_hours: str = ngettext(
            '%(hours)d hour',
            '%(hours)d hours',
            hours
        ) % {'hours': hours}

        if minutes == 0:
            return _('%(hours)s to read') % {'hours': formatted_hours}

        formatted_minutes: str = ngettext(
            '%(minutes)d minute',
            '%(minutes)d minutes',
            minutes
        ) % {'minutes': minutes}

        return _('%(hours)s, %(minutes)s to read') % {
            'hours': formatted_hours,
            'minutes': formatted_minutes
        }

    if minutes >= 1:
        return ngettext(
            '%(minutes)d minute to read',
            '%(minutes)d minutes to read',
            minutes
        ) % {'minutes': minutes}

    return _('Less than 1 minute to read')


def format_ttr(ttr: float) -> str:
    """
    Return a string indicating the type-token ratio.

    Args:
        ttr (float): The type-token ratio.

    Returns:
        str: The formatted string indicating the ratio.
    """
    return _('Type-token ratio: %(ttr).2f') % {'ttr': ttr}
