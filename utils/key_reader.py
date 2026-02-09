"""Cross-platform single-key reader for interactive modes."""
from __future__ import annotations

import os
import sys
from typing import Optional


def read_key() -> str:
    """Read a single keypress and return it as a lowercase string.

    - Windows: uses msvcrt.getch()
    - POSIX: uses termios/tty raw mode

    Raises RuntimeError if stdin is not a TTY.
    """
    if not sys.stdin.isatty():
        raise RuntimeError("Interactive mode requires a TTY (interactive terminal).")

    if os.name == "nt":
        import msvcrt  # type: ignore
        ch = msvcrt.getch()
        # Handle special keys (arrows etc.) which return a prefix byte.
        if ch in (b"\x00", b"\xe0"):
            _ = msvcrt.getch()
            return ""
        try:
            return ch.decode("utf-8", errors="ignore").lower()
        except Exception:
            return ""
    else:
        import termios
        import tty

        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            return (ch or "").lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
