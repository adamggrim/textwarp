"""Tests for internal enumerations."""

from textwarp._core.enums import (
    CaseSeparator,
    Casing,
    CountLabels,
    ModelPriority,
    PresenceCheckType,
    RegexBoundary
)


def test_case_separator_values():
    assert CaseSeparator.DOT == '.'
    assert CaseSeparator.KEBAB == '-'
    assert CaseSeparator.SNAKE == '_'
    assert '...' not in [s.value for s in CaseSeparator]


def test_casing_enums():
    assert isinstance(Casing.SENTENCE, Casing)
    assert isinstance(Casing.START, Casing)
    assert isinstance(Casing.TITLE, Casing)


def test_count_labels_values():
    assert CountLabels.CHAR == 'Character'
    assert CountLabels.LINE == 'Line'
    assert CountLabels.SENTENCE == 'Sentence'
    assert CountLabels.WORD == 'Word'
    assert CountLabels.WORD != 'Paragraph'


def test_presence_check_type_enums():
    assert isinstance(PresenceCheckType.CASE, PresenceCheckType)
    assert isinstance(PresenceCheckType.REGEX, PresenceCheckType)
    assert isinstance(PresenceCheckType.SUBSTRING, PresenceCheckType)


def test_regex_boundary_enums():
    assert isinstance(RegexBoundary.WORD_BOUNDARY, RegexBoundary)
    assert isinstance(RegexBoundary.START_ANCHOR, RegexBoundary)
    assert isinstance(RegexBoundary.END_ANCHOR, RegexBoundary)


def test_model_priority_values():
    assert ModelPriority.ACCURACY == 'accuracy'
    assert ModelPriority.SPEED == 'speed'
