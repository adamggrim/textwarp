"""Tests for Markdown parsing and transformation."""

from textwarp._lib.markdown import process_markdown, strip_markdown


def test_strip_markdown_removes_formatting():
    markdown_text = (
        '# Canto XI\n'
        '*Be bold, be bold*, and euery where **Be bold**\n'
        '- Stanza 54\n'
        '[link](https://example.com)'
    )
    plain_text = strip_markdown(markdown_text)

    assert 'Canto XI' in plain_text
    assert 'Be bold, be bold' in plain_text
    assert 'Stanza 54' in plain_text
    assert 'link' in plain_text
    assert '**' not in plain_text
    assert '#' not in plain_text
    assert 'https://example.com' not in plain_text


def test_process_markdown_transforms_text_nodes():
    markdown_text = '## The Faerie Queene\n\n**XII.** Moral vertues.'

    def mock_transform(text: str) -> str:
        return text.upper()

    transformed = process_markdown(markdown_text, mock_transform)
    assert '## THE FAERIE QUEENE' in transformed
    assert '**XII.** MORAL VERTUES.' in transformed


def test_strip_markdown_empty_string():
    assert strip_markdown('') == ''


def test_process_markdown_empty_string():
    assert process_markdown('', str.upper) == ''
