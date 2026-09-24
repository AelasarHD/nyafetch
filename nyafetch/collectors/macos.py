"""macOS-specific info collector."""
from __future__ import annotations

import platform
import re
import subprocess
from typing import Optional

from . import common
from .base import InfoSnapshot

# Codenames for modern (major-version-only) releases.
_CODENAMES = {
    26: "Tahoe",
    15: "Sequoia",
    14: "Sonoma",
    13: "Ventura",
    12: "Monterey",
    11: "Big Sur",
}
# Legacy 10.x releases are identified by (major, minor).
_LEGACY_CODENAMES = {
    (10, 15): "Catalina",
    (10, 14): "Mojave",
    (10, 13): "High Sierra",
    (10, 12): "Sierra",
    (10, 11): "El Capitan",
    (10, 10): "Yosemite",
    (10, 9): "Mavericks",
    (10, 8): "Mountain Lion",
    (10, 7): "Lion",
    (10, 6): "Snow Leopard",
    (10, 5): "Leopard",
    (10, 4): "Tiger",
}


def _codename(mac_ver: str) -> Optional[str]:
    parts = mac_ver.split(".")
    try:
        major = int(parts[0])
        minor = int(parts[1]) if len(parts) > 1 else 0
    except (ValueError, IndexError):
        return None
    if major >= 11:
        return _CODENAMES.get(major)
    return _LEGACY_CODENAMES.get((major, minor))


def _os_name() -> str:
    mac_ver = platform.mac_ver()[0]
    codename = _codename(mac_ver)
    return f"macOS {mac_ver} ({codename})" if codename else f"macOS {mac_ver}".strip()


def collect() -> InfoSnapshot:
    return InfoSnapshot(
        os_name=_os_name(),
        host=common.get_host(),
        kernel=platform.release(),
        uptime=common.get_uptime(),
        shell=common.get_shell(),
        terminal=common.get_terminal(),
        cpu=common.format_cpu(_cpu_brand() or platform.processor() or "unknown"),
        gpu=_gpu_name() or "unknown",
        ram=common.format_ram(_ram_speed_mhz()),
        disk=common.get_disk("/"),
        python_version=common.get_python_version(),
    )


def _cpu_brand() -> Optional[str]:
    try:
        result = subprocess.run(
            ["sysctl", "-n", "machdep.cpu.brand_string"],
            capture_output=True,
            text=True,
            timeout=2,
            check=True,
        )
        return result.stdout.strip() or None
    except (subprocess.SubprocessError, OSError):
        return None


def _gpu_name() -> Optional[str]:
    try:
        result = subprocess.run(
            ["system_profiler", "SPDisplaysDataType"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
    except (subprocess.SubprocessError, OSError):
        return None
    match = re.search(r"Chipset Model:\s*(.+)", result.stdout)
    return match.group(1).strip() if match else None


def _ram_speed_mhz() -> Optional[int]:
    try:
        result = subprocess.run(
            ["system_profiler", "SPMemoryDataType"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
    except (subprocess.SubprocessError, OSError):
        return None
    match = re.search(r"Speed:\s*(\d+)\s*MHz", result.stdout)
    return int(match.group(1)) if match else None
