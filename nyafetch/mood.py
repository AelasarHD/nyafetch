"""nyafetch's twist on the classic static logo: a reactive ASCII cat mascot
whose mood (and color) reflect real CPU/memory/disk load, not just a picture."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

import psutil

from .ascii_art import LOGOS as _OS_LOGOS

# The "overloaded" face: a much bigger, angrier cat for when things are on fire.
_OVERLOADED_CAT = """\
⠀⠀⠀⠀⠀⠀⣠⣶⣶⢶⣶⣶⣶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢰⡿⠃⠀⠀⠀⠀⠀⠉⠙⢻⣦⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀⠀⢀⣠⣶⠿⠛⠉⠉⠙⣿⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠩⠉⠈⠇⠀⠀⢈⠀⠈⠉⠉⠛⠻⠟⠋⠁⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠈⠀⠁⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⠀⠀⠀⠀⠀⠀
⠀⣀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠃⠀⠀⠀⠀⠀⠀
⠀⠛⠿⢶⣤⣄⠀⢀⣴⡟⠋⠉⠉⠙⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⢀⣠⣴⡆⠀
⠀⠀⠀⠀⠈⠉⠀⣾⣿⣧⠀⠀⠀⣠⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⣰⣿⣿⠋⠁⠀⠀⠈⣿⣿⣿⡆⠰⡿⠟⠋⠁⠀⠀
⢠⣴⣦⣤⣤⡀⠀⣿⣿⣿⣶⣶⣶⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⢀⣿⣿⣿⣄⡀⠀⣀⣰⣿⣿⣿⡇⠀⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠉⠉⠁⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠶⠶⠶⠶⠶⠆
⠀⠀⠀⠀⠀⠀⠆⠀⠀⣹⣿⣿⣿⣿⣿⣧⣿⣿⠟⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣻⣿⣿⣿⡿⠟⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣾⣍⣛⠿⠿⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⣷⣶⣶⣶⣶⣤⣤⣤⣤⣤⣴⣶⣶⡶⠿⠟⠛⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣶⠀⠀⠀⠀⠈⠁⠉⠀⣠⣽⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡀⢀⣤⣤⣤⣤⠀⣸⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⠿⠋⠁⠀⠛⠿⠛⠁⠀⠀⠀"""

# The "zen" face: fully relaxed, curled up and dozing.
_ZEN_CAT = """\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡴⣆⠀⠀⠀⠀⠀⣠⡀⠀⠀⠀⠀⠀⠀⣼⣿⡗⠀⠀⠀⠀
⠀⠀⠀⣠⠟⠀⠘⠷⠶⠶⠶⠾⠉⢳⡄⠀⠀⠀⠀⠀⣧⣿⠀⠀⠀⠀⠀
⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣤⣤⣤⣤⣤⣿⢿⣄⠀⠀⠀⠀
⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⠀⠀⠀⠀⠀⠙⣷⡴⠶⣦
⠀⠀⢱⡀⠀⠉⠉⠀⠀⠀⠀⠛⠃⠀⢠⡟⠀⠀⠀⢀⣀⣠⣤⠿⠞⠛⠋
⣠⠾⠋⠙⣶⣤⣤⣤⣤⣤⣀⣠⣤⣾⣿⠴⠶⠚⠋⠉⠁⠀⠀⠀⠀⠀⠀
⠛⠒⠛⠉⠉⠀⠀⠀⣴⠟⢃⡴⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

# The "chill" face: the braille cat, mildly loaded (~20-45%), also used for the classic macOS logo.
_CHILL_CAT = _OS_LOGOS["macos"]

# The "stressed" face: orange warning sign, load is climbing.
_ORANGE_CAT = """\
⠀⠀⠀⠀⠀⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢿⣧⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣿⣇⠀⢸⣿⣿⣦⣤⣄⣀⣴⣿⣷⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣿⣿⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⢀⣼⣿⣿⣧⣿⣿⣿⣿⡟⣿⣿⣿⠻⣿⠂⡀⠀
⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣦⣿⣏⠁⠀
⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀
⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀
⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀
⢠⣾⣿⡿⠋⠀⠈⠙⣿⣿⣿⡿⣿⡿⠿⠟⢿⣿⣿⣷⣄⠀
⠈⠿⡿⠃⠀⠀⠀⠀⣿⣿⣿⣧⠀⠀⠀⠀⠀⠉⠻⣿⡿⠂
⠀⠀⠀⠀⠀⠀⠀⠈⢿⡿⠟⠃⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀"""

_RAW_FACES = {
    "zen": _ZEN_CAT.splitlines(),
    "chill": list(_CHILL_CAT),
    "stressed": _ORANGE_CAT.splitlines(),
    "overloaded": _OVERLOADED_CAT.splitlines(),
}

# Braille pattern blank -- matches the width of the glyphs used inside the art
# itself, so padding doesn't shift under fonts that size regular spaces differently.
_BLANK = "\u2800"


def _pad(face: List[str], width: int, height: int) -> List[str]:
    lines = [line + _BLANK * (width - len(line)) for line in face]
    extra_rows = height - len(lines)
    top = extra_rows // 2
    bottom = extra_rows - top
    blank_row = _BLANK * width
    return [blank_row] * top + lines + [blank_row] * bottom


_TARGET_WIDTH = max(len(line) for face in _RAW_FACES.values() for line in face)
_TARGET_HEIGHT = max(len(face) for face in _RAW_FACES.values())

_FACES = {name: _pad(face, _TARGET_WIDTH, _TARGET_HEIGHT) for name, face in _RAW_FACES.items()}

_CAPTIONS = {
    "zen": "no issues so far. sleepin'",
    "chill": "vibing. nothing to see here.",
    "stressed": "?!... something's off... eating resources!",
    "overloaded": "meltdown incoming. seriously, close some tabs.",
}

# Escalating theme: cyan -> green -> orange -> red as load climbs.
_COLORS = {
    "zen": "cyan",
    "chill": "green",
    "stressed": "orange",
    "overloaded": "red",
}

# Ordered thresholds: the mood is picked by the worst (highest) of the three metrics.
_THRESHOLDS = (
    (40, "zen"),
    (70, "chill"),
    (92, "stressed"),
)


@dataclass
class Mood:
    name: str
    face: List[str]
    caption: str
    color: str


def compute_mood(cpu_percent: float, memory_percent: float, disk_percent: float) -> Mood:
    load = max(cpu_percent, memory_percent, disk_percent)
    name = "overloaded"
    for ceiling, mood_name in _THRESHOLDS:
        if load < ceiling:
            name = mood_name
            break
    return Mood(name=name, face=list(_FACES[name]), caption=_CAPTIONS[name], color=_COLORS[name])


def sample_mood(disk_path: str = "/") -> Mood:
    cpu_percent = psutil.cpu_percent(interval=0.2)
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage(disk_path).percent
    return compute_mood(cpu_percent, memory_percent, disk_percent)
