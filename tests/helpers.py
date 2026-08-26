"""Helper functions for the test suite."""

def normalize_output(text: str) -> str:
    """Normalize whitespace for wrapped terminal output."""
    return ' '.join(text.split())
