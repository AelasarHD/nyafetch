"""Combines a collected InfoSnapshot with ASCII art into the final printable,
optionally colorized, side-by-side block (the classic neofetch layout)."""
from __future__ import annotations

from typing import List, Optional

from .collectors.base import InfoSnapshot

_ANSI_COLORS = {
    "black": "\x1b[30m",
    "red": "\x1b[31m",
    "green": "\x1b[32m",
    "yellow": "\x1b[33m",
    "blue": "\x1b[34m",
    "magenta": "\x1b[35m",
    "cyan": "\x1b[36m",
    "white": "\x1b[37m",
    "orange": "\x1b[38;5;208m",  # not in the basic 8-color palette
}
_RESET = "\x1b[0m"
_BOLD = "\x1b[1m"

_LABELS = {
    "os": "OS",
    "host": "Host",
    "kernel": "Kernel",
    "uptime": "Uptime",
    "shell": "Shell",
    "terminal": "Terminal",
    "cpu": "CPU",
    "gpu": "GPU",
    "ram": "RAM",
    "disk": "Disk",
    "python": "Python",
}


def _color(text: str, name: str, no_color: bool) -> str:
    if no_color or not text or name not in _ANSI_COLORS:
        return text
    return f"{_ANSI_COLORS[name]}{text}{_RESET}"


def _values(snapshot: InfoSnapshot) -> dict:
    return {
        "os": snapshot.os_name,
        "host": snapshot.host,
        "kernel": snapshot.kernel,
        "uptime": snapshot.uptime,
        "shell": snapshot.shell,
        "terminal": snapshot.terminal,
        "cpu": snapshot.cpu,
        "gpu": snapshot.gpu,
        "ram": snapshot.ram,
        "disk": snapshot.disk,
        "python": snapshot.python_version,
    }


def _info_lines(snapshot: InfoSnapshot, fields: List[str], accent: str, no_color: bool) -> List[str]:
    values = _values(snapshot)
    header = snapshot.host if no_color else f"{_BOLD}{snapshot.host}{_RESET}"
    lines = [
        _color(header, accent, no_color),
        _color("-" * len(snapshot.host), accent, no_color),
    ]
    for key in fields:
        if key not in _LABELS:
            continue
        label = _color(_LABELS[key], accent, no_color)
        lines.append(f"{label}: {values[key]}")
    return lines


def _palette_line(no_color: bool) -> str:
    if no_color:
        return ""
    return "".join(f"\x1b[3{i}m\u2588\u2588\u2588{_RESET}" for i in range(8))


def render(
    snapshot: InfoSnapshot,
    logo_lines: List[str],
    fields: List[str],
    accent: str = "cyan",
    no_color: bool = False,
    extra_lines: Optional[List[str]] = None,
) -> str:
    info = _info_lines(snapshot, fields, accent, no_color)
    if extra_lines:
        info.append("")
        info.extend(_color(line, accent, no_color) for line in extra_lines)
    palette = _palette_line(no_color)
    if palette:
        info.append("")
        info.append(palette)

    height = max(len(logo_lines), len(info))
    logo_width = max((len(line) for line in logo_lines), default=0)

    rows = []
    for i in range(height):
        left = logo_lines[i] if i < len(logo_lines) else ""
        left_colored = _color(left, accent, no_color)
        pad = " " * (logo_width - len(left))  # pad using the *uncolored* width
        right = info[i] if i < len(info) else ""
        rows.append(f"{left_colored}{pad}   {right}")
    return "\n".join(rows)
