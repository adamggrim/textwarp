"""
English-specific functions for converting between cardinal and ordinal
numbers.
"""


def _get_nlp_doc(text: str):
    """
    Helper to initialize the NLP document.

    Args:
        text: The input text to process.

    Returns:
        The processed NLP document.
    """
    from textwarp._lib.nlp import process_as_doc
    return process_as_doc(text, disable=['parser', 'ner', 'lemmatizer'])


def _get_ordinal_suffix(number: int) -> str:
    """Determine the correct ordinal suffix for a given integer."""
    if 10 <= number % 100 <= 20:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')


def _is_part_of_mixed_fraction(text: str, start_index: int) -> bool:
    """
    Look ahead in the text to determine if the current number precedes a
    fraction.

    Args:
        text: The text to analyze.
        start_index: The index immediately following the current number.
    """
    lookahead_index = start_index

    while lookahead_index < len(text) and text[lookahead_index].isspace():
        lookahead_index += 1

    found_numerator = False
    while lookahead_index < len(text) and text[lookahead_index].isdigit():
        found_numerator = True
        lookahead_index += 1

    return (
        found_numerator
        and lookahead_index < len(text)
        and text[lookahead_index] == '/'
    )


def cardinal_to_ordinal(text: str) -> str:
    """
    Convert cardinal numbers in a given string to ordinal numbers.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    doc = _get_nlp_doc(text)
    result = []
    last_idx = 0

    for token in doc:
        # Isolate the digits or fraction by stripping commas.
        normalized_text = token.text.replace(',', '')
        is_digit = normalized_text.isdigit()
        is_fraction = (
            '/' in normalized_text
            and len(normalized_text.split('/')) == 2
            and all(p.isdigit() for p in normalized_text.split('/'))
        )

        if token.pos_ == 'NUM' and (is_digit or is_fraction):
            start = token.idx
            end = start + len(token)

            # Ignore numbers with decimals.
            if (
                (start > 0 and text[start - 1] == '.')
                or (end < len(text) and text[end] == '.')
            ):
                continue

            if is_digit:
                # Ignore numbers that are the numerator of a fraction.
                if (end < len(text) and text[end] == '/'):
                    continue
                # Ignore the whole number part of a mixed fraction.
                if _is_part_of_mixed_fraction(text, end):
                    continue

                number = int(normalized_text)
                suffix = _get_ordinal_suffix(number)

            elif is_fraction:
                numerator_str, denominator_str = normalized_text.split('/')
                number = int(denominator_str)
                suffix = _get_ordinal_suffix(number)

                if int(numerator_str) > 1:
                    suffix += 's'

            result.append(text[last_idx:end] + suffix)
            last_idx = end

    result.append(text[last_idx:])
    return ''.join(result)


def ordinal_to_cardinal(text: str) -> str:
    """
    Convert ordinal numbers in a given string to cardinal numbers.

    Args:
        text: The string to convert.

    Returns:
        str: The converted string.
    """
    doc = _get_nlp_doc(text)
    result = []
    last_idx = 0

    valid_suffixes = (
        'nd', 'nds',
        'rd', 'rds',
        'st', 'sts',
        'th', 'ths',
    )

    for token in doc:
        lower_text = token.text.lower()

        # Check for standard ordinal suffixes.
        if lower_text.endswith(valid_suffixes):
            suffix_len = 3 if lower_text.endswith('s') else 2

            # Ensure the remaining base string is a number.
            base_num = token.text[:-suffix_len]
            if base_num and base_num.replace(',', '').isdigit():
                # Avoid stripping letters from the end of a decimal
                # (invalid ordinal syntax).
                if (
                    token.i >= 2
                    and doc[token.i - 1].text == '.'
                    and doc[token.i - 2].text.isdigit()
                ):
                    continue

                start = token.idx
                end = start + len(token)

                result.append(text[last_idx:start] + base_num)
                last_idx = end

    result.append(text[last_idx:])
    return ''.join(result)
