"""Tests for Markdown parsing and transformation."""

from hypothesis import given, strategies

from textwarp._lib.markdown import process_markdown, strip_markdown


def test_strip_markdown_removes_formatting():
    markdown = (
        '# Canto XI\n'
        '*Be bold, be bold*, and euery where **Be bold**\n'
        '- Stanza 54\n'
        '[link](https://example.com)'
    )
    stripped = strip_markdown(markdown)

    assert 'Canto XI' in stripped
    assert 'Be bold, be bold' in stripped
    assert 'Stanza 54' in stripped
    assert 'link' in stripped
    assert '**' not in stripped
    assert '#' not in stripped
    assert 'https://example.com' not in stripped


def test_process_markdown_transforms_text_nodes():
    markdown = '## The Faerie Queene\n\n**XII.** Moral vertues.'

    def mock_transform(text: str) -> str:
        return text.upper()

    transformed = process_markdown(markdown, mock_transform)
    assert '## THE FAERIE QUEENE' in transformed
    assert '**XII.** MORAL VERTUES.' in transformed


def test_strip_markdown_empty_string():
    assert strip_markdown('') == ''


def test_process_markdown_empty_string():
    assert process_markdown('', str.upper) == ''


@given(strategies.text())
def test_strip_markdown_no_crash(s):
    result = strip_markdown(s)
    assert isinstance(result, str)
