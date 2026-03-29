"""
composeforge.cli.colors
~~~~~~~~~~~~~~~~~~~~~~~~
ANSI color codes and console output helpers.
"""


class C:
    """ANSI escape codes for terminal coloring."""

    G  = "\033[92m"   # green
    B  = "\033[94m"   # blue
    CY = "\033[96m"   # cyan
    Y  = "\033[93m"   # yellow
    R  = "\033[91m"   # red
    BD = "\033[1m"    # bold
    RS = "\033[0m"    # reset


def ok(msg: str) -> None:
    """Print a success (green ✓) message."""
    print(f"  {C.G}✓{C.RS} {msg}")


def info(msg: str) -> None:
    """Print an info (blue →) message."""
    print(f"  {C.B}→{C.RS} {msg}")


def warn(msg: str) -> None:
    """Print a warning (yellow ⚠) message."""
    print(f"  {C.Y}⚠{C.RS} {msg}")


def err(msg: str) -> None:
    """Print an error (red ✗) message."""
    print(f"  {C.R}✗{C.RS} {msg}")
