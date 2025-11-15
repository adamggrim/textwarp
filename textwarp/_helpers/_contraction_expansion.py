from .._config import CONTRACTIONS_MAP
from ..warping import curly_to_straight


def apply_expansion_casing(original_word: str, expanded_word: str) -> str:
    """
    Apply the casing of the original word to the expanded word.

    Args:
        original_word: The original word.
        expanded_word: The cased word.

    Returns:
        str: The expanded word in the original word's casing.
    """
    if original_word.isupper():
        return expanded_word.upper()
    elif original_word.istitle():
        return expanded_word.capitalize()
    return expanded_word


def repl_contraction_from_dict(contraction: str) -> str:
    """
    Replace a contraction using the contractions map.

    Args:
        contraction: The contraction to expand.

    Returns:
        str: The expanded contraction.
    """
    normalized_contraction: str = curly_to_straight(contraction).lower()
    expanded_contraction: str = CONTRACTIONS_MAP.get(
        normalized_contraction, contraction
    )
    return apply_expansion_casing(contraction, expanded_contraction)
