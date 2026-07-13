"""Tests for the command-line spinner."""

import sys
from textwarp._cli.spinner import AcceleratingSpinner


def test_spinner_context_manager(monkeypatch):
    """
    Test that the logarithmically accelerating spinner starts and stops
    cleanly without errors.
    """
    class MockStdout:
        encoding = 'utf-8'
        def isatty(self): return True
        def write(self, text): pass
        def flush(self): pass

    monkeypatch.setattr(sys, 'stdout', MockStdout())

    with AcceleratingSpinner(accel_secs=0.1, max_render_fps=10.0) as spinner:
        assert spinner._thread is not None
        assert spinner._thread.is_alive() is True

    assert spinner._thread.is_alive() is False
