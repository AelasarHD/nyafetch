"""Shared cross-platform helpers for the OS-specific collectors."""
from __future__ import annotations

import os
import platform
import socket
import time
from typing import Optional

import psutil


def get_host() -> str:
    return socket.gethostname()


def get_shell() -> str:
    shell = os.environ.get("SHELL")
    if shell:
        return os.path.basename(shell)
    return os.environ.get("COMSPEC", "unknown")


def get_terminal() -> str:
    return os.environ.get("TERM_PROGRAM") or os.environ.get("TERM") or "unknown"


def get_uptime() -> str:
    seconds = int(time.time() - psutil.boot_time())
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, _ = divmod(seconds, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return " ".join(parts)


def format_cpu(brand: str) -> str:
    physical = psutil.cpu_count(logical=False) or 0
    logical = psutil.cpu_count(logical=True) or 0
    freq = psutil.cpu_freq()
    mhz = (freq.max or freq.current) if freq else None
    # Apple Silicon's psutil backend sometimes reports bogus single-digit "MHz" values.
    freq_str = f"{mhz / 1000:.1f} GHz" if mhz and mhz >= 100 else "unknown"
    return f"{brand} ({physical}C/{logical}T) {freq_str}"


def format_ram(speed_mhz: Optional[int]) -> str:
    total_gb = psutil.virtual_memory().total / (1024 ** 3)
    speed_str = f"{speed_mhz} MHz" if speed_mhz else "unknown MHz"
    return f"{total_gb:.1f} GB | {speed_str}"


def get_disk(path: str) -> str:
    du = psutil.disk_usage(path)
    used_gib = du.used / (1024 ** 3)
    total_gib = du.total / (1024 ** 3)
    return f"{used_gib:.1f} GiB / {total_gib:.1f} GiB ({du.percent:.0f}%)"


def get_python_version() -> str:
    return platform.python_version()
