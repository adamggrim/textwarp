"""Command-line spinner for loading heavy dependencies."""

import math
import multiprocessing
import random
import sys
import time
from typing import Callable, Any

__all__ = ['AcceleratingSpinner', 'run_with_spinner']

_SPINNER_FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
_NUM_FRAMES = len(_SPINNER_FRAMES)


def _spinner_worker(
    stop_event: Any,
    accel_secs: float,
    initial_fps: float,
    peak_animation_fps: float,
    loop_delay: float
) -> None:
    """
    Run the logarithmically accelerating spinner in a background
    process.
    """
    current_frame = float(random.randint(0, _NUM_FRAMES - 1))
    last_rendered_idx = -1
    start_time = last_update_time = time.time()

    while not stop_event.is_set():
        now = time.time()
        elapsed_total = now - start_time
        elapsed_since_last = now - last_update_time
        last_update_time = now

        if elapsed_total < accel_secs:
            progress = elapsed_total / accel_secs
            log_progress = math.log10(1 + 9 * progress)
            current_fps = (
                initial_fps
                + (peak_animation_fps - initial_fps)
                * log_progress
            )
        else:
            current_fps = peak_animation_fps

        current_frame += current_fps * elapsed_since_last
        current_frame_idx = int(current_frame) % _NUM_FRAMES

        # Only write to the terminal if the frame actually changed.
        if current_frame_idx != last_rendered_idx:
            char = _SPINNER_FRAMES[current_frame_idx]
            sys.stdout.write(
                char if last_rendered_idx == -1 else f'\b{char}'
            )
            sys.stdout.flush()
            last_rendered_idx = current_frame_idx

        # Sleep briefly to avoid pegging the CPU.
        time.sleep(loop_delay)

    sys.stdout.write('\r\033[K')
    sys.stdout.flush()


class AcceleratingSpinner:
    """
    A class for displaying a logarithmically accelerating spinner and
    offloading other work to a background process.
    """

    def __init__(
        self,
        accel_secs: float = 3.0,
        initial_fps: float = 6.0,
        peak_animation_fps: float = 120.0,
        max_render_fps: float = 60.0
    ) -> None:
        """
        Initialize the spinner state.

        Args:
            accel_secs: Seconds to peak speed.
            initial_fps: Starting frames per second.
            peak_animation_fps: Peak frames per second.
            max_render_fps: Terminal throttle to prevent dropped frames.
        """
        self.accel_secs = accel_secs
        self.initial_fps = initial_fps
        self.peak_animation_fps = peak_animation_fps
        self.loop_delay = 1.0 / max_render_fps

        is_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        is_utf8 = getattr(sys.stdout, 'encoding', '').lower() in (
            'utf-8',
            'utf8'
        )
        self._disabled = not (is_tty and is_utf8)

    def _show_cursor(self) -> None:
        """Restore the terminal cursor."""
        if not self._disabled:
            try:
                sys.stdout.write('\033[?25h')
                sys.stdout.flush()
            except (OSError, ValueError):
                pass

    def _hide_cursor(self) -> None:
        """Hide the terminal cursor."""
        if not self._disabled:
            try:
                sys.stdout.write('\033[?25l')
                sys.stdout.flush()
            except (OSError, ValueError):
                pass

    def run(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """
        Run a function on the main process while the logarithmically
        accelerating spinner runs on a background process.
        """
        if self._disabled:
            return func(*args, **kwargs)

        self._hide_cursor()

        stop_event = multiprocessing.Event()
        spinner_process = multiprocessing.Process(
            target=_spinner_worker,
            args=(
                stop_event,
                self.accel_secs,
                self.initial_fps,
                self.peak_animation_fps,
                self.loop_delay
            )
        )

        try:
            spinner_process.start()
            return func(*args, **kwargs)
        finally:
            stop_event.set()
            spinner_process.join()
            self._show_cursor()


def run_with_spinner(func: Callable, *args: Any, **kwargs: Any) -> Any:
    """Helper function to execute another function with the spinner."""
    spinner = AcceleratingSpinner()
    return spinner.run(func, *args, **kwargs)
