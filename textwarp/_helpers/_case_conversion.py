from typing import Callable

from textwarp.enums import CaseSeparator
from textwarp.regexes import ProgrammingCasePatterns

from ._punctuation import _remove_apostrophes


def _change_first_letter_case(
    word: str,
    casing_func: Callable[[str], str]
) -> str:
    """
    Change the case of the first letter of a string without modifying
    any other letters.

    Args:
        text: The string to convert.
        casing_func: The function to apply to the first letter
            (i.e., str.upper or str.lower).

    Returns:
        str: The converted text.
    """
    for i, char in enumerate(word):
        if char.isalpha():
            # Modify the first letter and return the new text.
            return word[:i] + casing_func(char) + word[i+1:]

    # Return the original text if there are no letters in the string.
    return word


def _to_separator_case(
    text: str,
    separator: CaseSeparator
) -> str:
    """
    Convert a string to dot case, kebab case or snake case.

    Args:
        text: The string to convert.
        separator: The separator for the converted string.

    Returns:
        str: The converted string.
    """
    no_apostrophes_text: str = _remove_apostrophes(text)
    parts: list[str] = (
        ProgrammingCasePatterns.SPLIT_FOR_SEPARATOR_CONVERSION.split(
            no_apostrophes_text
        )
    )
    processed_parts: list[str] = []

    separator_pattern_name: str = f'{separator.name}_WORD'
    separator_pattern = getattr(
        ProgrammingCasePatterns,
        separator_pattern_name
    )
    other_separators = [s for s in CaseSeparator if s != separator]

    for i, part in enumerate(parts):
        processed_part: str
        # Part contains no alphabetical characters and is not a single
        # space.
        if not any(char.isalpha() for char in part) and part != ' ':
            processed_parts.append(part)
            continue
        # Part is a single space.
        elif part == ' ':
            # Default to keeping the space.
            processed_part = part
            # Check if the space is surrounded by lowercase parts.
            if i > 0 and i < len(parts) - 1:
                prev_part = parts[i - 1]
                next_part = parts[i + 1]
                if (prev_part.isalpha() and prev_part.islower() and
                        next_part.isalpha() and next_part.islower()):
                    processed_part = separator.value
        # Part is already in the given separator case.
        elif separator_pattern.match(part):
            processed_part = part
        # Part is in another separator case.
        elif any(
            getattr(ProgrammingCasePatterns, f'{s.name}_WORD').match(part)
            for s in other_separators
        ):
            processed_part = (
                ProgrammingCasePatterns.ANY_SEPARATOR.sub(
                    separator.value,
                    part
                )
            )
        # Part is in camel or Pascal case.
        elif (ProgrammingCasePatterns.CAMEL_WORD.match(part)
              or ProgrammingCasePatterns.PASCAL_WORD.match(part)):
            # Break camel case and Pascal case into constituent words.
            broken_words: list[str] = (
                ProgrammingCasePatterns.SPLIT_CAMEL_OR_PASCAL.split(part)
            )
            lower_words = [word.lower() for word in broken_words]
            processed_part = separator.value.join(lower_words)
        # Part is not in any of the above cases.
        else:
            processed_part = part.lower()
        processed_parts.append(processed_part)

    return ''.join(processed_parts)
