"""Command-line spinner for loading heavy dependencies."""

import atexit
import math
import random
import sys
import threading
import time
import types

__all__ = ['AcceleratingSpinner']


class AcceleratingSpinner:
    """
    A context manager for displaying a logarithmically accelerating
    spinner on a background thread.
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
        self._frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

        self.accel_secs = accel_secs
        self.initial_fps = initial_fps
        self.peak_animation_fps = peak_animation_fps
        self.max_render_fps = max_render_fps

        is_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        is_utf8 = getattr(sys.stdout, 'encoding', '').lower() in (
            'utf-8',
            'utf8'
        )
        self._disabled = not (is_tty and is_utf8)

    def _spin(self) -> None:
        """Run the logarithmically accelerating spinner loop."""
        try:
            current_frame = float(random.randint(0, len(self._frames) - 1))
            last_rendered_idx = -1
            is_first_frame = True

            start_time = time.time()
            last_update_time = start_time

            loop_delay = 1.0 / self.max_render_fps

            while not self._stop_event.is_set():
                now = time.time()
                elapsed_total = now - start_time
                elapsed_since_last = now - last_update_time
                last_update_time = now

                if elapsed_total < self.accel_secs:
                    progress = elapsed_total / self.accel_secs
                    log_progress = math.log10(1 + 9 * progress)
                    current_fps = self.initial_fps + (
                        (self.peak_animation_fps - self.initial_fps)
                        * log_progress
                    )
                else:
                    current_fps = self.peak_animation_fps

                frames_to_advance = current_fps * elapsed_since_last
                current_frame += frames_to_advance

                current_frame_idx = int(current_frame) % len(self._frames)

                # Only write to the terminal if the frame actually changed.
                if current_frame_idx != last_rendered_idx:
                    char = self._frames[current_frame_idx]
                    if is_first_frame:
                        sys.stdout.write(char)
                        is_first_frame = False
                    else:
                        sys.stdout.write(f'\b{char}')

                    sys.stdout.flush()
                    last_rendered_idx = current_frame_idx

                # Sleep briefly to avoid pegging the CPU.
                self._stop_event.wait(loop_delay)

            sys.stdout.write('\r\033[K')
            sys.stdout.flush()

        except (OSError, ValueError):
            pass

    def _show_cursor(self) -> None:
        """Safely restore the terminal cursor."""
        if not self._disabled:
            try:
                sys.stdout.write('\033[?25h')
                sys.stdout.flush()
            except (OSError, ValueError):
                pass

    def __enter__(self) -> 'AcceleratingSpinner':
        """Start or bypass the spinner thread."""
        if self._disabled:
            return self

        self._stop_event.clear()

        # Remove the cursor from the terminal during animation.
        sys.stdout.write('\033[?25l')
        sys.stdout.flush()

        atexit.register(self._show_cursor)

        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None
    ) -> None:
        """Stop the spinner thread and clear the terminal line."""
        self._stop_event.set()
        if self._thread:
            self._thread.join()

        self._show_cursor()
        atexit.unregister(self._show_cursor)
