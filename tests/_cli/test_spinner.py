"""Tests for the command-line spinner."""

import sys
from textwarp._cli.spinner import AcceleratingSpinner


def _dummy_task():
    import time
    time.sleep(0.1)
    return True

def test_spinner_process(monkeypatch):
    """
    Test that the logarithmically accelerating spinner cleanly executes
    a task.
    """
    class MockStdout:
        encoding = 'utf-8'
        def isatty(self): return True
        def write(self, text): pass
        def flush(self): pass

    monkeypatch.setattr(sys, 'stdout', MockStdout())

    spinner = AcceleratingSpinner(accel_secs=0.1, max_render_fps=10.0)

    result = spinner.run(_dummy_task)
    assert result is True
