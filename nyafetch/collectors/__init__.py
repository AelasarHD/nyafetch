"""Picks the right OS-specific collector and exposes a single collect() entry point."""
from __future__ import annotations

import sys

from .base import InfoSnapshot

__all__ = ["InfoSnapshot", "collect"]


def collect() -> InfoSnapshot:
    if sys.platform == "darwin":
        from . import macos as _impl
    elif sys.platform.startswith("win"):
        from . import windows as _impl
    else:
        from . import linux as _impl
    return _impl.collect()
