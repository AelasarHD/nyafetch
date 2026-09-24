"""Windows-specific info collector."""
from __future__ import annotations

import platform
import subprocess
from typing import Optional

from . import common
from .base import InfoSnapshot


def collect() -> InfoSnapshot:
    win_ver = " ".join(part for part in platform.win32_ver()[:2] if part).strip()
    return InfoSnapshot(
        os_name=f"Windows {win_ver}".strip() if win_ver else platform.system(),
        host=common.get_host(),
        kernel=platform.version(),
        uptime=common.get_uptime(),
        shell=common.get_shell(),
        terminal=common.get_terminal(),
        cpu=common.format_cpu(platform.processor() or "unknown"),
        gpu=_gpu_name() or "unknown",
        ram=common.format_ram(_ram_speed_mhz()),
        disk=common.get_disk("C:\\"),
        python_version=common.get_python_version(),
    )


def _gpu_name() -> Optional[str]:
    try:
        result = subprocess.run(
            ["wmic", "path", "win32_VideoController", "get", "name"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
    except (subprocess.SubprocessError, OSError):
        return None
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip() and "Name" not in line]
    return lines[0] if lines else None


def _ram_speed_mhz() -> Optional[int]:
    try:
        result = subprocess.run(
            ["wmic", "memorychip", "get", "speed"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
    except (subprocess.SubprocessError, OSError):
        return None
    values = [line.strip() for line in result.stdout.splitlines() if line.strip().isdigit()]
    return int(values[0]) if values else None
