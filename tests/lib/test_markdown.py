"""Tests for Markdown parsing and transformation."""

from textwarp._lib.markdown import process_markdown, strip_markdown


def test_strip_markdown_removes_formatting():
    """Test that `strip_markdown` extracts plain text."""
    markdown_text = (
        '# Header 1\n'
        'Paragraph with **bold** and *italic* text.\n'
        '- Item 1\n'
        '- Item 2\n'
        '[link](https://example.com)'
    )
    plain_text = strip_markdown(markdown_text)

    assert 'Header 1' in plain_text
    assert 'Paragraph with bold and italic text.' in plain_text
    assert 'Item 1' in plain_text
    assert 'link' in plain_text
    assert '**' not in plain_text
    assert '#' not in plain_text
    assert 'https://example.com' not in plain_text


def test_process_markdown_transforms_text_nodes():
    """
    Test that `process_markdown` applies a transformation function
    solely to text nodes.
    """
    markdown_text = '## Title\n\n**Bold** text.'

    def mock_transform(text: str) -> str:
        """Dummy transformation function for testing."""
        return text.upper()

    transformed = process_markdown(markdown_text, mock_transform)
    assert '## TITLE' in transformed
    assert '**BOLD** TEXT.' in transformed


def test_strip_markdown_empty_string():
    """Test that `strip_markdown` handles empty strings safely."""
    assert strip_markdown('') == ''


def test_process_markdown_empty_string():
    """Test that `process_markdown` handles empty strings safely."""
    assert process_markdown('', str.upper) == ''
