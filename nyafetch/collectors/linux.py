"""Linux-specific info collector."""
from __future__ import annotations

import platform
import re
import subprocess
from pathlib import Path
from typing import Optional

from . import common
from .base import InfoSnapshot


def collect() -> InfoSnapshot:
    return InfoSnapshot(
        os_name=_os_release_name() or platform.system(),
        host=common.get_host(),
        kernel=platform.release(),
        uptime=common.get_uptime(),
        shell=common.get_shell(),
        terminal=common.get_terminal(),
        cpu=common.format_cpu(_cpu_model() or platform.processor() or "unknown"),
        gpu=_gpu_name() or "unknown",
        ram=common.format_ram(_ram_speed_mhz()),
        disk=common.get_disk("/"),
        python_version=common.get_python_version(),
    )


def _os_release_name() -> Optional[str]:
    path = Path("/etc/os-release")
    if not path.exists():
        return None
    data = {}
    for line in path.read_text().splitlines():
        if "=" in line:
            key, _, value = line.partition("=")
            data[key] = value.strip().strip('"')
    return data.get("PRETTY_NAME")


def _cpu_model() -> Optional[str]:
    path = Path("/proc/cpuinfo")
    if not path.exists():
        return None
    match = re.search(r"model name\s*:\s*(.+)", path.read_text())
    return match.group(1).strip() if match else None


def _gpu_name() -> Optional[str]:
    try:
        result = subprocess.run(["lspci"], capture_output=True, text=True, timeout=5, check=True)
    except (subprocess.SubprocessError, OSError):
        return None
    for line in result.stdout.splitlines():
        if "VGA compatible controller" in line or "3D controller" in line:
            return line.split(":", 2)[-1].strip()
    return None


def _ram_speed_mhz() -> Optional[int]:
    # Requires root on most distros; fails gracefully to "unknown" otherwise.
    try:
        result = subprocess.run(
            ["dmidecode", "--type", "17"], capture_output=True, text=True, timeout=5, check=True
        )
    except (subprocess.SubprocessError, OSError):
        return None
    match = re.search(r"Speed:\s*(\d+)\s*MT/s", result.stdout) or re.search(r"Speed:\s*(\d+)\s*MHz", result.stdout)
    return int(match.group(1)) if match else None
