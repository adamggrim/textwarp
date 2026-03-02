"""Tests for replacement command functions."""

from textwarp._commands import replacement

CASE_TEST_STRING = 'pascal_case'

TEXT_TEST_STRING = (
    'My heart aches, and a drowsy numbness pains'
    'My sense, as though of hemlock I had drunk.'
)

REGEX_TEST_STRING = '525,600 minutes'


def test_replace_case(monkeypatch):
    """Test case replacement."""
    user_inputs = iter(['snake', 'pascal'])
    monkeypatch.setattr('builtins.input', lambda: next(user_inputs))

    result = replacement.replace_case(CASE_TEST_STRING)
    assert result == 'PascalCase'


def test_replace_text(monkeypatch):
    """Test text replacement."""
    user_inputs = iter(['hemlock', 'poison'])
    monkeypatch.setattr('builtins.input', lambda: next(user_inputs))

    result = replacement.replace(TEXT_TEST_STRING)

    assert 'of poison I had drunk' in result
    assert 'hemlock' not in result


def test_replace_regex(monkeypatch):
    """Test regular expression replacement."""
    target_regex = r'(\d{3}),(\d{3})'
    replacement_str = 'Five hundred twenty-five thousand, six hundred'

    # Simulate the user typing the regex and the replacement text.
    user_inputs = iter([target_regex, replacement_str])
    monkeypatch.setattr('builtins.input', lambda: next(user_inputs))

    result = replacement.replace_regex(REGEX_TEST_STRING)

    assert result == 'Five hundred twenty-five thousand, six hundred minutes'
